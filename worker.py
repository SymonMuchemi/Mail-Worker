import time, redis, os
import ssl, smtplib
from dotenv import load_dotenv
from logger import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# create redis client
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)

STREAM_NAME = os.getenv("STREAM_NAME")
GROUP_NAME = os.getenv("GROUP_NAME")
CONSUMER_NAME = os.getenv("CONSUMER_NAME")

SENDER_EMAIL = os.getenv("GMAIL_USERNAME")
PASSWORD = os.getenv("GMAIL_PWD")
GMAIL_HOST = os.getenv("GMAIL_HOST")
PORT = os.getenv("PORT")


# Create consumer group
try:
    redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, id="0", mkstream=True)
except Exception as e:
    pass


def send_email(address, subject, body) -> None:
    msg = MIMEMultipart()
    msg["from"] = SENDER_EMAIL
    msg["to"] = address
    msg["subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(GMAIL_HOST, port=PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, address, msg.as_string())

        logger.info(f"Email sent to {address} successfully!")


while True:
    try:
        messages = redis_client.xreadgroup(
            GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: ">"}, count=1, block=5000
        )

        if not messages:
            time.sleep(3)

        if messages:
            for stream, msg_list in messages:
                for msg_id, msg in msg_list:
                    logger.info(f'Processing message: {msg_id}, email: {msg["email"]}')
                    redis_client.xack(STREAM_NAME, GROUP_NAME, msg_id)
    except Exception as e:
        logger.error(f"Error reading message: {e}")
        exit(100)
