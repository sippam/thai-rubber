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

items = [
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023273/kaito_crdd00.jpg",
        "name": "เชื้อราไตรโคเดอร์มา",
        "price": "195",
        "market": "shopee / Lazada"
    },
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023273/white_rtayxe.jpg",
        "name": "ปูนขาว",
        "price": "195",
        "market": "shopee / Lazada / ร้านพันทวี"
    },
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023274/doromai_ylwo39.png",
        "name": "โดโลไมท์",
        "price": "195",
        "market": "บริษัททีพีไอ โพลีน จํากัด (มหาชน)"
    },
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023273/yuria_xvzgt8.jpg",
        "name": "ยูเรีย",
        "price": "195",
        "market": "shopee / Lazada"
    },
    #   ราแป้ง
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023274/benomyl_klgptd.jpg",
        "name": "Benomyl 50% WP",
        "price": "200",
        "market": "ร้านขายเคมีเกษตร / Shopee / Lazada"
    },
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023273/carbendazim_otkw2p.jpg",
        "name": "Carbendazim 50% WP",
        "price": "299 / ลิตร",
        "market": "ร้านขายเคมีเกษตร / Shopee / Lazada"
    },
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023273/cyproconazole_u5ovgy.jpg",
        "name": "Cyproconazole 10% SL",
        "price": "235 / 100 cc",
        "market": "ร้านขายเคมีเกษตร / Shopee / Lazada"
    },
    {
        "url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1737023273/hexaconazole_q0ac1p.jpg",
        "name": "Hexaconazole 5% SC",
        "price": "130 บาท / ลิตร ",
        "market": "ร้านขายเคมีเกษตร / Shopee / Lazada"
    },
]

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

items_template = """
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
                "type": "text",
                "text": "ราคา %s บาท",
                "size": "md"
            },
            {
                "type": "text",
                "text": "ซื้อได้ที่ %s",
                "size": "md"
            }
        ]
    }
}
"""


def flex_message_function(uid, items_array, predicted_class):

    with open('test.json', 'r', encoding='utf-8') as file:
        data_json = json.load(file)

    bubbles = [
        # Replace placeholders
        json.loads(bubble_template % (item['img_url'], item['header'], item['action'])) for item in items_array
    ]

    bubbles_items = [
        # Replace placeholders
        json.loads(items_template % (item['url'], item['name'], item['price'], item['market'])) for item in items
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
        # Use Bearer Authorization
        'Authorization': f'Bearer {channel_access_token}'
    }

    response = requests.post(url, headers=headers,
                             data=json.dumps(flex_message))

    # Final Flex Message template
    flex_message = {
        "to": user_id,
        "messages": [
            {
                "type": "flex",
                "altText": "ข้อมูลโรค",
                "contents": {
                    "type": "carousel",
                    "contents": bubbles_items
                }
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        # Use Bearer Authorization
        'Authorization': f'Bearer {channel_access_token}'
    }

    response = requests.post(url, headers=headers,
                             data=json.dumps(flex_message))
