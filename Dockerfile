FROM python:3.12-slim
RUN groupadd -r backend_group && useradd -r -g backend_group backend_user
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
USER backend_user
