![Habit Tracker Illustration](https://github.com/Tech4Dami/Habit-Tracker-Application/blob/261505721b459b80e99cb23921c1575be0b4ccc4/illustration-shows-woman-using-habit-tracker-app-her-phone-generated-ai-app-features-calendar-interface-374058192.webp?raw=true)

# Habit Tracker Application 

##  Project Overview
#### This is a conceptual habit-tracking application built with Python. It is designed to help individual users define, track, and analyze their personal habits over time. The application provides personalized insights into behavioral consistency and streaks through a secure, user-authenticated command-line interface.

#### The project is structured using object-oriented principles, with dedicated modules for core functionalities such as secure data storage, habit analysis, and user interaction. All data is stored and managed using a local SQLite database.

#### The project is structured using object-oriented principles, with dedicated modules for core functionalities such as data storage, habit analysis, and user interaction. All data is stored and managed using a local SQLite database.

# Core Features 

* User Management: Register new accounts, sign in securely with a unique username and password, and delete your account and all associated data.


* Habit Definition: Create habits with specific periodicities (daily or weekly).



*  Completion Tracking: Log completions for your habits with a timestamp.


*  Data Analysis: The application can calculate and display personalized analytics, including:


* The longest streak for any single habit.


* The overall longest streak across all habits.

* Lists of all active habits.


* Habits that were missed in the last week.

## Installation 

#### To set up the project and install all required dependencies, navigate to the project directory in your terminal and run the following command:
***
### pip install -r requirements.txt
***

## Usage

#### Upon startup, you will be prompted to either Register as a new user or Sign In to an existing account to begin tracking your habits. 
***
### python main.py
***
### Upon startup, you will be prompted to choose a mode:
### 
* Run the interactive application:This mode allows you to create new habits, log completions, and analyze your data.


* Populate database with simple habits: This option is for initial testing. It creates 50 habits with a simple, continuous completion history.


* Populate database with complex, realistic test data: This is the recommended option for comprehensive testing. It populates the database with up to 1000 habits that have varied and realistic completion histories, including missed periods.


* And follow instruction on screen.

## Testing

#### This project includes a comprehensive test suite using pytest. To run the tests and verify that all functionalities are working as expected, use the following command in your terminal:

***
### pytest
*** 

#### A successful test run will show a summary of all tests that have passed. If any tests fail, pytest will provide detailed error messages to help you with debugging.
