import requests
import os
import dotenv

dotenv.load_dotenv()


def get_geocode(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": os.getenv('GEO_API')
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            result = data['results'][0]
            return {
                "formatted_address": result['formatted_address'],
                "latitude": result['geometry']['location']['lat'],
                "longitude": result['geometry']['location']['lng']
            }
        else:
            return {"error": data['status']}
    else:
        return {"error": f"HTTP error {response.status_code}"}
