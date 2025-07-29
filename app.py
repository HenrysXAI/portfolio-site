import os
import re
import requests
from markupsafe import escape
from flask import Flask, request, redirect, flash, render_template
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    # reCAPTCHA v2 verification
    recaptcha_response = request.form.get('g-recaptcha-response')
    recaptcha_secret = '6Lc_9pIrAAAAA1cdVfW6_E7kTFNJy-4b2g32MM1'
    recaptcha_verify = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': recaptcha_secret, 'response': recaptcha_response}
    ).json()

    if not recaptcha_verify.get('success'):
        flash('reCAPTCHA verification failed.', 'error')
        return redirect('/')

    name = escape(request.form['name'].strip())
    email = escape(request.form['email'].strip())
    message = escape(request.form['message'].strip())

    # Basic validation
    if not name or not email or not message:
        flash('All fields are required.', 'error')
        return redirect('/')

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Invalid email address.', 'error')
        return redirect('/')

    if len(name) > 100 or len(email) > 100 or len(message) > 1000:
        flash('Input is too long.', 'error')
        return redirect('/')

    try:
        msg = Message(
            subject=f"New message from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"From: {name} <{email}>\n\n{message}"
        )
        mail.send(msg)
        flash('Message sent successfully!', 'success')
    except Exception as e:
        print(f"Error: {e}")
        flash('Failed to send message.', 'error')

    return redirect('/')
