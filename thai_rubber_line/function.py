def check_have_weather_station(mycursor, user_id):
    mycursor.execute("USE thai_rubber")
    mycursor.execute(
        "SELECT weather_station, weather_serial FROM plantation WHERE id = %s", (user_id,))
    result = mycursor.fetchone()
    return result