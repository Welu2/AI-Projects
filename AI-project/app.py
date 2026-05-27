import sqlite3
import streamlit as st

# 1. Connect to the database file
conn = sqlite3.connect("relational_platform.db", check_same_thread=False)
cursor = conn.cursor()

# 2. Enable foreign key support (this forces the tables to stay linked)
cursor.execute("PRAGMA foreign_keys = ON;")

# 3. Create the Parent Table (Users)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    tier TEXT
)
""")

# 4. Create the Child Table (Prompts) linked to the Parent via a Foreign Key
cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_prompts (
    prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_text TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
""")
conn.commit()

# --- Pre-populate with Mock Data for Testing ---
try:
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, tier) VALUES (1, 'Operator_Alpha', 'Premium')")
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, tier) VALUES (2, 'Operator_Beta', 'Free')")
    conn.commit()
except Exception:
    pass

# --- Streamlit Dashboard Interface ---
st.title("🔗 Relational Data Mapping Engine")
st.write("Link user accounts directly to their saved AI prompts using database relationships.")

# Display existing users
st.subheader("👥 Registered Platform Users")
cursor.execute("SELECT * FROM users")
all_users = cursor.fetchall()
for u in all_users:
    st.text(f"ID: {u[0]} | Username: {u[1]} | Tier: {u[2]}")

# Interactive Area to assign a prompt to a specific user
st.subheader("📝 Submit Prompt to Specific User ID")
target_user_id = st.number_input("Target User ID (Choose 1 or 2):", min_value=1, max_value=2, value=1)
new_prompt_text = st.text_input("Enter AI Prompt text:")

if st.button("Link and Save Prompt"):
    if new_prompt_text.strip() != "":
        # Insert prompt while assigning it to the specific user_id
        cursor.execute("INSERT INTO ai_prompts (prompt_text, user_id) VALUES (?, ?)", (new_prompt_text, target_user_id))
        conn.commit()
        st.success(f"Successfully linked prompt to User ID {target_user_id}!")
    else:
        st.warning("Please type a prompt first.")

# Display the linked data using an SQL JOIN query
st.subheader("📊 Combined Live Relational Logs")
cursor.execute("""
    SELECT users.username, ai_prompts.prompt_text 
    FROM ai_prompts 
    JOIN users ON ai_prompts.user_id = users.user_id
""")
joined_logs = cursor.fetchall()

if joined_logs:
    for log in joined_logs:
        st.info(f"👤 {log[0]} ran prompt: '{log[1]}'")
else:
    st.write("No prompt history mapped yet.")
