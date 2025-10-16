# Dockerfile
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Non-root kullanıcı oluştur
RUN useradd --create-home --shell /bin/bash appuser

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Dosya sahipliğini değiştir
RUN chown -R appuser:appuser /app

# Portu aç
EXPOSE 8000

# Non-root kullanıcıya geç
USER appuser

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]