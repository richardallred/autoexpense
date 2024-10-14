# Use an official Python image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your script
COPY download_verizon_bill.py /app/download_verizon_bill.py

# Create a directory for downloads
ENV DOWNLOAD_DIR=/downloads
RUN mkdir -p $DOWNLOAD_DIR

# Run the Python script with parameters passed to the container at runtime
CMD ["python", "/app/download_verizon_bill.py"]
