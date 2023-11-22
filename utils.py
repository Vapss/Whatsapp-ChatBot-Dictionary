from twilio.rest import Client
from dotenv import load_dotenv
import os
import logging

# Load the .env file

load_dotenv()
password = os.getenv("TWILIO_SECRET")
sid = os.getenv("TWILIO_SID")
twilio_number = os.getenv("TWILIO_NUMBER")
to_number = os.getenv("TO_NUMBER")

account_sid = sid
auth_token = password
client = Client(account_sid, auth_token)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=text,
            to=f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

def obtain_definitions_mongo():
    try:
        definitions = dictionary_collection.find()
        logger.info(f"Definitions obtained from MongoDB")
    except Exception as e:
        logger.error(f"Error obtaining definitions from MongoDB: {e}")
    return definitions