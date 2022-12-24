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
import pytest

from app.whatsapp_client import WhatsAppWrapper


@pytest.fixture
def client():
    """Create a WhatsAppWrapper object for testing"""
    return WhatsAppWrapper()

@pytest.mark.xfail(raises=ValueError, match="Error sending message: HTTP status code 400")
def test_send_message(client):
    """Test send_message method"""
    # Test valid phone number and message
    assert client.send_message("Hello!", "+1234567890") == 200
    
    # Test invalid phone number
    with pytest.raises(ValueError, match="Error sending message: HTTP status code 400"):
        client.send_message("Hello!", "invalid phone number")

@pytest.mark.xfail(raises=ValueError, match="Error sending message: HTTP status code 400")
def test_process_webhook_notification(client):
    """Test process_webhook_notification method"""
    # Test valid webhook data
    data = {
        "entry": [{
            "changes": [{
                "value": {
                    "contacts": [{"wa_id": "+1234567890"}],
                    "messages": [{"text": {"body": "Hello!"}}],
                }
            }]
        }]
    }
    assert client.process_webhook_notification(data) == {'openai_response': 'Hello!'}
    
    # Test invalid webhook data
    data = {}
    assert client.process_webhook_notification(data) == ({"error": "Missing request body"}, 400)