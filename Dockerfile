FROM python:3.9-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl

COPY requirements.txt .

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
    
CMD ["python", "app.py"]