import os
import smtplib
from email.mime.text import MIMEText

def send_alert_email(receiver: str, subject: str, body: str):
    """설정된 환경 변수를 사용하여 이메일 알림을 보냅니다."""
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")
    
    if not sender or not password:
        return "❌ 이메일 발신 정보가 누락되었습니다."

    msg = MIMEText(body)
    msg['Subject'], msg['From'], msg['To'] = subject, sender, receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    return "✅ 이메일 발송 성공"