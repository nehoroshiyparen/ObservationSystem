import os 
import subprocess
from bot import run_bot
from observation import run_video
import threading


if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    video_thread = threading.Thread(target=run_video)

    bot_thread.start()
    video_thread.start()

    bot_thread.join()
    video_thread.join()