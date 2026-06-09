FROM python:3.11-slim

RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY backend_requiremets.txt .

# install CPU only torch to save size of image
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r backend_requiremets.txt

COPY . .

EXPOSE 8080
CMD [ "uvicorn", "app.main:app" , "--host", "0.0.0.0", "--port", "8080"]


