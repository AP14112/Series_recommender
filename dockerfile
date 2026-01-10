FROM python:3.10-slim

WORKDIR /app

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure immediate printing for active logs
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true 

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# not at top for easier code changes without reinstalling deps
COPY . .  

EXPOSE 8501
RUN python pipeline/build_pipeline.py


CMD [ "streamlit", "run", "app/app.py" ]

