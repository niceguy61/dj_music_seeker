import os
import random
import string
from datetime import datetime
import yt_dlp
import boto3
import json

# 환경 변수 설정
AWS_PROFILE = os.getenv('AWS_PROFILE', 'sso')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')

# AWS 세션 설정
session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client('s3')

def download_youtube_audio(youtube_url, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            print(f"Successfully downloaded: {info['title']}")
            return True
            
    except Exception as e:
        print(f"Failed to download {youtube_url}: {str(e)}")
        return False

def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_music_list_from_bedrock(prompt):
    client = boto3.client('bedrock-runtime', region_name='ap-northeast-2')

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    response = client.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        body=body
    )

    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

def main():
    prompt = """
    You are a famous DJ and music producer in New York.
    You are selecting a playlist for a DJ party and downloading it.
    avoid officialmusic video.

    reference artist: Marcross 82-99
    reference music: youtube music
    like genres: house, drum and bass, dubstep, hip hop, pop, rock, synth-pop
    bpm: 100-130
    playtime: 2 hours

    Please provide the response in the following JSON format:
    {
        "playlist": [
            {
                "artist": "artist name",
                "title": "song title",
                "youtube_url": "youtube url",
                "bpm": "song bpm"
            }
        ]
    }

    Only respond with the JSON data, no additional text.
    """
    
    try:
        music_list_text = get_music_list_from_bedrock(prompt)
        print("Bedrock Response:", music_list_text)
        
        music_list = json.loads(music_list_text)
        
        today = datetime.now().strftime('%Y%m%d')
        random_id = generate_random_id()
        output_path = os.path.join(OUTPUT_DIR, today, random_id)
        os.makedirs(output_path, exist_ok=True)

        successful_downloads = 0
        failed_downloads = 0

        # 플레이리스트의 각 곡 다운로드
        for item in music_list['playlist']:
            youtube_url = item['youtube_url']
            if download_youtube_audio(youtube_url, output_path):
                successful_downloads += 1
            else:
                failed_downloads += 1
                continue

        print(f"\nDownload Summary:")
        print(f"Successfully downloaded: {successful_downloads} tracks")
        print(f"Failed to download: {failed_downloads} tracks")
        print(f"Files are saved in: {output_path}")
        
    except json.JSONDecodeError as e:
        print("JSON 파싱 오류:", e)
        print("받은 응답:", music_list_text)
    except Exception as e:
        print("오류 발생:", e)

if __name__ == "__main__":
    main()