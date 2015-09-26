from __future__ import print_function
__author__ = 'Bernard'

from flask import render_template, request, Flask
from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from forms import ComponentsForm

app = Flask(__name__)


@app.route('/showcomponent', methods=['GET', 'POST'])
def showcomponent():
    form = ComponentsForm()
    form.name.data = "Test"
    print("Start of test")
    print(form.name.label)
    print(form.name)
    if request.method == 'POST':
        print ("POST method")
        if not form.validate():
            return render_template('componentform.html', form=form)
        else:
            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
    elif request.method == 'GET':
        print ("GET method")
        return render_template('componentform.html', form=form)


app.run(debug=True)