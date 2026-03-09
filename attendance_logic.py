import cv2
import sqlite3
import os
from datetime import datetime

# 1. Database Initialization for Attendance Tracking
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    # Creating attendance table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (name TEXT, date TEXT, time TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# 2. Function to Mark Attendance with Duplicate Entry Prevention
def mark_attendance(name):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Check if the student is already marked present for the current day
    c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date_str))
    result = c.fetchone()

    if result is None:
        c.execute("INSERT INTO attendance (name, date, time, status) VALUES (?, ?, ?, ?)", 
                  (name, date_str, time_str, 'Present'))
        conn.commit()
        print(f"Success: Attendance marked for {name} at {time_str}")
    else:
        print(f"Info: {name} is already marked Present for today.")
    
    conn.close()

# 3. Main Logic for Camera Feed and Face Detection
def start_attendance_system():
    init_db()
    # Load OpenCV Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0) # Initialize webcam

    print("System Started. Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Draw rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Placeholder for identity recognition
            student_name = "SGGSIE&T_Student" 
            
            mark_attendance(student_name)
            
            # Display name on the frame
            cv2.putText(frame, f"ID: {student_name}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show the video feed window
        cv2.imshow('SGGSIE&T AI Attendance System', frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_attendance_system()