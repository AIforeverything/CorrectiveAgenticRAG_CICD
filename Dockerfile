FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY backend_requirements.txt .

# Install CPU-only PyTorch
RUN pip install \
    --index-url https://download.pytorch.org/whl/cpu \
    torch

# Install application dependencies
RUN pip install -r backend_requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# to build the image: 
# docker build -t image_name .

#to run the docker image:
# docker run -d \
#   --name crag \
#   -p 8080:8080 \
#   --env-file .env \
#   crag

# docker logs -f crag
