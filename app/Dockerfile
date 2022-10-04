FROM python:3.10

COPY src /src
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]