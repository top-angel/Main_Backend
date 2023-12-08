FROM ubuntu:20.04

RUN useradd -rm -d /home/appuser -s /bin/bash -g root -G sudo -u 1001 appuser

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y curl git software-properties-common libcairo2-dev libjpeg-dev libgif-dev libzbar-dev \
  && add-apt-repository -y ppa:deadsnakes/ppa \
  && apt-get install -y python3.9 python3.9-distutils python3.9-dev\
  && apt-get install -y build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.9 get-pip.py \
  && rm get-pip.py

RUN echo 'alias python="python3.9"' >> ~/.bashrc && echo 'alias python3="python3.9"' >> ~/.bashrc
RUN echo 'alias pip3="pip3.9"' >> ~/.bashrc && echo 'alias pip="pip3.9"' >> ~/.bashrc

RUN apt-get update && apt-get install vim -y && apt-get install less -y

# RUN chown -R appuser /home/appuser
# USER appuser

WORKDIR /home/appuser/app
RUN pip install --upgrade pip
RUN pip install wheel

COPY requirements/prod_linux.txt /home/appuser/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install ocean-lib

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY --chown=appuser:root . .

RUN chown -R appuser /home/appuser

EXPOSE 8080 8089

CMD ["uwsgi", "app.ini"]
