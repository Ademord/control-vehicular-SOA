# ademord/reconocedor
# author: ademord
FROM ademord/reconocedor-base

EXPOSE 5000
RUN apt-get update

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
ENV TARGET_SERVICE http://coincidencias
ENTRYPOINT ["python","/usr/src/app/worker.py"]