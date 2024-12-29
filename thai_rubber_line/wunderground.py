import requests


def get_wether_wunderground(apiKey):
    url = f"https://api.weather.com/v2/pws/observations/current?stationId=KMAHANOV10&format=json&units=e&apiKey={apiKey}"
    response = requests.get(url)

    # Checking if the request was successful
    if response.status_code == 200:
        # Print response content (JSON or text)
        print(response.json()['observations'][0])  # If response is JSON
    else:
        print(f"Error: {response.status_code}")
