# tl-ldn-rockband

Python3 console program that returns a list of tracks on the TL-LDN-ROX playlist that are playable on [Rock Band](http://www.rockband4.com/) (including as DLC). Also accepts an optional argument of a Spotify public playlist URL, to get matches which are on that playlist. Prints out the Spotify user ID of the person who added each track, to help decide who to nominate as the singer :)

### The Problem
There are a ton of downloadable songs on Rock Band (about 2500). It can be time consuming to search through them all to find your favourite songs! That time could be better spent playing Rock Band and drinking contraband rum.

### The Solution
Download python3 and run dis ting.

Also check out the awesome [Rock Band Database](http://rbdb.online/) which lets you search for and filter tracks by just about everything.

## How to Run

Make sure you have python3 installed. Open up your terminal/windows command thingy, clone this project and type:

```
python3 setup.py install
python3 spotifymatches.py
```

This will list the tracks on the TL-LDN-ROX playlist that are available on Rock Band.

You can also pass the URL of a **public** Spotify playlist as an argument:

```
python3 spotify-matches.py https://open.spotify.com/user/{userId}/playlist/{playlistId}
```

This will list the tracks on your playlist that are available on Rock Band.

To find a Spotify playlist URL:
* Right-click your playlist's name in the Spotify menu bar (or click on the three little dots on the playlist's home screen)
* Hover over `Share` in the context menu and click `Copy Playlist URI`.

Try not to type the URL incorrectly or input a private playlist because the error handling and user input validation are currently pretty crap (sorry, will fix all that soon).

Please Slack me with any bugs or general complaints. This is my first Python project so be nice :)

Enjoy!

## Acknowledgements
Thank you to Darren Doyle for the use of the [rbdb APIs](http://rbdb.online/) and exposing the Spotify IDs.
