FROM python:3.9-alpine

LABEL maintainer="Augusto Arraes <arraes.augusto@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN mkdir uploads

COPY . .

EXPOSE 5671

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5671"]
