from abc import ABCMeta, abstractmethod
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


class API(object):

	__metaclass__ = ABCMeta

	def __init__(self, url):
		self._url = url

	@abstractmethod
	def getData(self, url, headers={}):
		try:
			request = Request(url, headers=headers)
			response = urlopen(request)
			data = response.read()
			encoding = response.info().get_content_charset('utf8')
			return loads(data.decode(encoding))
		except Exception:
			print('\nFailed to get data from', url)


class SpotifyAPI(API):

	def __init__(self, client_id, secret, url):
		self._token = self.authorise((client_id, secret))
		self._url = self.createUrl(url)

	def authorise(self, credentials):
		authUrl='https://accounts.spotify.com/api/token'
		body_params = {'grant_type' : 'client_credentials'}

		response = requests.post(authUrl, data=body_params, auth=credentials)
		return response.json()['access_token']

	def createUrl(self, url):
		try:
			regex = re.compile('(?:(\S+users?\W))(\w+)(\Wplaylists?\W)(\w+)')
			matchObj = re.match(regex, url)

			return 'https://api.spotify.com/v1/users/{0}/playlists/{1}'.format(matchObj.group(2), matchObj.group(4))
		except Exception:
			print('\nIncorrect Spotify URL provided')
			return null;

	def getData(self, url, headers={}):
		return super().getData(url, headers)

	def getPlaylistName(self):
		try:
			data = self.getData(self._url + '?fields=name', {'Authorization': 'Bearer ' + self._token})
			return data['name']
		except Exception:
			return 'Spotify playlist'

	def getTracks(self):
		tracks = []
		params = '/tracks?fields=items(track(id,name,artists(name)),added_by(id)),next'
		url = self._url
		try:
			while url:
				decodedData = self.getData(url + params, {'Authorization': 'Bearer ' + self._token})
				tracks.extend(decodedData['items'])
				url = decodedData['next']
		except Exception:
			print('\nFailed to get Spotify tracks')
		return tracks


class RockBandAPI(API):

	def getData(self, url, headers={}):
		return super().getData(url, headers)

	def getRockBandIds(self):
		try:
			rbTracks = self.getData(self._url)['collection']
			rbIndexes = { 'availability': 6, 'spotifyId': 7 }

			availableTracks = (
				track[rbIndexes['spotifyId']] for track in rbTracks if track[rbIndexes['availability']] == 4
			)
			return list(availableTracks)
		except Exception:
			print('\nFailed to get Rock Band tracks')
			return []


class Matcher:

	def __init__(self, ids, tracks):
		self._ids = ids
		self._tracks = tracks
		self._matches = 0

	def getMatches(self):
		numberOfMatches = self._matches

		for track in self._tracks:
			if any(id == track['track']['id'] for id in self._ids):
				print('\n* {track[name]} by {track[artists][0][name]}. Added by {added_by[id]}.'.format(**track))
				numberOfMatches += 1
		return numberOfMatches


def main():

	client_id = 'fcc8cc664f5f448e9c90b265a77118a5'
	client_secret = 'b651409975ea4a129347d1c7c603c070'
	rockbandPlaylistUrl = 'https://rbdb.io/v3/songs?fields=availability,spotifyId&playsOn=rb4&compact=true'
	tlPlaylistUrl = 'https://api.spotify.com/v1/users/robcthegeek/playlists/2JwE2prZ0fdX82d3alpGhQ'

	spotifyUrl = (sys.argv[1]) if len(sys.argv) > 1 else tlPlaylistUrl

	try:
		spotify = SpotifyAPI(client_id, client_secret, spotifyUrl)
	except Exception:
		print('\nFailed to call Spotify API')
		return

	spotifyPlaylistName = spotify.getPlaylistName()

	print('\n>> Getting tracks from {0}'.format(spotifyPlaylistName))

	spotifyTracks = spotify.getTracks()

	rockBand = RockBandAPI(rockbandPlaylistUrl)

	rockBandIds = rockBand.getRockBandIds()

	matcher = Matcher(rockBandIds, spotifyTracks)

	numberOfMatches = matcher.getMatches()

	if numberOfMatches == 0:
		print('\n** No matches :(')
	else:
		print('\n*** {0} Rock Band tracks found in {1}. ***'.format(numberOfMatches, spotifyPlaylistName)) # pluralisation (1 tracks?)


if __name__ == '__main__':
	main()
