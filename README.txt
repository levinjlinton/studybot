# StudyBot

StudyBot is a Python-based tool to track study sessions using Firebase Firestore. 
It logs session start and end times, subjects, and generates study statistics and charts.

## Features
- Create an account and configure study subjects.
- Start and stop study sessions with automatic time tracking.
- View study statistics and trends.
- Generate weekly and subject-wise charts.

## Requirements
- Python 3.8 or later
- Firebase Firestore
- Dependencies listed in requirements.txt

## Installation
1. Clone the repository:
   git clone https://github.com/levinjlinton/studybot.git
   cd studybot

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate     # macOS/Linux
   venv\Scripts\activate        # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Set up Firebase:
   - Create a Firebase project and enable Firestore.
   - Download your Firebase service account key JSON file.
   - Keep the file private and set the environment variable:
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/serviceAccountKey.json"
     (Use 'set' instead of 'export' on Windows.)

## Usage
Run the program:
   python main.py

Available commands:
- start — begin a study session
- end — stop the current session
- stats — display statistics and generate charts
- quit — exit the program

## Notes
- DONT commit your Firebase service account key to GitHub.
- Add it and your venv folder to .gitignore.
