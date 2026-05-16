import streamlit as st
import time

st.title("🚨 Automated Infrastructure Alerting")
st.write("Simulate a cloud server failure and watch the automated alerting engine trigger.")

# 1. This function simulates sending an alert to an engineering team
def send_system_alert(service_name, error_message):
    # In a real system, this would send an SMS, email, or Slack message
    alert_time = time.strftime("%H:%M:%S")
    notification = f"⚠️ [ALERT @ {alert_time}] System: '{service_name}' failed! Reason: {error_message}"
    return notification

# 2. Interactive buttons to trigger different severities
st.subheader("Trigger Test Alerts")

if st.button("Simulate AI Model Crash"):
    with st.spinner("Processing error log..."):
        time.sleep(1)
        # Call the alerting function
        alert_result = send_system_alert("Llama-3-Model-Server", "Out of GPU Memory (OOM)")
        st.error("🚨 Critical Alert Dispatched to Team Chat!")
        st.code(alert_result)

if st.button("Simulate Database Timeout"):
    with st.spinner("Processing error log..."):
        time.sleep(1)
        alert_result = send_system_alert("User-Database-Cluster", "Connection timed out after 30 seconds")
        st.warning("⚠️ Warning Alert Sent to On-Call Engineer.")
        st.code(alert_result)
