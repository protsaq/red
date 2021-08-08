import sys
import requests

apikey = "INSERT_API_KEY"
url = "https://redacted.ch/ajax.php?"
header = {"Authorization": apikey}

def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

def artist_search():
	artist = {"action": "artist", "artistname": sys.argv[2]}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()['response']

	print("")
	for group in r1_json['torrentgroup']:
		print("Album name: " + group['groupName'])
		print("Album ID: " + str(group['groupId']))
		print("")

def album_search():
	artist = {"action": "artist", "artistname": sys.argv[2]}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()['response']
	for group in r1_json['torrentgroup']:
		if group['groupName'].lower() == sys.argv[3]:
			album = {"action": "torrentgroup", "id": str(group['groupId'])}
			r2 = requests.get(url, params=album, headers=header)
			r2_json = r2.json()['response']
			for release in r2_json['torrents']:
				if release['format'] == "FLAC":
					if release['media'] != "Vinyl":
						if release['encoding'] == '24bit Lossless':
							print("***THIS IS A 24-BIT RELEASE***")
						print("Torrent ID: " + str(release['id']))
						print("Media: " + release['media'])
						print("Size: " + str(sizeof_fmt(release['size'])))
						print("Seeders: " + str(release['seeders']))
						print("")
		else:
			continue

def torrent_download():
	torrentID = {"action": "download", "id": sys.argv[2]}
	r1 = requests.get(url, params=torrentID, headers=header)
	open('file.torrent', 'wb').write(r1.content)

def user_stats():
    stats = {"action": "index"}
    r1 = requests.get(url, params=stats, headers=header)
    r1_json = r1.json()['response']
    print("Username........." + r1_json['username'])
    print("Class............" + r1_json['userstats']['class'])
    print("Ratio............" + str(r1_json['userstats']['ratio']))
    print("Required Ratio..." + str(r1_json['userstats']['requiredratio']))
    print("Upload..........." + str(sizeof_fmt(r1_json['userstats']['uploaded'])))
    print("Download........." + str(sizeof_fmt(r1_json['userstats']['downloaded'])))
    print("Messages........." + str(r1_json['notifications']['messages']))

if sys.argv[1] == "search":
    if len(sys.argv[3]) > 0:
        album_search()
    else:
        artist_search()
if sys.argv[1] == "stats":
    user_stats()
if sys.argv[1] == "download":
	torrent_download()
