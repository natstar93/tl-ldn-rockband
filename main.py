from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import Request
from json import loads

def getTracks(url):
    print('\n>> Getting tracks from {0}'.format(url))
    token = 'Bearer BQC9Jyw32zS1wDHeq0poASw2ohB7RYElexrKlGZfM5f2g8KmrwBtBEFAgUT1vRC8UWM2uXzGzBi0TTfoMyf3O8LeA08tKJeGZzusY8K2ijYTyi2jvaOnbDeSqPFohqHjoJAAf5oyBn1idxjpmWwnaU3ObaH3AJ4oYA'
    try:
        tracks = []
        while url:
            request = Request(url, headers={'Authorization': token})
            response = urlopen(request)
            data = response.read()
            encoding = response.info().get_content_charset('utf8')
            decodedData = loads(data.decode(encoding))
            tracks = tracks + decodedData['items']
            url = decodedData['next']
        return tracks
    except(URLError, e):
        print('Fail', e)

def main():
    tlUrl = 'https://api.spotify.com/v1/users/robcthegeek/playlists/2JwE2prZ0fdX82d3alpGhQ/tracks?fields=items(track(id,name,artists(name)),added_by(id)),next'
    rbUrl = 'https://api.spotify.com/v1/users/rockbandofficial/playlists/1LOZfgjinUc6K2mz8wjPz3/tracks?fields=items(track(id)),next'

    tlTracks = getTracks(tlUrl)
    rbTracks = getTracks(rbUrl)

    rbIds = [track['track']['id'] for track in rbTracks]

    matches = []

    for track in tlTracks:
        if any(rbId == track['track']['id'] for rbId in rbIds):
            matches.append(track)

    for track in matches:
        print('\n\n*** Match: {track[name]} by {track[artists][0][name]}. Added by {added_by[id]}. ***'.format(**track))

    if len(matches) == 0:
        print('** No matches :(')
    else:
        print('*** {0} matches found. ***'.format(len(matches))) # pluralisation !(1 matches)

if __name__ == '__main__':
    main()
