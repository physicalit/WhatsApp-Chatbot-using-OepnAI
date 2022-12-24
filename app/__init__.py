"""
WhatsApp_Chatbo
-------

A Python package for interacting with the WhatsApp API and the OpenAI API.

This package contains the following components:

- WhatsAppWrapper: A class for wrapping WhatsApp API interactions
- app: A Flask web application for handling webhook notifications and sending messages

Example:

```python
from mypackage import WhatsAppWrapper

client = WhatsAppWrapper()
client.send_message("Hello World!", "+1234567890")
"""
from .main import app
from .whatsapp_client import WhatsAppWrapper

__all__ = ['app', 'WhatsAppWrapper']