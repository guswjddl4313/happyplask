FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
Run echo "FLAG{which_d0_you_pr3fer_fl4sk_or_php?}" > ./flag.txt
RUN chmod 444 ./flag.txt
CMD ["python", "app.py"]

