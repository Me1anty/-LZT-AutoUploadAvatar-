import os
import requests
import time
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

token = config.get('API', 'token')

image_folder = "image"
image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]

url = "https://api.zelenka.guru/users/me/avatar"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {token}"
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M',
    handlers=[logging.StreamHandler()]
)

def change_avatar(image_path):
    try:
        with open(image_path, "rb") as avatar_file:
            files = {
                "avatar": (os.path.basename(image_path), avatar_file, "image/png")
            }
            response = requests.post(url, files=files, headers=headers)

            if response.status_code == 200:
                logging.info(f"✔️ Успешно сменили аватарку: {os.path.basename(image_path)}")
            else:
                logging.error(f"❌ Ошибка при смене аватарки {os.path.basename(image_path)}: {response.text}")

    except Exception as e:
        logging.error(f"❌ Ошибка при обработке изображения {image_path}: {str(e)}")

while True:
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        logging.info(f"🔄 Начинаем смену аватарки на: {image_file}")
        change_avatar(image_path)
        logging.info((
            f"⏳ Ожидаем 10 секунд перед следующей аватаркой...\n"
            f"============================================="
        ))

        time.sleep(10)
