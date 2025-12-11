CREATE DATABASE ACTIVATED;
USE ACTIVATED;

-- Athlete Onboarding Info
CREATE TABLE athlete_onboarding (
  onboarding_id INT AUTO_INCREMENT PRIMARY KEY,
  submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  full_legal_name VARCHAR(150),
  preferred_name VARCHAR(100),
  date_of_birth DATE,
  gender VARCHAR(20),
  school_program_name VARCHAR(150),
  graduation_year YEAR,
  height_feet TINYINT,
  height_inches TINYINT,
  weight_lbs DECIMAL(5,2),

  athlete_email VARCHAR(100),
  parent_guardian_names TEXT,
  parent_guardian_email VARCHAR(100),
  parent_phone_number VARCHAR(20),
  athlete_phone_number VARCHAR(20),

  teambuildr_url TEXT,
  output_url TEXT,
  vald_url TEXT,
  myfitnesspal_url TEXT,
  youtube_url TEXT,
  linkedin_url TEXT,

  participation_consent BOOLEAN,
  data_collection_consent BOOLEAN
);

CREATE TABLE counter_movement_jump (
id INT AUTO_INCREMENT PRIMARY KEY,
athlete_id INT NOT NULL,
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
measurement_timestamp DATETIME NULL,
FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id)
);
