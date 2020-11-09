FROM python:3.8
COPY . /work
WORKDIR /work/App

RUN apt-get update 
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y
	
RUN pip install -r env.txt

EXPOSE 5000
ENV FLASK_APP=FindTheActor.py
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
