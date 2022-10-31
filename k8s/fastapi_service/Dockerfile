FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]
CMD ["uvicorn", "fastapi_service.__main__:app", "--host", "0.0.0.0", "--port", "80"]
