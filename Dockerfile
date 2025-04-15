FROM python:3.13

WORKDIR ./app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN cd ./diploma-frontend/dist && pip install diploma-frontend-0.6.tar.gz && cd ../..

RUN python ./megano/manage.py migrate

CMD ["python", "./megano/manage.py", "runserver", "--insecure", "0.0.0.0:8000"]