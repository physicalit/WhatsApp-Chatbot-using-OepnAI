import os
from flask import Flask, jsonify, request
from app.whatsapp_client import WhatsAppWrapper

app = Flask(__name__)

# Get the verify token from environment variables
VERIFY_TOKEN = os.environ.get('WHATSAPP_HOOK_TOKEN')

@app.route("/")
def hello_world():
    """
    A simple endpoint that returns a message.
    """
    return "Hello World!"

@app.route("/send_message/", methods=["POST"])
def send_template_message():
    """
    Endpoint for sending a template message to a phone number.
    """
    # Check if request body is present
    if not request.json:
        return jsonify({"error": "Missing request body"}), 400

    # Check if body and phone_number fields are present in the request body
    if "body" not in request.json:
        return jsonify({"error": "Missing message"}), 400
    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    # Send the template message using the WhatsApp client
    client = WhatsAppWrapper()
    send_response = client.send_template_message(
        body=request.json["body"],
        phone_number=request.json["phone_number"],
    )

    # Return success status and the send response
    return jsonify({"status": "success", "data": send_response}), 200

@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    """
    Endpoint for processing webhook notifications from WhatsApp.
    """
    # Handle GET request for verifying the webhook
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Authentication failed. Invalid Token."

    # Check if request body is present
    if not request.json:
        return jsonify({"error": "Missing request body"}), 400

    # Process the webhook notification using the WhatsApp client
    client = WhatsAppWrapper()
    client.process_webhook_notification(request.get_json())

    # Return success status
    return jsonify({"status": "success"}), 200
