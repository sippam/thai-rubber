import json
import requests
import os
import dotenv

dotenv.load_dotenv()
# LINE API Endpoint
url = 'https://api.line.me/v2/bot/message/push'

# Replace with your Channel Access Token
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# Example data as a dictionary

data_json = {}

bubble_template = """
{
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "%s",
        "size": "md",
        "aspectRatio": "20:13",
        "aspectMode": "fit",
        "action": {
            "type": "uri",
            "uri": "https://line.me/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "%s",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "ดูรายละเอียดเพิ่มเติม",
                    "text": "%s"
                }
            }
        ]
    }
}
"""

def flex_message_function(uid, items_array, predicted_class):

    with open('test.json', 'r', encoding='utf-8') as file:
        data_json = json.load(file)
        
    bubbles = [
        json.loads(bubble_template % (item['img_url'], item['header'], item['action']))  # Replace placeholders
        for item in items_array
    ]

    user_id = uid

    # Final Flex Message template
    flex_message = {
        "to": user_id,
        "messages": [
            {
                "type": "flex",
                "altText": "ข้อมูลโรค",
                "contents": {
                    "type": "carousel",
                    "contents": bubbles
                }
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'  # Use Bearer Authorization
    }

    response = requests.post(url, headers=headers, data=json.dumps(flex_message))