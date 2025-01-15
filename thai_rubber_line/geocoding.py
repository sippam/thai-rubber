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
            print("result", result)
            address_components = result['address_components']

            province = ""
            district = ""
            subdistrict = ""

            for component in address_components:
                if 'administrative_area_level_1' in component['types']:
                    province = component['long_name']
                if 'administrative_area_level_2' in component['types']:
                    district = component['long_name']
                if 'locality' in component['types']:
                    subdistrict = component['long_name']

            if province == "" or district == "" or subdistrict == "":
                return {"status": 500, "error": "Cannot find the address"}
            else:
                return {
                    "status": 200,
                    "formatted_address": result['formatted_address'],
                    "latitude": result['geometry']['location']['lat'],
                    "longitude": result['geometry']['location']['lng'],
                    "province": province,
                    "district": district,
                    "subdistrict": subdistrict
                }
        else:
            return {"error": data['status']}
    else:
        return {"error": f"HTTP error {response.status_code}"}
