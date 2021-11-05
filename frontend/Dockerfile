FROM python:3.9.7-alpine
WORKDIR /app
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 9090
ARG tag=null
ENV VERSION=${tag}
ENV KAFKA_URL=localhost:29092
ENV BACKEND_URL=localhost:9091
ENTRYPOINT ["python", "-u", "app.py"]