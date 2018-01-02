from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import Request
import urllib.parse
from json import loads
import http.client
import http.server
import webbrowser
import re
import sys
import requests

def getData(url, headers={}):
	try:
		request = Request(url, headers=headers)
		response = urlopen(request)
		data = response.read()
		encoding = response.info().get_content_charset('utf8')
		return loads(data.decode(encoding))
	except Exception:
		print('\nFailed to get data from', url)

def createSpotifyUrl(url):
	urlComponents = {
		'https://open.spotify.com/user': 'https://api.spotify.com/v1/users',
		'playlist': 'playlists'
	}

	for component in urlComponents:
		url = url.replace(component, urlComponents[component])
	return url

def getSpotifyTracks(url, token):
	tracks = []
	params = '/tracks?fields=items(track(id,name,artists(name)),added_by(id)),next'
	try:
		while url:
			decodedData = getData(url + params, {'Authorization': 'Bearer ' + token})
			tracks.extend(decodedData['items'])
			url = decodedData['next']
	except Exception:
		print('\nFailed to get Spotify tracks')
	return tracks

def getRockBandIds(url):
	try:
		rbTracks = getData(url)['collection']
		return [track['spotifyId'] for track in rbTracks]
	except Exception:
		print('\nFailed to get Rock Band tracks')
		return []

def getSpotifyPlaylistName(url, token):
	try:
		data = getData(url + '?fields=name', {'Authorization': 'Bearer ' + token})
		return data['name']
	except Exception:
		return 'Spotify playlist'

def getSpotifyAuthToken():
	client_id = 'fcc8cc664f5f448e9c90b265a77118a5'
	client_secret = 'b651409975ea4a129347d1c7c603c070'

	grant_type = 'client_credentials'

	body_params = {'grant_type' : grant_type}

	authUrl='https://accounts.spotify.com/api/token'

	response = requests.post(authUrl, data=body_params, auth = (client_id, client_secret))
	return response.json()['access_token']

def main():
	tlPlaylistUrl = 'https://api.spotify.com/v1/users/robcthegeek/playlists/2JwE2prZ0fdX82d3alpGhQ'
	spotifyPlaylistUrl = createSpotifyUrl(sys.argv[1]) if len(sys.argv) > 1 else tlPlaylistUrl
	rockbandPlaylistUrl = 'https://rbdb.io/v3/songs?fields=spotifyId'

	spotifyToken = getSpotifyAuthToken()

	spotifyPlaylistName = getSpotifyPlaylistName(spotifyPlaylistUrl, spotifyToken)

	print('\n>> Getting tracks from {0}'.format(spotifyPlaylistName))

	spotifyTracks = getSpotifyTracks(spotifyPlaylistUrl, spotifyToken)
	rockBandIds = getRockBandIds(rockbandPlaylistUrl)

	numberOfMatches = 0

	for track in spotifyTracks:
		if any(rockBandId == track['track']['id'] for rockBandId in rockBandIds):
			print('\n* {track[name]} by {track[artists][0][name]}. Added by {added_by[id]}.'.format(**track))
			numberOfMatches += 1

	if numberOfMatches == 0:
		print('\n** No matches :(')
	else:
		print('\n*** {0} Rock Band tracks found in {1}. ***'.format(numberOfMatches, spotifyPlaylistName)) # pluralisation (1 matches?)

if __name__ == '__main__':
	main()
