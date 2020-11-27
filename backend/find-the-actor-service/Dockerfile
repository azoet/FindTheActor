FROM python:3.8
COPY src /app
WORKDIR /app

RUN pip install flask
RUN pip install requests

EXPOSE 80
ENV FLASK_APP=main.py
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "80"]
