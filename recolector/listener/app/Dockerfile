# ademord/listener
# author: ademord

FROM python

ENV REDIS_SERVICE_HOST redis

WORKDIR /app
COPY . /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -rf /var/cache/apk/* root/.cache/*

ENTRYPOINT ["python","/app/listener.py"]

