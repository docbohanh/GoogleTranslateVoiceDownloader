try:
    import requests
    from fake_useragent import UserAgent
    import json
    import time
    import os
except ImportError as e:
    print("This script requires 'requests' and 'fake_useragent' to be installed.")
    print("Please run 'pip install requests fake_useragent' from your shell to install them first.")
    print(f"Details:\n{e}")

ua = UserAgent()

# Download function
def download(url, filename):
    if len(filename) > 20:
        filename_disp = filename[:filename.find(".mp3")][:30] + "..." + ".mp3"
    else:
        filename_disp = filename
    print(f"Downloading '{filename_disp}'")

    headers = {'User-Agent': ua.chrome}

    r = requests.get(url, allow_redirects=True, headers=headers)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

print("Google Translate Voice Batch Downloader")
print("Audio provider: TextToSpeech.io")
print("By hungngocphat01\n")

# Default config
cfgDict = {"lang": "vi", "engine": "g1", "pitch": 0.5, "rate": 0.5, "gender": "female", "wait": 0.5}

# Open config file
try:
    confFile = open("config.json", mode="r", encoding="utf-8")
    cfgDict = json.load(confFile)
except Exception:
    print("File 'config.json' not exist or not readable. The program will use its default config.")
    print('{"lang": "vi", "engine": "g1", "pitch": 0.5, "rate": 0.5, "gender": "female", "wait": 0.5}')
finally:
    cfgLang = cfgDict["lang"]
    cfgEngine = cfgDict["engine"]
    cfgPitch = cfgDict["pitch"]
    cfgRate = cfgDict["rate"]
    cfgGender = cfgDict["gender"]
    cfgWait = cfgDict["wait"]

# Open input file 
try:
    inpFile = open("input.txt", mode="r", encoding="utf-8")
except Exception:
    print("File 'input.txt' not exist or not readable.")
    exit()

# Number of lines 
count = 0

# If "downloaded folder not exist, create one"
try:
    if os.path.exists("./downloaded") == False:
        os.mkdir("./downloaded")
except Exception as e:
    print("Folder 'downloaded' cannot be created. Please create one by yourself and run this script again.")
    print(f"Error: {e}")
    exit()

# Read and download the input file line-by-line
for line in inpFile.read().splitlines():
    text = line.replace(" ", "%20")
    url = f"https://texttospeech.responsivevoice.org/v1/text:synthesize?text={text}&lang={cfgLang}&engine={cfgEngine}&name=&pitch={cfgPitch}&rate={cfgRate}&volume=1&key=PL3QYYuV&gender={cfgGender}"
    try:
        download(url, r"./downloaded/" + line + ".mp3")
        count += 1
        time.sleep(cfgWait)
    except Exception as e:
        print(f"Cannot download {line}.mp3\n")


print(f"\nDownloaded {count} file(s)")

inpFile.close()
confFile.close()