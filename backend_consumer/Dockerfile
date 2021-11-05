FROM python:3.9.7-alpine
WORKDIR /app
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ARG tag=null
ENV VERSION=${tag}
ENV KAFKA_URL=localhost:9092 MONGO_URL=localhost:27017 MONGO_USER=root MONGO_PASS=pass12345
ENTRYPOINT ["python", "-u", "app.py"]