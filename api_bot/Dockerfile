FROM python:3.11.8

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR /api_bot

COPY . .


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]