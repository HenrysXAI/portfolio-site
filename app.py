from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Set in Render
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Set in Render
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    try:
        msg = Message(f'New message from {name}', recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"From: {name} <{email}>\n\n{message}"
        mail.send(msg)
        flash('Message sent successfully!', 'success')
    except Exception as e:
        print(str(e))
        flash('Failed to send message.', 'error')

    return redirect(url_for('index'))
