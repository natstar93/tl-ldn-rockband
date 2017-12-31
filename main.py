from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import Request
import urllib.parse
from json import loads
import http.client
import http.server
import webbrowser
import re

class SpotifyAPI:
	def __init__(self, auth):
		self._auth = auth

	def getTracks(self, url):
		print('\n>> Getting tracks from {0}'.format(url))
		try:
			tracks = []
			while url:
				request = Request(url, headers={'Authorization': 'Bearer ' + self._auth})
				response = urlopen(request)
				data = response.read()
				encoding = response.info().get_content_charset('utf8')
				decodedData = loads(data.decode(encoding))
				tracks.extend(decodedData['items'])
				url = decodedData['next']
			return tracks
		except(URLError, e):
			print('Fail', e)

	@staticmethod
	def webAuthorize(client_id):
		webbrowser.open('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode({
			'response_type': 'token',
			'client_id': client_id,
			'scope': '',
			'redirect_uri': 'http://127.0.0.1:{}/redirect'.format(SpotifyAPI._SERVER_PORT)
		}))

		server = SpotifyAPI._AuthorizationServer('127.0.0.1', SpotifyAPI._SERVER_PORT)
		try:
			while True:
				server.handle_request()
		except SpotifyAPI._Authorization as auth:
			return SpotifyAPI(auth.access_token)

	_SERVER_PORT = 43019

	class _AuthorizationServer(http.server.HTTPServer):
		def __init__(self, host, port):
			http.server.HTTPServer.__init__(self, (host, port), SpotifyAPI._AuthorizationHandler)

		def handle_error(self, request, client_address):
			raise

	class _AuthorizationHandler(http.server.BaseHTTPRequestHandler):
		def do_GET(self):
			if self.path.startswith('/redirect'):
				self.send_response(200)
				self.send_header('Content-Type', 'text/html')
				self.end_headers()
				self.wfile.write(b'<script>location.replace("token?" + location.hash.slice(1));</script>')

			elif self.path.startswith('/token?'):
				self.send_response(200)
				self.send_header('Content-Type', 'text/html')
				self.end_headers()
				self.wfile.write(b'<script>close()</script>Thanks! You may now close this window.')
				raise SpotifyAPI._Authorization(re.search('access_token=([^&]*)', self.path).group(1))

			else:
				self.send_error(404)

		def log_message(self, format, *args):
			pass

	class _Authorization(Exception):
		def __init__(self, access_token):
			self.access_token = access_token

def main():
    spotify = SpotifyAPI.webAuthorize(client_id='fcc8cc664f5f448e9c90b265a77118a5')

    tlPlaylistUrl = 'https://api.spotify.com/v1/users/robcthegeek/playlists/2JwE2prZ0fdX82d3alpGhQ/tracks?fields=items(track(id,name,artists(name)),added_by(id)),next'
    rbPlaylistUrl = 'https://api.spotify.com/v1/users/rockbandofficial/playlists/1LOZfgjinUc6K2mz8wjPz3/tracks?fields=items(track(id)),next'

    tlTracks = spotify.getTracks(tlPlaylistUrl)
    rbTracks = spotify.getTracks(rbPlaylistUrl)

    rbIds = [track['track']['id'] for track in rbTracks]

    matches = []

    for tlTrack in tlTracks:
        if any(rbId == tlTrack['track']['id'] for rbId in rbIds):
            matches.append(tlTrack)

    for track in matches:
        print('\n*** Match: {track[name]} by {track[artists][0][name]}. Added by {added_by[id]}.'.format(**track))

    if len(matches) == 0:
        print('\n** No matches :(')
    else:
        print('\n*** {0} matches found. ***'.format(len(matches))) # pluralisation (1 matches?)

if __name__ == '__main__':
    main()
