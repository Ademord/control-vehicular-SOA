# ademord/recolector-img
# author: ademord

FROM miiha/python-opencv-ffmpeg
USER root
RUN mkdir -p /app && mkdir -p /app/data
WORKDIR /app
COPY . /app/
#RUN wget https://www.dropbox.com/s/rwi1oc1spj1kjb7/image.jpg  && \
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 55552

ENTRYPOINT ["python","app.py"]
