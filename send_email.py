from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Email configuration (use your Gmail or SMTP details)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"  # ← UPDATE THIS
SENDER_PASSWORD = "your-app-password"  # ← UPDATE THIS (use App Password, not regular password)
RECIPIENT_EMAIL = "Sidhhibagdane@gmail.com"

@app.route('/api/consultation', methods=['POST'])
def send_consultation():
    try:
        data = request.json
        
        # Extract form data
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')
        
        # Email subject and body
        subject = f"New Consultation Request from {name}"
        
        body = f"""
        <h2>New Consultation Request</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Message:</strong></p>
        <p>{message}</p>
        <hr>
        <p><em>This person would like to schedule a consultation. Please contact them at your earliest convenience.</em></p>
        """
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        
        part = MIMEText(body, 'html')
        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        
        return jsonify({'success': True, 'message': 'Email sent successfully'}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
