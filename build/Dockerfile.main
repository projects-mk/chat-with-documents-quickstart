FROM python:3.10.13-bookworm

RUN apt-get update && mkdir /app

COPY .. /app

RUN pip install -r /app/build/requirements.txt

WORKDIR /app/src

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
