"""
Email Test Script - Chalao aur dekho kya problem hai!
Run: python test_email.py
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("="*50)
print("📧 EMAIL TEST SCRIPT")
print("="*50)

# ==========================================
# ⬇️  YAHAN APNA EMAIL AUR PASSWORD DAALO
# ==========================================
EMAIL_ADDRESS  = input("\n📧 Apna Gmail enter karo: ").strip()
EMAIL_PASSWORD = input("🔑 App Password enter karo (16 digit): ").strip()
TEST_TO        = input("📬 OTP kis email pe bhejni hai: ").strip()
# ==========================================

print("\n⏳ Email bhej raha hun...")

try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "✅ Test OTP - Tech Skills Checker"
    msg['From']    = EMAIL_ADDRESS
    msg['To']      = TEST_TO

    html = """
    <div style="font-family:sans-serif;max-width:400px;margin:auto;padding:30px;background:#f0f3ff;border-radius:12px;">
        <h2 style="color:#667eea;text-align:center;">🚀 Tech Skills Checker</h2>
        <p style="text-align:center;">Your Test OTP is:</p>
        <div style="font-size:3em;font-weight:900;letter-spacing:10px;color:#667eea;text-align:center;font-family:monospace;">
            123456
        </div>
        <p style="color:#888;text-align:center;font-size:0.85em;">Email is working! ✅</p>
    </div>
    """

    msg.attach(MIMEText("Your Test OTP: 123456", 'plain'))
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TEST_TO, msg.as_string())

    print("\n✅✅✅ EMAIL SUCCESSFULLY SENT! ✅✅✅")
    print(f"📬 Check karo: {TEST_TO}")
    print("(Spam folder bhi check karo!)")
    print("\nAb app.py mein same credentials daalo!")

except smtplib.SMTPAuthenticationError:
    print("\n❌ AUTHENTICATION ERROR!")
    print("Fix: App Password galat hai.")
    print("\nSahi App Password kaise banaye:")
    print("1. myaccount.google.com kholo")
    print("2. Security → 2-Step Verification ON karo")
    print('3. Search "App passwords"')
    print("4. Mail + Windows → Generate")
    print("5. 16-digit code milega - woh daalo")

except smtplib.SMTPException as e:
    print(f"\n❌ SMTP ERROR: {e}")
    print("Fix: Internet connection check karo")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("Fix: Email address sahi format mein daalo (xxx@gmail.com)")

print("\n" + "="*50)
input("Press Enter to exit...")
