ARG BUILD_FROM
FROM $BUILD_FROM
FROM python:3.11-slim
# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3


# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
WORKDIR /app

RUN pip install flask flask_cors
COPY run.py .
RUN pip install flask flask_cors
CMD ["python", "run.py"]
