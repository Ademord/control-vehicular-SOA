FROM miiha/python-opencv-ffmpeg

USER root
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt


ENV TARGET_SERVICE http://reconocedor
EXPOSE 55552
ENTRYPOINT ["python","/usr/src/app/server.py"]
