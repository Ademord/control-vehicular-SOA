# ademord/recolector-img
# author: ademord

FROM miiha/python-opencv-ffmpeg
USER root
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN wget https://www.dropbox.com/s/62fg0djaafuazpc/video1.avi && \
    wget https://www.dropbox.com/s/rwi1oc1spj1kjb7/image.jpg  && \ 
    pip install --no-cache-dir -r requirements.txt

EXPOSE 55552

ENTRYPOINT ["python","/usr/src/app/app.py"]
