# streamlit_app.py
import streamlit as st
import schedule
import subprocess
from datetime import datetime, timedelta

st.title('Automatic Script Runner via Streamlit')

def run_python_script():
    try:
        result = subprocess.run(["python", "darvas_box_final.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        st.code(result.stdout, language='python')
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def job():
    st.header("Running Python Script...")
    run_python_script()

# Schedule the job to run at 9:15 AM
schedule.every().day.at("09:15").do(job)

# Set the end time to 3:15 PM
end_time = datetime.now().replace(hour=15, minute=15, second=0, microsecond=0)

current_time = datetime.now()
if (
    current_time.weekday() < 5
    and current_time >= datetime(current_time.year, current_time.month, current_time.day, 9, 15)
    and current_time <= end_time
):
    st.empty()  # Clear the previous content
    job()
else:
    st.warning("Automatic execution is available on weekdays between 9:15 AM and 3:15 PM.")
