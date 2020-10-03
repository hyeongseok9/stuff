FROM intelpython/intelpython3_full

RUN mkdir -p /home/hsnam
WORKDIR /home/hsnam

ADD . /home/hsnam/
RUN pip install -r requirements.txt

CMD ["celery",  "--app=grid_search_async.celery_app", "worker", "-c", "1", "--loglevel=INFO"]
