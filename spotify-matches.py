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

class SpotifyAPI:

	def __init__(self, client_id, secret, url):
		self._credentials = (client_id, secret)
		self._url = url

	def authorise(self):
		authUrl='https://accounts.spotify.com/api/token'
		grant_type = 'client_credentials'
		body_params = {'grant_type' : grant_type}

		response = requests.post(authUrl, data=body_params, auth=self._credentials)
		self._token = response.json()['access_token']

	def createUrl(self):
		url = self._url
		urlComponents = {
			'https://open.spotify.com/user': 'https://api.spotify.com/v1/users',
			'playlist': 'playlists'
		}

		for component in urlComponents:
			url = url.replace(component, urlComponents[component])
		self._url = url

	def getPlaylistName(self):
		try:
			data = getData(self._url + '?fields=name', {'Authorization': 'Bearer ' + self._token})
			return data['name']
		except Exception:
			return 'Spotify playlist'

	def getTracks(self):
		tracks = []
		params = '/tracks?fields=items(track(id,name,artists(name)),added_by(id)),next'
		url = self._url
		try:
			while url:
				decodedData = getData(url + params, {'Authorization': 'Bearer ' + self._token})
				tracks.extend(decodedData['items'])
				url = decodedData['next']
		except Exception:
			print('\nFailed to get Spotify tracks')
		return tracks


class RockBandAPI:

	def __init__(self, url):
		self._url = url

	def getRockBandIds(self):
		try:
			rbTracks = getData(self._url)['collection']
			rbIndexes = { 'availability': 6, 'spotifyId': 7 }

			availableTracks = (
				track[rbIndexes['spotifyId']] for track in rbTracks if track[rbIndexes['availability']] == 4
			)
			return list(availableTracks)
		except Exception:
			print('\nFailed to get Rock Band tracks')
			return []


def getData(url, headers={}):
	try:
		request = Request(url, headers=headers)
		response = urlopen(request)
		data = response.read()
		encoding = response.info().get_content_charset('utf8')
		return loads(data.decode(encoding))
	except Exception:
		print('\nFailed to get data from', url)


def main():

	client_id = 'fcc8cc664f5f448e9c90b265a77118a5'
	client_secret = 'b651409975ea4a129347d1c7c603c070'
	rockbandPlaylistUrl = 'https://rbdb.io/v3/songs?fields=availability,spotifyId&playsOn=rb4&compact=true'
	tlPlaylistUrl = 'https://api.spotify.com/v1/users/robcthegeek/playlists/2JwE2prZ0fdX82d3alpGhQ'

	spotifyUrl = (sys.argv[1]) if len(sys.argv) > 1 else tlPlaylistUrl

	spotify = SpotifyAPI(client_id, client_secret, spotifyUrl)

	spotify.authorise()

	spotify.createUrl()

	spotifyPlaylistName = spotify.getPlaylistName()

	print('\n>> Getting tracks from {0}'.format(spotifyPlaylistName))

	spotifyTracks = spotify.getTracks()

	rockBand = RockBandAPI(rockbandPlaylistUrl)

	rockBandIds = rockBand.getRockBandIds()

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
