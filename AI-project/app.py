import streamlit as st
# Import the new database functions from your backend
from engine import compute_server_load, get_system_greeting, save_config, load_config

st.title("💾 Persistent Infrastructure Hub")

# 1. Load saved data automatically when the app starts
saved_data = load_config()

st.subheader("System Settings")
# Use the saved data as the default values
operator_name = st.text_input("Operator Name:", saved_data["operator"])
multiplier = st.number_input("Server Load Multiplier:", value=float(saved_data["multiplier"]))

# 2. Add a Save Button to write data to disk
if st.button("💾 Save Settings permanently"):
    save_config(operator_name, multiplier)
    st.toast("Settings saved to system_config.json!", icon="✅")

# 3. Visual Diagnostics
st.divider()
greeting = get_system_greeting(operator_name)
st.success(greeting)

users = st.slider("Simulate Active Users:", min_value=1, max_value=100, value=20)
# Use the dynamic multiplier instead of a hardcoded one
base_load = users * multiplier
st.metric(label="Calculated Infrastructure Load", value=f"{base_load}%")
