import os
from datetime import datetime, timedelta, timezone

import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import matplotlib.pyplot as plt

cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path or not os.path.exists(cred_path):
    raise RuntimeError(
        "Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to your Firebase service account JSON file path."
    )
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

name = ""
username = ""

def start():
    global username, name
    collections = list(db.collections())
    existing_users = [c.id for c in collections]

    name = input("Enter your Name\n   ").strip()
    username = input("Choose your Username\n   ").strip()

    if username in existing_users:
        print("You are logged in!")
    else:
        print("Your account has been created")
        print("Configure your subjects")
        subjects = config()
        db.collection(username).document("Initial").set({
            "name": name,
            "subjects": subjects,
            "sessions": 0,
        })

    print(f"Welcome {name}!")
    print("Type 'start' to start a session, 'end' to end a session, 'stats' to display your statistics, or 'quit' to exit")

    x = input("   ").strip().lower()
    if x == "start":
        start_session()
    elif x == "end":
        end_session()
    elif x == "stats":
        print("Displaying your statistics...")
        display_stats()
        print("Generating DataFrame and plots...")
        df = get_sessions_df()
        print(df)
        plot_weekly_study_time()
        plot_subject_pie_chart()
    elif x == "quit":
        print("Goodbye!")
    else:
        print("Invalid command. Please type 'start', 'end', 'stats', or 'quit'.")

def config():
    subjects = []
    while True:
        x = input("Type a subject (type 'stop' to finish)\n").strip()
        if x.lower() == "stop":
            break
        if x:
            subjects.append(x)
            print("Your Subjects:", ", ".join(subjects))
            print()
    return subjects

def start_session():
    global username
    data = db.collection(username).document("Initial").get().to_dict() or {}
    subjects = data.get('subjects', [])
    n = data.get('sessions', 0)

    if not subjects:
        print("No subjects found. Run config first.")
        return

    for i, s in enumerate(subjects):
        print(f"   [{i}] {s}")
    try:
        x = int(input("Select subject number: ").strip())
        subj = subjects[x]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    db.collection(username).document("StudySessions").collection(subj).document(str(n + 1)).set({
        "start": datetime.now(timezone.utc),
        "end": None,
        "duration": 0
    })
    db.collection(username).document("Initial").set({"sessions": n + 1}, merge=True)
    print(f"Started session {n+1} for {subj}.")

def end_session():
    global username
    data = db.collection(username).document("Initial").get().to_dict() or {}
    subjects = data.get('subjects', [])

    if not subjects:
        print("No subjects found.")
        return

    for i, s in enumerate(subjects):
        print(f"   [{i}] {s}")
    try:
        x = int(input("Select subject number: ").strip())
        subj = subjects[x]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Get the latest few sessions; close the most recent one that has end == None
    sessions = (db.collection(username)
                  .document("StudySessions")
                  .collection(subj)
                  .order_by("start", direction=firestore.Query.DESCENDING)
                  .limit(5)
                  .stream())

    target = None
    for d in sessions:
        if d.to_dict().get("end") is None:
            target = d
            break

    if not target:
        print(f"No open session found for {subj}.")
        return

    now = datetime.now(timezone.utc)
    start_time = target.to_dict().get("start")
    duration_min = round((now - start_time).total_seconds() / 60) if start_time else 0

    target.reference.update({"end": now, "duration": duration_min})
    print(f"Ended session {target.id} for {subj}: {duration_min} min.")

def calculate_duration(subj, n):
    t = db.collection(username).document("StudySessions").collection(subj).document(n).get()
    t = t.to_dict()
    start_time = t.get('start')
    end_time = t.get('end')
    if start_time and end_time:
        duration = end_time - start_time
        db.collection(username).document("StudySessions").collection(subj).document(n).update({
            "duration": round(duration.total_seconds() / 60)
        })

def display_stats():
    data = db.collection(username).document("Initial").get().to_dict()
    subjects = data.get('subjects', [])
    n = data.get('sessions', 0)

    print("Your Statistics:")
    for subj in subjects:
        print(f"Subject: {subj}")
        for j in range(1, n + 1):
            session = db.collection(username).document("StudySessions").collection(subj).document(str(j)).get()
            if session.exists:
                sd = session.to_dict()
                print(f"   Session {j}: Start: {sd.get('start')}, End: {sd.get('end')}, Duration: {sd.get('duration', 0)} minutes")
        print()

def get_sessions_df():
    data = db.collection(username).document("Initial").get().to_dict()
    subjects = data.get('subjects', [])
    n_sessions = data.get('sessions', 0)
    records = []

    for subj in subjects:
        for j in range(1, n_sessions + 1):
            session = db.collection(username).document("StudySessions").collection(subj).document(str(j)).get()
            if session.exists:
                sd = session.to_dict()
                start_time = sd.get('start')
                end_time = sd.get('end')
                duration = sd.get('duration', 0)
                date = start_time.date() if start_time else None
                records.append({
                    "subject": subj,
                    "session": j,
                    "start": start_time,
                    "end": end_time,
                    "duration": duration,
                    "date": date
                })

    return pd.DataFrame(records)

def plot_weekly_study_time():
    df = get_sessions_df()
    if df.empty:
        print("No study sessions found.")
        return
    df['date'] = pd.to_datetime(df['date'])
    last_week = pd.Timestamp.now() - pd.Timedelta(days=7)
    week_df = df[df['date'] >= last_week]
    if week_df.empty:
        print("No study sessions in the last week.")
        return
    daily = week_df.groupby(week_df['date'].dt.date)['duration'].sum().reset_index()
    plt.bar(daily['date'].astype(str), daily['duration'])
    plt.title("Study Time in the Past Week (minutes)")
    plt.xlabel("Date")
    plt.ylabel("Total Minutes Studied")
    plt.show()


def plot_subject_pie_chart():
    df = get_sessions_df()
    if df.empty:
        print("No study sessions found.")
        return
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0)
    totals = df.groupby('subject', as_index=False)['duration'].sum()
    if totals['duration'].sum() == 0:
        print("No durations recorded yet.")
        return
    plt.pie(totals['duration'], labels=totals['subject'], autopct='%1.1f%%', startangle=140)
    plt.title("Study Time by Subject")
    plt.axis('equal')
    plt.show()

start()
