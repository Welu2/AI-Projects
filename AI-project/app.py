import os
import streamlit as st

st.title("⚙️ Smart Environment Configurator")
st.write("This application automatically detects its host environment and adjusts settings.")

# 1. Look for a classic cloud variable to determine where the app is hosted
# Streamlit Cloud automatically sets specific internal indicators when live
is_cloud = os.environ.get("STREAMLIT_RUNTIME_VERSION") or os.environ.get("HOSTNAME")

# 2. Automatically toggle application behavior based on the result
if is_cloud:
    current_env = "PRODUCTION 🚀 (Live Cloud Server)"
    theme_color = "red"
    debug_mode = "DISABLED"
else:
    current_env = "DEVELOPMENT 💻 (Your Personal PC)"
    theme_color = "blue"
    debug_mode = "ENABLED"

# 3. Display the custom infrastructure dashboard
st.markdown(f"### Current Environment: :{theme_color}[{current_env}]")

st.json({
    "Environment Mode": current_env,
    "Debug Logging": debug_mode,
    "Database Pathway": "/local/storage/db" if not is_cloud else "/cloud/secure/cluster",
    "Security Level": "Standard Guardrails" if not is_cloud else "MAXIMUM PRODUCTION SHIELD"
})
