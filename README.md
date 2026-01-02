# 🔐 StegoSecure Backend

Production-ready FastAPI backend for secure image steganography with encryption.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Development Server

```bash
# Run locally
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
# Using Gunicorn with Uvicorn workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📡 API Endpoints

### Base URL
```
http://localhost:8000
```

### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "StegoSecure API"
}
```

---

### 2. Encrypt Image
```http
POST /api/encrypt
```

**Request Type:** `multipart/form-data`

**Parameters:**
- `image` (file): Image file (JPG/PNG, max 5MB)
- `message` (string): Secret message to hide
- `key` (string): Encryption key

**Response:** PNG image file download

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/api/encrypt" \
  -F "image=@original.jpg" \
  -F "message=Confidential Data" \
  -F "key=secure123" \
  --output stego_image.png
```

---

### 3. Decrypt Image
```http
POST /api/decrypt
```

**Request Type:** `multipart/form-data`

**Parameters:**
- `image` (file): Stego image (JPG/PNG)
- `key` (string): Decryption key

**Response:**
```json
{
  "status": "success",
  "message": "Confidential Data"
}
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/api/decrypt" \
  -F "image=@stego_image.png" \
  -F "key=secure123"
```

## 📚 Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🏗️ Project Structure

```
backend/
├── main.py              # FastAPI application
├── stegano.py           # Steganography logic
├── config.py            # Configuration settings
├── validators.py        # Input validation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## ⚙️ Configuration

Edit `config.py` to customize:
- `MAX_IMAGE_SIZE_MB`: Maximum image size (default: 5MB)
- `ALLOWED_EXTENSIONS`: Allowed file types
- `API_PREFIX`: API route prefix

## 🔒 Security Features

- ✅ In-memory processing only (no file storage)
- ✅ Stateless API design
- ✅ XOR encryption with custom key
- ✅ LSB steganography technique
- ✅ Input validation and sanitization
- ✅ CORS enabled for frontend integration

## 🌐 Deployment

### Render

1. Create new Web Service
2. Connect your repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

### Railway

1. Create new project
2. Add GitHub repository
3. Railway will auto-detect and deploy

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## 🧪 Testing

### Python Tests
```bash
pytest tests/
```

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test encryption (replace with your files)
curl -X POST http://localhost:8000/api/encrypt \
  -F "image=@test.jpg" \
  -F "message=Test Message" \
  -F "key=testkey" \
  --output result.png

# Test decryption
curl -X POST http://localhost:8000/api/decrypt \
  -F "image=@result.png" \
  -F "key=testkey"
```

## 📊 Performance

- **Response Time:** < 2 seconds
- **Max Image Size:** 5MB
- **Memory:** Optimized for cloud deployment
- **Scalability:** Horizontal scaling ready

## 🚧 Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error

Example error response:
```json
{
  "detail": "Message too large for selected image"
}
```

## 🔮 Future Enhancements

- AES encryption support
- JWT authentication
- Rate limiting
- Batch processing
- Video steganography
- WebSocket support

## 📝 License

MIT License - Feel free to use for your college project!

## 🤝 Support

For issues or questions, check:
- Interactive docs at `/docs`
- Health endpoint at `/api/health`

---

**Built with FastAPI + OpenCV + NumPy**