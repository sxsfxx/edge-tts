import sys
sys.path.append("../src")
import edge_tts
import asyncio
import os
import sys
import math
import random
import datetime
import pprint

TXT_FILE = "搜神记-树下野狐.txt"
if len(sys.argv) == 2 and sys.argv[1].lower().endswith(".txt"):
    TXT_FILE = sys.argv[1]

async def text_to_mp3(txt_file, VOICES):
    """Main function"""
    path_name, file_name = os.path.split(txt_file)
    file_name, _ = os.path.splitext(file_name)
    if not os.path.exists(os.path.join(path_name, file_name)):
        os.mkdir(os.path.join(path_name, file_name))
    with open(txt_file, encoding="utf-8") as fr:
        text = fr.read()
        slice = 1024*16
        count = math.ceil(len(text)/slice)
        padding = math.floor(math.log10(count)) + 1
        fmt = "{{0}}_{{1:0{0}}}_{{2}}.mp3".format(padding)
        for n,pos in enumerate(range(0, len(text), slice), 1):
            header = "{0}。第{1}册。".format(file_name, n)
            mp3_file = os.path.join(path_name, file_name, fmt.format(file_name, n, VOICES[n%len(VOICES)]["ShortName"]))
            tmp_file = mp3_file + ".tmp"
            if not os.path.exists(mp3_file):
                print(f"{n}/{count} {datetime.datetime.now()} ~ ", end="")
                communicate = edge_tts.Communicate(header+text[pos:pos+slice], VOICES[n%len(VOICES)]["ShortName"])
                await communicate.save(tmp_file)
                os.rename(tmp_file, mp3_file)
                print(f"{datetime.datetime.now()}")
            else:
                print(f"{n}/{count} {datetime.datetime.now()}")

def list_voices():
    mgr = asyncio.run(edge_tts.VoicesManager.create())
    VOICES = [v for v in mgr.voices if v["Locale"].startswith("zh-CN") or v["Locale"].startswith("zh-TW")]
    pprint.pprint(VOICES)
    return VOICES

def get_voices():
    return list_voices()

def main():
    VOICES = get_voices()
    asyncio.run(text_to_mp3(TXT_FILE, VOICES))

if __name__ == "__main__":
    main()
