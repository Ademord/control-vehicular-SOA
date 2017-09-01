# ademord/recolector-vid
# author: ademord

FROM ademord/recolector-base
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/
EXPOSE 55551
ENTRYPOINT ["python","/usr/src/app/app.py"]
