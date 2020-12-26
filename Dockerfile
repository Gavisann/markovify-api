FROM python:3
COPY ./code /code
COPY ./data /data
VOLUME [ "/data" ]
WORKDIR /code
RUN pip install -r requirements.txt
CMD python /code/app.py