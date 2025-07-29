import os
import re
import requests
from markupsafe import escape
from flask import Flask, request, redirect, flash, render_template
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mail configuration
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
    name = escape(request.form['name'].strip())
    email = escape(request.form['email'].strip())
    message = escape(request.form['message'].strip())
    recaptcha_response = request.form.get('g-recaptcha-response')

    # Validate non-empty
    if not name or not email or not message:
        flash('All fields are required.', 'error')
        return redirect('/')

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Invalid email address.', 'error')
        return redirect('/')

    # Length validation
    if len(name) > 100 or len(email) > 100 or len(message) > 1000:
        flash('Input is too long.', 'error')
        return redirect('/')

    # Verify reCAPTCHA
    secret_key = "6Lc_9pIrAAAAA1cdVFw6_E7kTFNJy-4b2g32MM1"
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    response = requests.post(verify_url, data={
        'secret': secret_key,
        'response': recaptcha_response
    })
    result = response.json()

    if not result.get("success"):
        flash('reCAPTCHA verification failed. Try again.', 'error')
        return redirect('/')

    try:
        msg = Message(subject=f"New message from {name}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"From: {name} <{email}>\n\n{message}"
        mail.send(msg)
        flash('Message sent successfully!', 'success')
    except Exception as e:
        print(f"Error sending email: {e}")
        flash('Failed to send message.', 'error')

    return redirect('/')
