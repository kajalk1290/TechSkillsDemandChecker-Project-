"""
Tech Skills Demand Checker - Flask App with Real Gmail OTP
"""
from flask import Flask, render_template, request, jsonify, session
from tech_skills_scraper import TechSkillsScraper, SKILLS_TO_TRACK
from collections import Counter
import smtplib
import random
import string
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'techskills_secret_2026'  # Session ke liye

# =============================================
# EMAIL CONFIGURATION
# app_config.py file mein apna email daalo!
# =============================================
try:
    from app_config import EMAIL_ADDRESS, EMAIL_PASSWORD
except ImportError:
    EMAIL_ADDRESS  = "your_gmail@gmail.com"
    EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx"

# Check karo email set hua ya nahi
if EMAIL_ADDRESS == "your_gmail@gmail.com":
    print("\n⚠️  WARNING: app_config.py mein apna Gmail set karo!")
    print("⚠️  Tab tak OTP screen pe dikhega (dev mode)\n")

# OTP storage (memory mein - production mein database use karein)
otp_store = {}   # { email: { otp, expires_at } }


# =============================================
# OTP EMAIL SENDER
# =============================================
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp_code, user_name="User"):
    """Gmail SMTP se OTP bhejta hai"""
    try:
        # Email content
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🔐 Your OTP - Tech Skills Demand Checker"
        msg['From']    = EMAIL_ADDRESS
        msg['To']      = to_email

        # Plain text fallback
        text = f"""
Hello {user_name}!

Your OTP for Tech Skills Demand Checker is:

{otp_code}

This OTP is valid for 5 minutes only.
Do not share this with anyone.

- Tech Skills Demand Checker Team
        """

        # HTML email (beautiful)
        html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:500px;margin:40px auto;background:white;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
    
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:35px;text-align:center;">
      <div style="font-size:3em;">🚀</div>
      <h1 style="color:white;margin:10px 0 5px;font-size:1.5em;">Tech Skills Checker</h1>
      <p style="color:rgba(255,255,255,0.85);margin:0;font-size:0.9em;">Password Reset OTP</p>
    </div>
    
    <!-- Body -->
    <div style="padding:35px;">
      <p style="color:#333;font-size:1em;margin-bottom:5px;">Hello <b>{user_name}</b> 👋</p>
      <p style="color:#666;font-size:0.95em;margin-bottom:25px;">
        We received a request to reset your password. Use the OTP below:
      </p>
      
      <!-- OTP Box -->
      <div style="background:linear-gradient(135deg,#f0f3ff,#f5f0ff);border:2px dashed #667eea;border-radius:12px;padding:25px;text-align:center;margin-bottom:25px;">
        <p style="color:#667eea;font-size:0.85em;font-weight:600;margin:0 0 8px;">YOUR ONE-TIME PASSWORD</p>
        <div style="font-size:3em;font-weight:900;letter-spacing:12px;color:#667eea;font-family:monospace;">{otp_code}</div>
        <p style="color:#888;font-size:0.8em;margin:10px 0 0;">⏱️ Valid for <b>5 minutes</b> only</p>
      </div>
      
      <div style="background:#fff8e1;border-left:4px solid #f59e0b;border-radius:4px;padding:12px 15px;margin-bottom:20px;">
        <p style="color:#92400e;font-size:0.85em;margin:0;">
          ⚠️ <b>Security Warning:</b> Never share this OTP with anyone. 
          Our team will never ask for your OTP.
        </p>
      </div>
      
      <p style="color:#888;font-size:0.82em;margin:0;">
        If you didn't request this, please ignore this email. 
        Your account is safe.
      </p>
    </div>
    
    <!-- Footer -->
    <div style="background:#f8f9fa;padding:20px;text-align:center;border-top:1px solid #eee;">
      <p style="color:#aaa;font-size:0.8em;margin:0;">
        © 2026 Tech Skills Demand Checker | Made with ❤️
      </p>
    </div>
  </div>
</body>
</html>
        """

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html,  'html'))

        # Gmail SMTP bhejo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        return True, "OTP sent successfully!"

    except smtplib.SMTPAuthenticationError:
        return False, "Gmail authentication failed. Please check App Password."
    except smtplib.SMTPException as e:
        return False, f"Email sending failed: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"


# =============================================
# API ROUTES
# =============================================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/send-otp', methods=['POST'])
def api_send_otp():
    """OTP generate karke email pe bhejta hai"""
    data = request.get_json()
    email     = data.get('email', '').strip().lower()
    user_name = data.get('name', 'User')

    if not email:
        return jsonify({'success': False, 'error': 'Email required'})

    # OTP generate karo
    otp = generate_otp()

    # Store karo with 5 min expiry
    otp_store[email] = {
        'otp': otp,
        'expires_at': (datetime.now() + timedelta(minutes=5)).isoformat()
    }

    # Email bhejo
    success, message = send_otp_email(email, otp, user_name)

    if success:
        return jsonify({'success': True, 'message': f'OTP sent to {email}'})
    else:
        # Development mode - OTP return karo agar email fail ho
        return jsonify({
            'success': False,
            'error': message,
            'dev_otp': otp  # Sirf development ke liye
        })


@app.route('/api/verify-otp', methods=['POST'])
def api_verify_otp():
    """OTP verify karta hai"""
    data  = request.get_json()
    email = data.get('email', '').strip().lower()
    otp   = data.get('otp', '').strip()

    if email not in otp_store:
        return jsonify({'success': False, 'error': 'No OTP found. Please resend.'})

    stored = otp_store[email]
    expires = datetime.fromisoformat(stored['expires_at'])

    if datetime.now() > expires:
        del otp_store[email]
        return jsonify({'success': False, 'error': 'OTP expired! Please resend.'})

    if otp != stored['otp']:
        return jsonify({'success': False, 'error': 'Incorrect OTP! Please try again.'})

    # Sahi OTP - delete karo
    del otp_store[email]
    return jsonify({'success': True, 'message': 'OTP verified!'})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data   = request.get_json()
        source = data.get('source', 'sample')
        scraper = TechSkillsScraper()
        if source == 'indeed':
            scraper.scrape_indeed_jobs(
                data.get('search_query', 'Python Developer'),
                data.get('location', 'India'),
                int(data.get('num_pages', 3))
            )
        else:
            scraper.scrape_github_jobs()
        top_skills  = scraper.analyze_skills()
        skill_counts = Counter(scraper.all_skills_found)
        return jsonify({
            'success': True,
            'total_jobs': len(scraper.job_titles),
            'total_mentions': len(scraper.all_skills_found),
            'top_skills': [{'skill': s, 'count': c} for s, c in top_skills],
            'all_skills': dict(skill_counts.most_common(15)),
            'job_titles': scraper.job_titles[:10]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Tech Skills Demand Checker")
    print("="*50)
    print(f"📧 Email configured: {EMAIL_ADDRESS}")
    print("🌐 Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
