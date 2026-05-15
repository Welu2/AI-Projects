import sqlite3
import streamlit as st

# 1. Initialize the database and create a table if it doesn't exist
conn = sqlite3.connect("platform_data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS prompts (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
)
conn.commit()

st.title("🗄️ Local Platform Database App")
st.write("Type something below to permanently store it in your local database.")

# 2. Input box for new data
new_prompt = st.text_input("Enter text to save:")

if st.button("Save to Memory Bank"):
    if new_prompt.strip() != "":
        # Insert the text into the database table
        cursor.execute("INSERT INTO prompts (text) VALUES (?)", (new_prompt,))
        conn.commit()
        st.success(f"Successfully saved: '{new_prompt}'")
    else:
        st.warning("Please enter some text first.")

# 3. Fetch and display the stored history
st.subheader("📜 Stored History Logs")
cursor.execute("SELECT text FROM prompts ORDER BY id DESC")
history = cursor.fetchall()

if history:
    for row in history:
        st.text(f"• {row[0]}")
else:
    st.info("The database is currently empty.")
