import subprocess
import os
import time
import json


def start_stream(file_path, file_name, rtmp_url, stream_key):
    ffmpeg_command = [
        'ffmpeg',
        '-re',
        '-i', file_path,
        '-vf',
        f"drawtext=text='{file_name}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=w-tw-10:y=h-th-10",
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-f', 'flv',
        f'{rtmp_url}/{stream_key}'
    ]

    process = subprocess.Popen(ffmpeg_command)
    return process


def stream_default_video(default_video, rtmp_url, stream_key):
    while True:
        print(f"Streaming Default Video: {default_video}")
        stream_process = start_stream(default_video, default_video, rtmp_url, stream_key)
        stream_process.wait()
        time.sleep(5)


if __name__ == '__main__':
    try:
        with open('settings-cast-cli.json', 'r') as f:
            settings = json.load(f)

        video_dir = settings['video_dir']
        rtmp_url = settings['rtmp_url']
        stream_key = settings['stream_key']
        default_video = settings['default_video']

        while True:
            video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]

            if not video_files:
                print("Keine Videos im Verzeichnis gefunden. Streame Standardvideo.")
                stream_default_video(default_video, rtmp_url, stream_key)
            else:
                print("Starting Streaming...")

                for video_file in video_files:
                    file_path = os.path.join(video_dir, video_file)
                    print(f"Streame Datei: {video_file}")
                    stream_process = start_stream(file_path, video_file, rtmp_url, stream_key)
                    stream_process.wait()
                    time.sleep(5)

    except KeyboardInterrupt:
        print("Streaming interrupted.")
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        print("Streaming ended.")
