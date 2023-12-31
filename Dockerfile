FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./Mobi_Market/manage.py", "runserver", "0.0.0.0:8000"]