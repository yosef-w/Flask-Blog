from app import app

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def hello_test():
    return 'This is a test!'