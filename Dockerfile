FROM python:3.12.6-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /challenge

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /challenge/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]