FROM python:3.8
WORKDIR /usr/src/app
ADD . /usr/src/app
CMD ["python", "main.py"]