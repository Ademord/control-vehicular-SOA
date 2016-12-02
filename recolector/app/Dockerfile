FROM tsutomu7/python-opencv

USER root
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

ENV TARGET_SERVICE http://reconocedor
EXPOSE 55552
ENTRYPOINT ["python","/usr/src/app/server.py"]
