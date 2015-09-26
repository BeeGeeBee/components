__author__ = 'Bernard'

from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/string/')
def return_string():
    return "HelloWorld.Again."

@app.route('/object/')
def return_object():
    h1={'Content-Type': 'text/plain'}
#    headers=dict('Content-Type', 'text/plain')
    x = 42
#    return make_response('Hello World', status=200, headers=h1)
    return make_response('Hello World')
#    return "Object function"

@app.route('/tuple/')
def return_tuple():
    return 'Hello World tuple',200,{'Content-Type': 'text/html'}

@app.before_request
def before():
    print "Before"

@app.after_request
def after(response):
    print "After", response
    return response

if __name__ == '__main__':
    app.run(debug = True)