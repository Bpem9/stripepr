FROM python:3.7

ENV PYTHONUNBUFFERED 1


WORKDIR ./shop_app

COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]