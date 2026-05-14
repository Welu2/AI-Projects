# 1. Start with a pre-configured Python environment
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy files from your PC into the container
COPY requirements.txt .
COPY app.py .

# 4. Install the exact dependencies needed
RUN pip install uv && uv pip install --system --no-cache -r requirements.txt

# 5. Expose the port that Streamlit uses
EXPOSE 8501

# 6. Define the command to start your application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
