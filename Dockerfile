FROM python:3.7-slim

# If needed, install system dependencies here

# Add requirements.txt before rest of repo for caching
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD main.py /app
ADD generate_key.py /app
CMD [ "python3", "main.py" ]