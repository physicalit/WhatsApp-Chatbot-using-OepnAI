# WhatsApp Chatbot using OepnAI [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fphysicalit%2FWhatsApp-Chatbot-using-OepnAI.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fphysicalit%2FWhatsApp-Chatbot-using-OepnAI?ref=badge_shield)
This is a Python wrapper for interacting with the WhatsApp API. It includes a class for sending template messages and handling webhook notifications from the WhatsApp API.

## Prerequisites
* Python 3.6 or later
* OpenAI API key
* WhatsApp API token and number ID
## Installation
1. Clone the repository:
```
git clone https://github.com/your-username/whatsapp-api-wrapper.git
```
2. Install the required libraries:
```
pip install -r requirements.txt
```
3. Set the necessary environment variables:
* OPENAI_API_KEY: Your OpenAI API key
* WHATSAPP_API_TOKEN: Your WhatsApp API token
* WHATSAPP_NUMBER_ID: Your WhatsApp number ID

### Deploying to Heroku
1. Create a new Heroku app.
2. Connect the app to your repository.
3. Set the necessary environment variables in the Heroku app's "Settings" > "Config Vars" section.
4. Deploy the app by clicking the "Deploy" button in the "Deploy" tab.
## Usage
### Sending a template message
Use the `/send_message/` endpoint to send a template message to a phone number:
```
curl -X POST \
  http://localhost:5000/send_message/ \
  -H 'Content-Type: application/json' \
  -d '{
    "body": "Hello World!",
    "phone_number": "40762296614"
}'
```
### Processing a webhook notification
Use the /webhook/ endpoint to process a webhook notification from the WhatsApp API:
```
curl -X POST \
  http://localhost:5000/webhook/ \
  -H 'Content-Type: application/json' \
  -d '{
        data = {
        "entry": [{
            "changes": [{
                "value": {
                    "contacts": [{"wa_id": "1234567890"}],
                    "messages": [{"text": {"body": "Hello"}}]
                }
            }]
        }]
    }
}'
```
### To deploy the app to Heroku, you can follow these steps:

1. Install the Heroku CLI and log in to your account.
```
heroku login
```
2. Create a new Heroku app:
```
heroku create app-name
```
3. Set the necessary environment variables in the Heroku app:
```
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set WHATSAPP_API_TOKEN=your_whatsapp_api_token
heroku config:set WHATSAPP_NUMBER_ID=your_whatsapp_number_id
heroku config:set WHATSAPP_HOOK_TOKEN=some generated token
```
4. Deploy the app to Heroku:
```
git push heroku master:main
```

### To deploy the app with docker, you can follow these steps:
To build a Docker image from this Dockerfile, run the following command:
```
docker build -t openai-whatsapp-bot:latest .
```
To start a container from the image, run the following command:
```
docker run -p 5000:5000 \
           -e OPENAI_API_KEY=your_openai_api_key \
           -e WHATSAPP_API_TOKEN=your_whatsapp_api_token \
           -e WHATSAPP_NUMBER_ID=your_whatsapp_number_id \
           -e WHATSAPP_HOOK_TOKEN=some_generated_token \
           openai-whatsapp-bot:latest
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.
