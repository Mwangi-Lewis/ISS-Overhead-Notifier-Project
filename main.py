import requests
from datetime import datetime
import smtplib
import time
MY_LAT = -1.743340  # Your latitude
MY_LONG = 37.018290  # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.
def check_iss_proximity(my_lat, my_long):
    """
    Check if the ISS is within +5 or -5 degrees of the given position.
    """
    # ISS API call
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if the distance is within +5 or -5 degrees
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False


# Check proximity
is_near_iss = check_iss_proximity(MY_LAT, MY_LONG)
if is_near_iss:
    print("You are within +5 or -5 degrees of the ISS position.")
else:
    print("You are not within +5 or -5 degrees of the ISS position.")

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

# If the ISS is close to my current position
# and it is currently dark
def is_dark():
    try:
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
        # Get the current hour
        current_hour = datetime.now().hour

        # Check if the current hour is after sunset or before sunrise
        if current_hour >= sunset or current_hour < sunrise:
            return True
        else:
            return False
    except requests.RequestException as e:
        # Handle request exceptions
        print("Error fetching sunrise and sunset times:", e)
        return None
    except KeyError as e:
        # Handle missing or incorrect data keys
        print("Error parsing sunrise and sunset times:", e)
        return None
    except Exception as e:
        # Handle other unexpected errors
        print("An unexpected error occurred:", e)
        return None

is_dark_result = is_dark()
print(is_dark_result)

# Then email me to tell me to look up.
def send_email():
    """
    Send an email notification.
    """
    # Email configuration
    sender_email = "PUT SENDER EMAIL"
    receiver_email = "PUT RECEIVER EMAIL"
    password = "YOUR PASSWORD"

    # SMTP server configuration (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # For starttls

    # Create a secure SSL connection
    connection = smtplib.SMTP(smtp_server, smtp_port)
    connection.starttls()

    # Login to the email server
    connection.login(sender_email, password)

    # Email content
    subject = "Subject: Go outside and look up!\n"
    body = "The ISS is nearby, and it's dark outside. Go outside and look up to see it!"

    # Construct the email message
    message = subject + body

    # Send the email
    connection.sendmail(sender_email, receiver_email, message)

    # Close the SMTP connection
    connection.close()

# Your latitude and longitude
MY_LAT = -1.743340
MY_LONG = 37.018290

# ISS API call for sunrise and sunset times
response = requests.get(url="https://api.sunrise-sunset.org/json?lat=-1.743340&lng=37.018290")
response.raise_for_status()
data = response.json()

# Extract sunrise and sunset times
try:
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
except IndexError:
    # Handle the case where the expected data structure is not found
    print("Error: Unable to extract sunrise and sunset times.")
    # Provide default values or handle the error as needed
    sunrise = 6  # Default sunrise hour
    sunset = 18  # Default sunset hour

while True:
    if check_iss_proximity(MY_LAT, MY_LONG) and is_dark():
        send_email()
        print("Email sent!")
    else:
        print("No need to send email.")
    # BONUS: run the code every 60 seconds.
    # Check every hour
    time.sleep(3600)  # Sleep for 1 hour

