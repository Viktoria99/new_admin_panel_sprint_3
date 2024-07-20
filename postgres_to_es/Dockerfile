FROM python:3.11

WORKDIR /opt/app

COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
         && pip install -r requirements.txt

COPY . .

RUN  chmod +x ./EtlProcess.py

ENTRYPOINT ["python", "/opt/app/EtlProcess.py"]