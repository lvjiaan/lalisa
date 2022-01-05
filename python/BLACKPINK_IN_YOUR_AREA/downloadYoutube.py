import hashlib
import youtube_dl
import time
import os
import logging
import socket

socket.setdefaulttimeout(20)

def download_video(url):
    """
    下载视频
    :param url:
    :return:
    """
    #设置视频保存路径
    storePath = "E:\\videos"
    if not os.path.exists(storePath):
        os.mkdir(storePath)
    try:
        print('Downloading:',url)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': hashlib.md5(url.encode()).hexdigest() + '.mp4'
        }
        os.chdir(storePath)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(url,"download compete",)
        time.sleep(0.5)
    except Exception as e:
        print("Download failed..",url)
        logging.error("url error:{}".format(url))

if __name__ == '__main__':
    #视频链接
    video_url = 'https://www.youtube.com/watch?v=cAvMGWLZCHA'
    download_video(video_url)
