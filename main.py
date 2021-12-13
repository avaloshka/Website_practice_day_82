from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
import smtplib, ssl
from email.mime.text import MIMEText
import os


MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_CONFIG")

Bootstrap(app)


# Create a Form Class
class Form(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    email = StringField('Please enter your valid email')
    message = StringField('Enter your message here')
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact_me():
    form = Form()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Send an email
        message = f"Subject: {name}\n\n{message}\n\n {email}"
        smtpserver = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(MY_EMAIL, MY_PASSWORD)
        smtpserver.sendmail(MY_EMAIL, MY_EMAIL, message)
        smtpserver.quit()

        return redirect(url_for('home'))

    return render_template('contact_me.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)