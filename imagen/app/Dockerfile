FROM ekazakov/python-opencv
USER root
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/data
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

ENV UPLOADS_PATH /usr/src/data/
ENV DATABASE_HOST=homestead
ENV DATABASE_NAME=homestead
ENV DATABASE_USER=homestead
ENV DATABASE_PASSWORD=secret
ENV DATABASE_PORT=5432
EXPOSE 55555
ENTRYPOINT ["python","/usr/src/app/server.py"]

