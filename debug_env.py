#!/usr/bin/env python3
"""
Environment Debug Script
Bu script, ortam değişkenlerinin doğru yüklenip yüklenmediğini kontrol eder.
"""

import os
from dotenv import load_dotenv

# Önce mevcut ortam değişkenlerini kontrol edelim
print("Mevcut API_KEY ortam değişkeni:", os.environ.get("API_KEY", "Bulunamadı"))

# .env dosyasını yükleyelim
print("\n.env dosyası yükleniyor...")
load_dotenv()

# Yüklemeden sonra ortam değişkenlerini kontrol edelim
api_key = os.environ.get("API_KEY", "Bulunamadı")
print("Yükleme sonrası API_KEY değeri:", api_key)

if api_key != "Bulunamadı" and api_key != "YOUR_DEFAULT_API_KEY_OR_ERROR":
    print(f"API Anahtarı uzunluğu: {len(api_key)} karakter")
else:
    print("Geçerli bir API anahtarı bulunamadı!")