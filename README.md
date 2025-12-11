#  Output Sports Athlete Performance ETL Pipeline

This project is a complete ETL pipeline that connects to the Output Sports API, retrieves athlete performance data, transforms raw JSON measurements into clean structured fields, and loads the processed results into a MySQL relational database.

The pipeline is designed to support multiple exercise types, but this repository demostrates Counter Movement Jump (CMJ) ETL flow as a representative example. 

##  Project Purpose

Athlete performance data often comes in nested, unstructured API responses that are not ready for analysis or visualization.  
This pipeline solves that problem by:

- Automatically connecting to the Output Sports API  
- Extracting measurements for each athlete  
- Mapping raw JSON metric names to clean SQL column names  
- Storing transformed data in a normalized relational schema  
- Laying the foundation for dashboards, trend analysis, and modeling  

##  Tools & Technologies

Below is a list of tools used for the project:

- Python
- MySQL
- python-dotenv
- JSON
- Output Sports API 

##  API Workflow

The ETL interacts with 3 key endpoints:

1. OAuth Login (`POST /oauth/token`)
2. Athlete Directory (`GET /athletes`)
3. Measurements Endpoint (`POST /exercises/measurements`)

The pipeline loops through each athlete and retrieves all their measurements within a defined date range


##  ETL Flow Diagram

The diagram below show show the flow of the ETL:

   Authenticate via OAuth 
              ↓
    Extract Athlete List   
              ↓
    Extract Measurements   
              ↓
     Transform Raw JSON     
              ↓
       Load into MySQL         


##   Example Raw JSON

The following is a simplified sample of the JSON structure returned by the Output Sports API. Actual data has been anonymized for privacy.

{
"athleteId": 12345,
"exerciseId": "counter_movement_jump",
"metrics": [
{"field": "jumpHeightL", "value": 26.7},
{"field": "jumpHeightR", "value": 27.9},
{"field": "flightTimeL", "value": 0.32},
{"field": "flightTimeR", "value": 0.30},
{"field": "peakPowerL", "value": 3150},
{"field": "peakPowerR", "value": 3305},
{"field": "rsiModifiedL", "value": 0.72},
{"field": "rsiModifiedR", "value": 0.75}
],
"timestamp": "2025-02-14T12:05:00Z"
}


##   Field Mapping

The Output Sports API returns raw metric names that are not SQL-friendly and vary by exercise.

To standardize the data for storage and analysis, the ETL pipeline applies a field mapping layer that converts API fields into clean, descriptive SQL column names.

This transformation ensures:

- Consistent naming conventions
- Readability for analysts
- Query-friendly SQL schema

Below is an example of the mapping dictionary used for Counter Movement Jump (CMJ) metrics:

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

When JSON is returned from the API, each metric appears in the form:

{"field": "jumpHeightL", "value": 27.5}

The ETL pipeline:

- Reads the field key
- Checks if it exists in the field_map
- Converts it to the SQL column name
- Inserts the matching value into the correct MySQL column

This is the Transform stage of the ETL. 


##   SQL Schema


CREATE TABLE athlete_onboarding (
    onboarding_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    date_of_birth DATE,
    sport VARCHAR(100),
    onboarding_date DATE
);

CREATE TABLE counter_movement_jump (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    test_type VARCHAR(50),
    jump_height_cm_l FLOAT,
    jump_height_cm_r FLOAT,
    flight_time_l FLOAT,
    flight_time_r FLOAT,
    take_off_velocity_l FLOAT,
    take_off_velocity_r FLOAT,
    peak_landing_force_l FLOAT,
    peak_landing_force_r FLOAT,
    peak_power_l FLOAT,
    peak_power_r FLOAT,
    rsi_modified_l FLOAT,
    rsi_modified_r FLOAT,
    FOREIGN KEY (user_id) REFERENCES athlete_onboarding(onboarding_id)
);


##   How to Run

1. Install dependencies:

- pip install -r requirements.txt

2. Create a `.env` file:

- OUTPUT_EMAIL=your_email
- OUTPUT_PASSWORD=your_password
- DB_USER=root
- DB_PASSWORD=your_password
- DB_NAME=activated

3. Run the ETL:

- python etl.py


##   What I Learned

- API authentication (OAuth)
- JSON parsing & transformation
- SQL schema design & normalization
- ETL pipeline planning
- Secure credential handling
- Automation of data ingestion

##   Future Improvements

- Automate pipeline using cron/Airflow  
- Add cloud data warehouse integration  
- Build analytics dashboard (Tableau/Power BI)  
