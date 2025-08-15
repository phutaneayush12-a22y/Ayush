import socket
import os
import requests
import shutil

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=4)
        return True
    except OSError:
        return False


def download_file(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, url.split("/")[-1])
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    print(f"Downloaded: {filename}")


def update_resources():
    if check_internet():
        print("Internet found 🌐 — downloading online resources...")
        online_folder = "online_resources"
        if not os.path.exists(online_folder):
            os.makedirs(online_folder)

        urls = [
                "https://cdn.pixabay.com/download/audio/2024/03/15/audio_0d2a689d30.mp3",
                "https://cdn.pixabay.com/download/audio/2025/06/21/audio_fba2cc81f7.mp3"
        ]

        for url in urls:
            download_file(url, online_folder)

        if not os.path.exists("local_resources"):
            os.makedirs("local_resources")

        for filename in os.listdir(online_folder):
            shutil.copy(os.path.join(online_folder, filename),
                        os.path.join("local_resources", filename))
        print("----Local storage updated----")
    else:
        print("----No internet — using local resources----")
        if os.path.exists("local_resources"):
            print(f"Found {len(os.listdir('local_resources'))} local files.")
        else:
            print("----No local resources found----")


update_resources()
