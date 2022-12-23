import os
import requests
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class WhatsAppWrapper:
    """Class for wrapping WhatsApp API interactions"""

    # URL for WhatsApp API
    API_URL = "https://graph.facebook.com/v15.0/"

    def __init__(self):
        """Initialize WhatsAppWrapper with necessary headers and API URL"""
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('WHATSAPP_API_TOKEN')}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + os.environ.get("WHATSAPP_NUMBER_ID")
        self.thread = []

    def send_template_message(self, body, phone_number):
        """Send a text message to the specified phone number using WhatsApp API

        Args:
        - body (str): The message to be sent
        - phone_number (str): The phone number to send the message to

        Returns:
        - status_code (int): The HTTP status code of the API response
        """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": body}
        })

        # Send message using WhatsApp API
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        # Check if request was successful
        assert response.status_code == 200, "Error sending message"
        return response.status_code

    def process_webhook_notification(self, data):
        """Process a webhook notification from the WhatsApp API

        Args:
        - data (dict): The data payload of the webhook notification

        Returns:
        - response (dict): The response from the OpenAI API
        """
        # Load previous conversation from file
        if os.path.isfile("db.json"):
            with open("db.json", 'r') as f:
                self.thread = json.load(f)

        response = []

        # Extract relevant information from webhook data
        for entry in data["entry"]:
            for change in entry["changes"]:
                response.append(
                    {
                        "type": change["field"],
                        "from": change["value"]["metadata"]["display_phone_number"],
                        "body": change["value"],
                    }
                )

        # Get phone number and message from response
        try:
            telefon = response[0]["body"]["contacts"][0]["wa_id"]
            reply = response[0]["body"]["messages"][0]["text"]["body"]
        except:
            print("Could not read callback. Object has changed")
            return response
        
        # Check if user reply is "reset"
        if reply == "reset":
            # Delete db.json file
            os.remove("db.json")
            # Clear conversation thread
            self.thread = []
            # Send message to user indicating that the file has been deleted
            self.send_template_message("The conversation has been reset.", telefon)
            return

        # Add human message to conversation thread
        self.thread.append(f"\nHuman: {reply}")

        # Build conversation string
        if len(self.thread) > 0:
            msg = " ".join(self.thread)
        else:
            msg = f"\nHuman: {reply}"

        # Build prompt for OpenAI API
        data = (
            "The following is a conversation with my best friend named Simon. He is the most inteligent person, "
            "is creative, clever, and very friendly, but his atitude is a little bit sarcastig and knows good jokes.\n"
            f"{msg}"
        )
        
        # Generate response from OpenAI API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=data,
            temperature=0.9,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " Simon:"]
        )
        
        # Add Simon's response to conversation thread
        self.thread.append(response["choices"][0]["text"])

        # Limit length of conversation thread to the last 30 messages
        if len(self.thread) < 40:
            self.thread = self.thread[-30:]

        # Save conversation thread to file
        with open("db.json", 'w') as f:
            json.dump(self.thread, f, indent=2)

        # Send Simon's response to phone number using WhatsApp API
        self.send_template_message(
            response["choices"][0]["text"].split("\nSimon: ")[-1], telefon
            )
        return response
