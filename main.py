from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import Request
from json import loads

def getTracks(url):
    print('\n>> Getting tracks from {0}'.format(url))
    token = 'Bearer BQAHUlzhOtl_9NLFCXVdb2tmOB69nfB5_tlwrod17Y8axtoa0iyQHH9HYaPtjGd9bAkbwJ1910xiUCnXq7KXRn8zWrSGA8HXm3qMsZVLvuIJQ9fYIpNkPInsZ88XeKkl3lEKR32OX_dBwdo-k1l25CNghqJlPNCqDQ'
    request = Request(url, headers={'Authorization': token})
    try:
        response = urlopen(request)
        data = response.read()
        encoding = response.info().get_content_charset('utf8')
        decodedData = loads(data.decode(encoding))
        return decodedData['items']
    except(URLError, e):
        print('Fail', e)

def main():
    tlUrl = 'https://api.spotify.com/v1/users/robcthegeek/playlists/2JwE2prZ0fdX82d3alpGhQ/tracks?fields=items(track(id,name,artists(name)),added_by(id)),next&offset=00'
    rbUrl = 'https://api.spotify.com/v1/users/rockbandofficial/playlists/1LOZfgjinUc6K2mz8wjPz3/tracks?fields=items(track(id)),next&offset=600'

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
