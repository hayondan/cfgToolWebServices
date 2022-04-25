from flask import request, render_template, app
from flask_wtf import form
import flask


@app.route("/temp", methods=['GET', 'PUT', 'POST'])
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            pass # do something
        elif request.form['submit_button'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html', form=form)