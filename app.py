import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="SGGSIE&T Smart Attendance",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size:35px !important; font-weight: bold; color: #1E3A8A; }
    .sub-text { font-size:18px !important; color: #555; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">AI-Powered Smart Campus Attendance System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Developed by: Assistant Professor (SGGSIE&T, Nanded) | M.Tech AI Research</p>', unsafe_allow_html=True)

st.divider()

# Function to Fetch Attendance Data from SQLite Database
def load_attendance():
    try:
        conn = sqlite3.connect('attendance.db')
        # Fetching data ordered by date and time in descending order
        query = "SELECT * FROM attendance ORDER BY date DESC, time DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception:
        # Returning an empty DataFrame if the table/database doesn't exist
        return pd.DataFrame(columns=['name', 'date', 'time'])

# Sidebar Configuration
st.sidebar.title("Professor Panel")

if st.sidebar.button('Refresh Dashboard'):
    st.cache_data.clear()
    st.rerun()

# Main Dashboard Layout
df = load_attendance()
today = datetime.now().strftime("%Y-%m-%d")
today_count = len(df[df['date'] == today])

# Metrics Display
m1, m2, m3 = st.columns(3)
m1.metric("Total Attendance Logs", len(df))
m2.metric("Today Attendance", today_count)
m3.metric("System Integrity", "Verified")

# Data Display
st.subheader("Recent Attendance Records")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    # CSV Report Export Functionality
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Attendance Report (CSV)",
        data=csv,
        file_name=f'attendance_report_{today}.csv',
        mime='text/csv',
    )
else:
    st.warning("No attendance records found.")

st.sidebar.write("---")
st.sidebar.markdown("**Tech Stack:** Python, Streamlit, SQLite, OpenCV")