# Bu dosya uygulamayı yerel olarak çalıştırmak için kullanılır
# Komut: uvicorn main:app --reload --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)