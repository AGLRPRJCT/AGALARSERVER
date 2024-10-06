import os
import requests
from mcstatus import MinecraftServer
import time

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
    
    # 10 dakikada bir durumu kontrol et
    time.sleep(600)  # 600 saniye = 10 dakika
