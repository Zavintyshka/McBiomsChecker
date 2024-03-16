FROM python:3.12.2-alpine3.19
COPY ./requirements.txt /temp/requirements.txt
RUN mkdir /source
WORKDIR /source
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
CMD [ "/bin/sh" ]
