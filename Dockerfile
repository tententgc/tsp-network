FROM python:3.9

WORKDIR /app

COPY . .

CMD [ "python", "-u", "city.py" ]
