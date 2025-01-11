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
            
            reverse_geocode(os.getenv('GEO_API'), result['geometry']['location']['lat'], result['geometry']['location']['lng'])
            return {
                "formatted_address": result['formatted_address'],
                "latitude": result['geometry']['location']['lat'],
                "longitude": result['geometry']['location']['lng']
            }
        else:
            return {"error": data['status']}
    else:
        return {"error": f"HTTP error {response.status_code}"}

def reverse_geocode(api_key, lat, lng):
    # สร้าง URL ของคำขอ
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": api_key
    }
    
    # ส่งคำขอไปยัง API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # ดึง address_components จากผลลัพธ์แรก
             print("kuyyyyyyyyyyyyyyyyyyyyyy", data["results"][0])
        else:
            return f"Error: {data['status']}"
    else:
        return f"HTTP Error: {response.status_code}"
