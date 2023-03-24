from app import app, db
from flask import render_template, redirect, url_for, flash
# from fake_data import posts
from app.forms import SignUpForm, LoginForm, PostForm, SearchForm
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods=["GET", "POST"])
def index():
    posts = Post.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search_term.data
        # posts = Post.query.filter(Post.title.ilike(f"%{search_term}%")).all()
        posts = db.session.execute(db.select(Post).where((Post.title.ilike(f"%{search_term}%")) | (Post.body.ilike(f"%{search_term}%")))).scalars().all()
    return render_template('index.html', posts=posts, form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the form (in the context of the current request)
    form = SignUpForm()
    # Check if the form was submitted and that all of the fields are valid
    if form.validate_on_submit():
        # If so, get the data from the form fields
        print('Hooray our form was validated!!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # Check to see if there is already a user with either username or email
        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:
            # Flash a message saying that user with email/username already exists
            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Check if there is a user with username and that password
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            # If the user exists and has the correct password, log them in
            login_user(user)
            flash(f'You have successfully logged in as {username}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))


@app.route('/create', methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Get the data from the form
        title = form.title.data
        body = form.body.data
        image_url = form.image_url.data or None
        # Create an instance of Post with form data AND auth user ID
        new_post = Post(title=title, body=body, image_url=image_url, user_id=current_user.id)
        flash(f"{new_post.title} has been created!", "success")
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@app.route('/edit/<post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = PostForm()
    post_to_edit = Post.query.get_or_404(post_id)
    # Make sure that the post author is the current user
    if post_to_edit.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))

    # If form submitted, update Post
    if form.validate_on_submit():
        # update the post with the form data
        post_to_edit.title = form.title.data
        post_to_edit.body = form.body.data
        post_to_edit.image_url = form.image_url.data
        # Commit that to the database
        db.session.commit()
        flash(f"{post_to_edit.title} has been edited!", "success")
        return redirect(url_for('index'))

    # Pre-populate the form with Post To Edit's values
    form.title.data = post_to_edit.title
    form.body.data = post_to_edit.body
    form.image_url.data = post_to_edit.image_url
    return render_template('edit.html', form=form, post=post_to_edit)


@app.route('/delete/<post_id>')
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))

    db.session.delete(post_to_delete)
    db.session.commit()
    flash(f"{post_to_delete.title} has been deleted", "info")
    return redirect(url_for('index'))