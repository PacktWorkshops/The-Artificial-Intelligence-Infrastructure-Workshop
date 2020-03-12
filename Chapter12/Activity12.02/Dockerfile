FROM python:3.7

RUN mkdir /api
WORKDIR /api
ADD . /api/

RUN pip install -r ./requirements.txt

EXPOSE 5000

ENV PYTHONPATH="$PYTHONPATH:/api"
CMD ["python", "/api/api.py"]
