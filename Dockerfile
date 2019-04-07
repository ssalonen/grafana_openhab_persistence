FROM python:3.7-slim

# If needed, install system dependencies here

# Add requirements.txt before rest of repo for caching
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD main.py /app

ENV PYTHONUNBUFFERED=true
CMD [ "python3", "main.py" ]