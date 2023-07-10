import sys
sys.path.append("../src")
import edge_tts
import asyncio
import os
import sys
import math
import random
import datetime

TXT_FILE = "庆余年.txt"
if len(sys.argv) == 2 and sys.argv[1].lower().endswith(".txt"):
    TXT_FILE = sys.argv[1]

async def amain(txt_file) -> None:
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
        v = 0
        for i in range(0, len(text), slice):
            n = i//slice + 1
            header = "{0}。第{1}册。".format(file_name, n)
            communicate = edge_tts.Communicate(header+text[i:i+slice], VOICES[v%len(VOICES)]["ShortName"])
            mp3_file = os.path.join(path_name, file_name, fmt.format(file_name, n, VOICES[v%len(VOICES)]["ShortName"]))
            tmp_file = mp3_file + ".tmp"
            if not os.path.exists(mp3_file):
                print(f"{n}/{count} {datetime.datetime.now()} ~ ", end="")
                await communicate.save(tmp_file)
                os.rename(tmp_file, mp3_file)
                print(f"{datetime.datetime.now()}")
            else:
                print(f"{n}/{count} {datetime.datetime.now()}")
            v += 1

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        mgr = asyncio.run(edge_tts.VoicesManager.create())
        VOICES = [v for v in mgr.voices if v["Locale"].startswith("zh-CN") or v["Locale"].startswith("zh-TW")]
        print("available languages : ", len(VOICES))
        loop.run_until_complete(amain(TXT_FILE))
    finally:
        loop.close()
