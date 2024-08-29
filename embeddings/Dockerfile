# Base Stage: Create our venv and install dependencies
FROM python:3.12.5-slim AS base
WORKDIR /app
COPY requirements.txt /app/
# Create venv and install app dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

# Test Stage: Install pytest and any other testing packages and run pytest
FROM python:3.12.5-slim AS test
COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
ENV ALLOW_DOWNLOAD_MODEL=true
WORKDIR /app
COPY . /app
RUN pip install -r requirements-test.txt
CMD ["pytest"]

# Production Stage: Build our production image
FROM python:3.12.5-slim AS production
COPY --from=base /opt/venv /opt/venv
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
WORKDIR /app
COPY src /app/
EXPOSE 5000
CMD ["sh", "-c", "gunicorn -t ${GUNICORN_TIMEOUT:-30} -w 1 -b :5000 app:app"]
