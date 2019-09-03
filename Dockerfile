FROM tensorflow/tensorflow:1.11.0-py3

RUN apt-get -y update && apt-get install -y \
    wget \
    nginx \
    ca-certificates

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY inference_code /opt/program
WORKDIR /opt/program
RUN chmod 755 serve
