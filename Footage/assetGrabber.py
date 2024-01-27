import os
import requests
import re

def download_files_from_assets():
    with open('assets.txt', 'r') as file:
        for line in file:
            # Extract video name, link, and ID
            video_name, link = line.strip().split(' - ')
            id_match = re.search(r'\((\d+)\)', video_name)
            id = id_match.group(1) if id_match else None

            file_path = os.path.join('assets', f'{video_name[:id_match.start()]}_{id}{video_name[id_match.end():]}') if id else os.path.join('assets', video_name)

            if os.path.exists(file_path):
                print(f"Skipping {video_name} (ID: {id}): File already exists.")
                continue

            try:
                response = requests.get(link, stream=True)
                response.raise_for_status() 

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

                print(f"Downloaded: {video_name}")
            except requests.exceptions.RequestException as err:
                print(f"Error downloading {video_name}: {err}")

if __name__ == '__main__':
    download_files_from_assets()