import html
import sys
import const as c
from log_setup import *
from make_requests import *
import json

def sizeof_fmt(num, suffix="B"):
	for unit in ["","K","M","G","T","P","E","Z"]:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, "Yi", suffix)


def print_album_info(release):
	print("Torrent ID: " + str(release["id"]))
	print("Media: " + release["media"])
	print("Format: " + release["format"])
	print("Encoding: " + release["encoding"])
	print("Size: " + str(sizeof_fmt(release["size"])))
	print("Files: " + str(release["fileCount"]))
	print("Seeders: " + str(release["seeders"]))
	print("")


def artist_search(args, header):
	""" requires 2 arguments """
	artist = {"action": "artist", "artistname": args.artist.lower()}
	r1 = make_request(artist, header).json()["response"]
	wanted_releases = args.r if args.r != None else c.releases
	for releaseName in wanted_releass:
		filtered_releases = list(filter(lambda x: x['releaseType'] == c.releases[releaseName], r1['torrentgroup']))
		unique_results = list(set(map(lambda x: x["groupName"], filtered_releases)))
		if unique_results != []:
			print(releaseName)
			for record in unique_results:
				print("\t" + record)

def album_search(args, header):
	artist = {"action": "artist", "artistname": args.artist.lower()}
	r1 = make_request(artist, header).json()["response"]
	logging.debug(r1)
	for group in r1["torrentgroup"]:
		if html.unescape(group["groupName"].lower()) == args.album.lower():
			group = {"action": "torrentgroup", "id": str(group["groupId"])}
			r2 = make_request(group, header).json()["response"]
			for release in r2["torrents"]:
				if args.f is None and args.m is None:
					print_album_info(release)
				elif args.m is None and args.f is not None:
					if release["format"].lower() in args.f:
						print_album_info(release)
				elif args.f is None and args.m is not None:
					if release["media"].lower() in args.m:
						print_album_info(release)
				elif release["format"].lower() in args.f and release["media"].lower() in args.m:
					print_album_info(release)


def torrent_download(args, dir, header):
	if args.fl is True:
		download_params = {"action": "download", "id": args.torrentid, "usetoken": True}
	else:
		download_params = {"action": "download", "id": args.torrentid}
	details_params = {"action": "torrent", "id": args.torrentid}
	r1 = make_request(details_params, header)
	album = r1.json()["response"]["group"]["name"]
	artist = str((r1.json()["response"]["group"]["musicInfo"]["artists"][0]["name"]))
	download_params = {"action": "download", "id": args.torrentid, "usetoken": int(args.fl)}
	r2 = make_request(download_params, header)
	path = dir + artist + " - " + album + ".torrent"
	open(path, "wb").write(r2.content)
	print(f"Torrent for {artist} - {album} was successfully downloaded!")


def user_stats(header):
	stats = {"action": "index"}
	response_json = requests.get(c.url, params=stats, headers=header).json()
	print(response_json)
	print("Username........." + r1["username"])
	print("Class............" + r1["userstats"]["class"])
	print("Ratio............" + str(r1["userstats"]["ratio"]))
	print("Required Ratio..." + str(r1["userstats"]["requiredratio"]))
	print("Upload..........." + str(sizeof_fmt(r1["userstats"]["uploaded"])))
	print("Download........." + str(sizeof_fmt(r1["userstats"]["downloaded"])))
	print("Messages........." + str(r1["notifications"]["messages"]))
