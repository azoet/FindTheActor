FROM python:3.8
COPY src /app
WORKDIR /app

RUN apt-get update 
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

RUN pip install flask
RUN pip install requests
RUN pip install numpy
RUN pip install opencv-python
RUN pip install mtcnn
RUN pip install tensorflow
RUN pip install Keras

EXPOSE 80
ENV FLASK_APP=main.py
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "80"]