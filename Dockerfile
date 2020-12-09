FROM python:3.8.6
COPY search_youbike/ /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install mysqlclient

