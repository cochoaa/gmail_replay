FROM python:3.9.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt
COPY *.py /app/
CMD ["python","/app/reply.py"]
