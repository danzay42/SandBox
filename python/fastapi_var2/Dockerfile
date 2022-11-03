FROM python 

WORKDIR /usr/src/app

# COPY requirenments.txt ./
COPY . .
RUN pip install --no-cache-dir -r requirenments.txt

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]