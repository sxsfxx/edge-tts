from gtts import gTTS
import pygame
import os

def text_to_speech(txt, lang="zh-cn"):
    with open(txt, "r", encoding="utf-8") as fr:
        text_content = fr.read()

        # 使用gTTS将文本转换为语音
        tts = gTTS(text=text_content, lang=lang, slow=False)

        # 保存为MP3文件
        tts.save(os.path.splitext(txt)[0]+".mp3")

def play_audio(audio_file):
    # 初始化pygame
    pygame.init()

    # 加载音频文件
    pygame.mixer.music.load(audio_file)

    # 播放音频
    pygame.mixer.music.play()

    # 等待音频播放完成
    pygame.time.wait(3000)  # 等待3秒，可根据需要调整

    # 关闭pygame
    pygame.mixer.quit()
    pygame.quit()





