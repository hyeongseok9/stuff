FROM intelpython/intelpython3_full

RUN mkdir -p /home/hsnam
WORKDIR /home/hsnam

ADD . /home/hsnam/
RUN pip install -r requirements.txt
CMD ["python","langtest8.py"]