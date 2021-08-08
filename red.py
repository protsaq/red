#!/usr/bin/env python3

import key
import sys
import requests

url = "https://redacted.ch/ajax.php?"
header = {"Authorization": key.api_key}

def release_type(x):
	if x == 1:
		x = "Album"
	elif x == 3:
		x = "Soundtrack"
	elif x == 5:
		x = "EP"
	elif x == 6:
		x = "Anthology"
	elif x == 7:
		x = "Compilation"
	elif x == 9:
		x = "Single"
	elif x == 11:
		x = "Live Album"
	elif x == 13:
		x = "Remix"
	elif x == 14:
		x = "Bootleg"
	elif x == 17:
		x = "Demo"
	elif x == 18:
		x = "Concert Recording"
	elif x == 1022:
		x = "Composition"
	elif x == 1024:
		x = "Guest Appearance"
	else:
		x = "N/A"
	return x

def sizeof_fmt(num, suffix='B'):
	for unit in ['','K','M','G','T','P','E','Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

def artist_search():
	artist = {"action": "artist", "artistname": str(sys.argv[2]).lower()}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()['response']

	print("")
	for group in r1_json['torrentgroup']:
		print("Album name: " + group['groupName'])
		print("Release type: " + str(release_type(group['releaseType'])))
		print("")

def album_search():
	artist = {"action": "artist", "artistname": str(sys.argv[2]).lower()}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()['response']
	for group in r1_json['torrentgroup']:
		if group['groupName'].lower() == str(sys.argv[3]).lower():
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
						print("Files: " + str(release['fileCount']))
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

if str(sys.argv[1]).lower() == "search":
	try:
		if len(sys.argv[3]) > 0:
			album_search()
	except:
		artist_search()
if str(sys.argv[1]).lower() == "stats":
    user_stats()
if str(sys.argv[1]).lower() == "download":
	torrent_download()
