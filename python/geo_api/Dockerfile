FROM python:3.11-alpine

WORKDIR /geo

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest
COPY . .

# ENTRYPOINT ["python3", "geo"]
# ENTRYPOINT ["pytest"]