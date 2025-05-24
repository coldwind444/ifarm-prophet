FROM python:3.13.3

# Set working directory
WORKDIR /app
COPY server.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
ENV TZ=Asia/Ho_Chi_Minh

EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]