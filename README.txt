STUDYBOT
========
A command-line tool to track your study sessions using Firebase.

---

REQUIREMENTS
1. Python 3.8 or higher
2. Firebase project and service account JSON key
3. Installed packages from requirements.txt

---

SETUP
1. Clone or download the repository.
2. Open a terminal in the project folder.
3. Create a virtual environment:
   Windows:
       python -m venv venv
   macOS/Linux:
       python3 -m venv venv
4. Activate the virtual environment:
   Windows:
       venv\Scripts\activate
   macOS/Linux:
       source venv/bin/activate
5. Install dependencies:
       pip install -r requirements.txt

---

FIREBASE SETUP
1. In the Firebase console, go to:
       Project Settings → Service Accounts → Generate New Private Key
2. Download the JSON key file.
3. Place the file in the project folder (e.g., `serviceAccount.json`).
4. Set the environment variable:
   Windows:
       set GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json
   macOS/Linux:
       export GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json

---

USAGE
Run the program:
   python main.py

When prompted:
- Type your name and choose a username.
- Commands inside the app:
   start  → Start a study session
   end    → End the current study session
   stats  → View statistics and charts
   quit   → Exit the program

---

NOTES
- The `.gitignore` already hides secrets (JSON keys) and virtual environment folders.
- Do NOT upload your Firebase JSON key to GitHub.
