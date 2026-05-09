import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Set these in your .env file
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SMTP_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")

def send_reset_email(to_email: str, reset_token: str):
    """
    Sends a password reset link to the specified email address using Gmail's SMTP server.
    """
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "AI Career Assistant - Password Reset Request"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    text = f"You requested a password reset. Click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."
    
    html = f"""
    <html>
      <body>
        <h2>Password Reset Request</h2>
        <p>We received a request to reset your password for the AI Career Assistant.</p>
        <p>Please click the button below to choose a new password:</p>
        <a href="{reset_link}" style="display:inline-block; padding:10px 20px; background-color:#4CAF50; color:white; text-decoration:none; border-radius:5px;">Reset Password</a>
        <br><br>
        <p>Or copy and paste this link into your browser:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <br>
        <p><small>If you did not request this reset, you can safely ignore this email.</small></p>
      </body>
    </html>
    """
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    msg.attach(part1)
    msg.attach(part2)
    
    try:
        # Create secure connection with server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    finally:
        try:
            server.quit()
        except:
            pass
