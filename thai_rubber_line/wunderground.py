import requests


def get_wether_wunderground(apiKey):
    url = f"https://api.weather.com/v2/pws/observations/all/1day?stationId=IMUEAN467&format=json&units=e&apiKey={apiKey}"
    response = requests.get(url)

    # Checking if the request was successful
    if response.status_code == 200:
        # Print response content (JSON or text)
        return response.json()['observations'][-1]
    else:
        print(f"Error: {response.status_code}")
