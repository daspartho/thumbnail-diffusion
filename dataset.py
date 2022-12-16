import scrapetube
import requests
import os
import jsonlines
from datasets import load_dataset

def get_thumbnail(video_id, data_dir, file_name):
    thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(thumb_url)
    with open(f'{data_dir}/{file_name}', "wb") as f:
        f.write(response.content)

def create_thumbnail_dataset(data_dir, channel_url, limit=None):
    
    os.mkdir(data_dir) # create data dir

    videos = scrapetube.get_channel(channel_url=channel_url, limit=limit) # get videos
    video_data = []

    for n, video in enumerate(videos):
        title = video['title']['runs'][0]['text']
        title = title.split('-')[0].strip() # remove name from title (for teded channel)
        video_id = video['videoId']
        file_name = f"{n:03d}.jpg"
        get_thumbnail(video_id, data_dir, file_name) # save thumbnail
        video_data.append({"file_name":file_name,"title":title}) # add video metadata

    # create metadata for dataset
    with jsonlines.open(f'{data_dir}/metadata.jsonl', 'w') as f:
        f.write_all(video_data)
    
    # create image folder dataset
    dataset = load_dataset("imagefolder", data_dir=data_dir)
    return dataset

if __name__ == "__main__":

    dataset = create_thumbnail_dataset(
        data_dir='teded-thumbnails', 
        channel_url='https://www.youtube.com/user/TEDEducation',
        )

    dataset.push_to_hub("daspartho/teded-thumbnails") # push dataset to HF Hub