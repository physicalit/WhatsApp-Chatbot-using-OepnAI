#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2022 Mihuleac Sergiu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
import openai
import logging
import requests
from flask import jsonify
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

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

    def send_message(self, body, phone_number):
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
        if response.status_code in (400, 401, 404, 500):
            raise ValueError(f"Error sending message: HTTP status code {response.status_code}")
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

        # Get phone number and message from response
        try:
            entry = data["entry"][0]["changes"][0]["value"]
            telefon = entry["contacts"][0]["wa_id"]
            reply = entry["messages"][0]["text"]["body"]
        except:
            logger.warning("Could not read callback. Object has changed")
            return jsonify({"error": "Missing request body"}), 400
        
        # Check if user reply is "reset"
        if reply == "reset":
            # Delete db.json file
            os.remove("db.json")
            # Clear conversation thread
            self.thread = []
            # Send message to user indicating that the file has been deleted
            self.send_message("The conversation has been reset.", telefon)
            return jsonify({"status": "success"}), 200

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
        self.send_message(
            response["choices"][0]["text"].split("\nSimon: ")[-1], telefon
            )
        return jsonify({"status": "success"}), 200
