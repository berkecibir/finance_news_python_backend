import os
import requests
from fastapi import FastAPI, HTTPException, Query
from typing import Optional

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(
    title="Apilayer Finans Haberleri Proxy Servisi",
    description="Flutter uygulamasından gelen istekleri Apilayer'a yönlendiren güvenli backend servisi. Apilayer'ın 'apikey' başlığı kullanılmıştır."
)

# API Anahtarınızı ortam değişkenlerinden alıyoruz. 
# Render'a deploy ederken bu anahtarı ortam değişkeni olarak tanımlayacaksınız (API_KEY).
# Bu, anahtarın kod içinde görünmesini engeller ve güvenliği artırır.
API_KEY = os.environ.get("API_KEY", "YOUR_DEFAULT_API_KEY_OR_ERROR")
BASE_URL = "https://api.apilayer.com/financelayer/news"

@app.on_event("startup")
async def startup_event():
    """Uygulama başladığında API anahtarının kontrolünü yap."""
    if API_KEY == "YOUR_DEFAULT_API_KEY_OR_ERROR":
        print("UYARI: API_KEY ortam değişkeni ayarlanmadı. Varsayılan veya sahte bir anahtar kullanılıyor olabilir.")
        # Gerçek bir üretim ortamında burada uygulamayı durdurmak isteyebilirsiniz.

@app.get("/")
def read_root():
    """Ana sayfa. Servisin çalıştığını gösterir."""
    return {"message": "Apilayer Finans Haberleri Proxy Servisi çalışıyor. /haberler endpoint'ini kullanın."}

@app.get("/haberler", summary="Apilayer'dan Finans Haberlerini Çeker")
async def get_financial_news(
    # Bu parametreler Flutter uygulamasından gelecektir
    date: str = Query("today", description="Haberin tarihi (ör: 'today' veya 'YYYY-MM-DD')."),
    keywords: Optional[str] = Query(None, description="Haber içeriğinde aranacak anahtar kelimeler (URL encode edilmeli)."),
    sources: Optional[str] = Query(None, description="Haber kaynakları (virgülle ayrılmış, ör: 'seekingalpha.com,ft.com')."),
    tickers: Optional[str] = Query(None, description="Şirket sembolleri (virgülle ayrılmış, ör: 'dis,att')."),
    keyword: Optional[str] = Query(None, description="Ek bir anahtar kelime.")
):
    """
    Kullanıcının belirlediği filtrelerle Apilayer Financelayer'dan haber verilerini çeker.
    """
    
    # Apilayer için doğru olan 'apikey' başlığı kullanılıyor
    headers = {
        'apikey': API_KEY
    }

    # API'ye gönderilecek parametreleri dinamik olarak oluşturuyoruz
    params = {
        'date': date,
    }
    if keywords:
        params['keywords'] = keywords
    if sources:
        params['sources'] = sources
    if keyword:
        params['keyword'] = keyword
    if tickers:
        params['tickers'] = tickers
        
    try:
        # Apilayer'a istek gönderiyoruz
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        # Eğer istek başarısız olursa (örn: 401 Unauthorized, 403 Forbidden, 429 Rate Limit)
        if response.status_code != 200:
            # Hata mesajını Apilayer'dan alıp Flutter'a iletiyoruz
            try:
                error_detail = response.json().get("message", "Apilayer'dan bilinmeyen bir hata alındı.")
            except:
                error_detail = "Apilayer'dan bilinmeyen bir hata alındı."
            
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Apilayer İstek Hatası: {error_detail}"
            )
        
        # Başarılı cevabı JSON olarak Flutter'a iletiyoruz
        return response.json()

    except requests.exceptions.RequestException as e:
        # Ağ veya bağlantı hatası durumunda
        raise HTTPException(status_code=503, detail=f"Backend bağlantı hatası: {str(e)}")