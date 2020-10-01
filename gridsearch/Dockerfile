FROM intelpython/intelpython3_full

RUN mkdir -p /home/hsnam
WORKDIR /home/hsnam

ADD . /home/hsnam/
RUN pip install -r requirements.txt
CMD ["celery","-A", "celery_app.celery", "worker" ,"--loglevel=info"]