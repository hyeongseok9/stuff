FROM python:3.6

RUN mkdir -p /home/hsnam
WORKDIR /home/hsnam

ADD . /home/hsnam/
RUN pip install -r requirements.txt
CMD ["python","app.py"]