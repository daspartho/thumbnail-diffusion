import scrapetube
import requests
import os
from datasets import load_dataset

def get_thumb(video_id, data_dir, file_name):
    thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(thumb_url)
    with open(f'{data_dir}/{file_name}', "wb") as f:
        f.write(response.content)
    
def update_metadata(data_dir, file_name, title):
    with open(f'{data_dir}/metadata.jsonl', 'a') as f:
        f.write('{"file_name": "'+file_name+'", "title": "'+title+'"}\n')

def create_thumb_dataset(data_dir, channel_url, limit=None):
    
    os.mkdir(data_dir)

    videos = scrapetube.get_channel(channel_url=channel_url, limit=limit)

    for n, video in enumerate(videos):
        title = video['title']['runs'][0]['text']
        video_id = video['videoId']
        file_name = f"{n:03d}.jpg"
        get_thumb(video_id, data_dir, file_name)
        update_metadata(data_dir, file_name, title)
    
    dataset = load_dataset("imagefolder", data_dir=data_dir)
    return dataset

if __name__ == "__main__":

    dataset = create_thumb_dataset(
        data_dir='mrbeast-thumbnails', 
        channel_url='https://www.youtube.com/user/mrbeast6000', 
        limit=150,
        )

    dataset.push_to_hub("daspartho/mrbeast-thumbnails")