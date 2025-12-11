import mysql.connector
import requests

# Step 1: Set your credentials
API_EMAIL = "your_email@example.com" # Replace this
API_PASSWORD = "your_password_here" # Replace this

# Step 2: Get the access token
def get_access_token():
	url = "https://api.outputsports.com/api/v1/oauth/token"
	payload = {
		"email": "juggernautcaptain23@gmail.com" ,
		"password": "IsahApache25.",
		"grantType": "password"
	}

	try:
		response = requests.post(url, json=payload)
		print("Status Code:", response.status_code)
		print("Raw Response:", response.text)

		if response.status_code != 200:
			print("Login failed. Check credentials or permissions.")
			return None

		data = response.json()
		token = data.get("accessToken")

		if token:
			print("Token received.")
		else:
			print("No token found in the response.")

		return token

	except Exception as e:
		print("Error during login:", str(e))
		return None

# Step 3: Get Athlete IDs
def get_athlete_ids(token):
	url = "https://api.outputsports.com/api/v1/athletes"
	headers = {"Authorization": f"Bearer {token}"}
	response = requests.get(url, headers=headers)
	response.raise_for_status()
	return [athlete["id"] for athlete in response.json()]

# Step 4: Get Measurement Data for Each Athlete
def get_measurements(token, athlete_id):
	url = "https://api.outputsports.com/api/v1/exercises/measurements"
	headers = {
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json"
	}

	print(f"athlete_id value: {athlete_id}, type: {type(athlete_id)}")

	payload = {
		"athleteId": athlete_id,
		"startDate": "2025-02-01",
		"endDate": "2025-03-01"
	}
	
	print("Sending POST to:", url)
	print("Headers:", headers)
	print("Payload:", payload)

	response = requests.post(url, headers=headers, json=payload)
	response.raise_for_status()
	return response.json()

# Step 5: Insert Counter Movement Jump Data into MySQL
def insert_jump_data_if_applicable(measurement, cursor, connection):
	#if measurement["exerciseId"].lower() != "counter_movement_jump":
	#	return

	field_map = {
		"jumpHeightL": "jump_height_cm_l",
		"jumpHeightR": "jump_height_cm_r",
		"flightTimeL": "flight_time_l",
		"flightTimeR": "flight_time_r",
		"takeOffVelocityL": "take_off_velocity_l",
		"takeOffVelocityR": "take_off_velocity_r",
		"peakLandingForceL": "peak_landing_force_l",
		"peakLandingForceR": "peak_landing_force_r",
		"peakPowerL": "peak_power_l",
		"peakPowerR": "peak_power_r",
		"rsiModifiedL": "rsi_modified_l",
		"rsiModifiedR": "rsi_modified_r"
	}

	user_id = measurement["athleteId"]
	test_type = "counter_movement"
	values_dict = {"user_id": user_id, "test_type": test_type}

	for metric in measurement["metrics"]:
		field = metric["field"]
		if field in field_map:
			values_dict[field_map[field]] = metric["value"]

	if len(values_dict) > 2:
		columns = ", ".join(values_dict.keys())
		placeholders = ", ".join(["%s"] * len(values_dict))
		sql = f"INSERT INTO counter_movement_jump ({columns}) VALUES ({placeholders})"
		values = list(values_dict.values())
		cursor.execute(sql, values)
		connection.commit()
		print(f"Instead CMJ data for athlete {user_id}")

# Step 5: Run Entire Script
def main():
	client_id = "your_client_id"
	client_secret = "your_client_secret"

	token = get_access_token()

	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="CGriffin@92.",
		database="activated"
	)
	cursor = db.cursor()

	for athlete_id in get_athlete_ids(token):
		measurements = get_measurements(token, athlete_id)
		for m in measurements:
			insert_jump_data_if_applicable(m, cursor, db)

	cursor.close()
	db.close()

main()