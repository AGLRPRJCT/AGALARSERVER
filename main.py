import os
import requests
from mcstatus import MinecraftServer
import time
import os
from flask import Flask  

app = Flask(__name__)

@app.route('/')
def home():
    return "Minecraft Sunucu Durum Bildirici Çalışıyor!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render'dan gelen portu al
    app.run(host='0.0.0.0', port=port)  # Tüm IP adreslerinden gelen bağlantıları dinle


# Çevre değişkenlerinden IP adresi ve Webhook URL'sini al
minecraft_server_ip = os.getenv("MINECRAFT_SERVER_IP")
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Sunucu durumu mesajını gönderme işlevi
def send_status_to_discord(status_message):
    data = {
        "content": status_message
    }
    response = requests.post(discord_webhook_url, json=data)
    if response.status_code == 204:
        print("Durum mesajı başarıyla gönderildi.")
    else:
        print("Bir hata oluştu:", response.text)

# Sunucu durumunu düzenli olarak kontrol et
while True:
    try:
        server = MinecraftServer(minecraft_server_ip)  # IP adresini burada kullanın
        status = server.status()
        message = f"🟢 Minecraft sunucusu **açık**. Şu anda {status.players.online} oyuncu bağlı."
    except Exception as e:
        try:
            server.ping()  # Sunucu pingi kontrol et
            message = "🟠 Minecraft sunucusu **sırada**. Lütfen bekleyin."
        except:
            message = "🔴 Minecraft sunucusu **kapalı**."

    send_status_to_discord(message)
    
    # 1 dakikada bir durumu kontrol et
    time.sleep(60) 
