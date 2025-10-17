#!/usr/bin/env python3
"""
API Key Test Script
Bu script, API anahtarınızın geçerli olup olmadığını test eder.
"""

import os
from dotenv import load_dotenv
import requests

def test_api_key():
    # .env dosyasını yükle
    load_dotenv()
    
    # API anahtarını al
    api_key = os.environ.get("API_KEY", "YOUR_DEFAULT_API_KEY_OR_ERROR")
    
    print("API Anahtarı Testi")
    print("=" * 50)
    
    if api_key == "YOUR_DEFAULT_API_KEY_OR_ERROR" or not api_key:
        print("HATA: API_KEY ortam değişkeni ayarlanmamış!")
        print("Lütfen .env dosyasını kontrol edin ve geçerli bir API anahtarı girin.")
        return False
    
    print(f"API Anahtarı uzunluğu: {len(api_key)} karakter")
    
    # Apilayer Financial News API test isteği
    url = "https://api.apilayer.com/financelayer/news"
    headers = {
        'apikey': api_key
    }
    params = {
        'date': 'today'
    }
    
    try:
        print("Apilayer'a test isteği gönderiliyor...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            print("BAŞARILI: API anahtarı geçerli!")
            data = response.json()
            print(f"Yanıt alındı. Toplam haber sayısı: {len(data.get('data', []))}")
            return True
        elif response.status_code == 401:
            print("HATA: 401 Unauthorized - API anahtarı geçersiz veya süresi dolmuş!")
            print("Lütfen Apilayer'dan yeni bir API anahtarı alın.")
            return False
        else:
            print(f"HATA: HTTP {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"HATA: İstek gönderilirken bir hata oluştu: {e}")
        return False

if __name__ == "__main__":
    test_api_key()