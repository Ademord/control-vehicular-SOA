FROM tsutomu7/python-opencv
USER root

# Install prerequisites
run apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libcurl3-dev \
    libleptonica-dev \
    liblog4cplus-dev \
    libopencv-dev \
    libtesseract-dev \
    wget

run apt-get update && sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev

EXPOSE 5000

RUN apt-get update

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
ENV TARGET_SERVICE http://coincidencias
ENTRYPOINT ["python","/usr/src/app/server.py"]
