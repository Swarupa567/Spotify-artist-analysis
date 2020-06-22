import os, time
import sys
import json
import spotipy
import pandas
import spotipy.util as util
from json.decoder import JSONDecodeError

t0 = time.time() # Initial timestamp

# Get the username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

client_id = input("Please input your client_id: ")
client_secret = print("Please input your client_secret:")

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope, client_id='',client_secret='',redirect_uri='https://www.google.com/') # add client_id, client_secret
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope, client_id='',client_secret='',redirect_uri='https://www.google.com/') # add client_id, client_secret

# Artists for the analysis
artists = ['Taylor Swift', 'Ariana Grande', 'Shawn Mendes', 'Maroon 5', 'Adele', 'Twenty One Pilots', 'Ed Sheeran', 'Justin Timberlake', 'Charlie Puth','Mumford & Sons',
    'Lorde', 'Linkin Park', 'Lana Del Rey', 'James Arthur',
    'Kendrick Lamar', 'Post Malone', 'Queen', 'Kanye West', 'Eminem', 'Future', 'Snoop Dogg', 'Macklemore', 'Jay-Z',
    'Bruno Mars', 'Beyoncé', 'Drake', 'Stevie Wonder', 'John Legend', 'The Weeknd', 'Rihanna', 'Michael Jackson',
    'Kygo', 'The Chainsmokers', 'Illenium', 'Marshmello', 'Avicii', 'Martin Garrix', 'Eden', 'Prince',
    'Coldplay', 'Elton John', 'OneRepublic', 'Jason Mraz', 'Metallica', 'The Beatles', 'Guns N\' Roses',
    'Frank Sinatra', 'Michael Bublé', 'Norah Jones', 'David Bowie']

# Initialize empty dataframe with columns
allfeatures = pandas.DataFrame(columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'duration_ms', 'time_signature'])

# Create our spotify object with permissions
sp = spotipy.Spotify(auth=token)

# Print user info
user = sp.current_user()
name = user['display_name'].split(' ')
followers = user['followers']['total']
print('Welcome %s to the Spotify API!' %(str(name[0])))
print('You have %d followers.' %(followers))

print('\nSearching for playlists...\n\n')


def time_it():
    t1 = time.time()
    print("Total time for the operation: %fsec\n" %(t1-t0))

# Search playlist_id for This Is playlist of the artist from search results.
def search_playlist(result, query):
    if str.lower(result['playlists']['items'][0]['name']) == str.lower(query) and result['playlists']['items'][0]['owner']['id'] == 'spotify':
        playlist_id = result['playlists']['items'][0]['id']
        print("Found playlist - " + searchq)
        return playlist_id
    else:
        print("Playlist not found for " + (str(artists[i])), end='\n')

for i in range(len(artists)):    
    track_ids = []
    searchq = "This Is " + artists[i]
    search_result = sp.search(searchq, type="playlist")     # Search Spotify for This Is playlist of the artist
    playlist_id = search_playlist(search_result, searchq)   # Get playlist_id 

    playlist_content = sp.user_playlist_tracks('spotify', playlist_id=playlist_id)  # Get tracks info from the playlist_id
    
    for j, t in enumerate(playlist_content['items']):   # Loop through track items and generate track_ids list
        track_ids.append(t['track']['id'])
        
    audio_feat = sp.audio_features(tracks=track_ids)    # Get audio features from track_ids
    aud = pandas.DataFrame(data=audio_feat)     # Insert into dataframe
    aud_mean = aud.mean()   # Mean of all features of 'This Is artist' tracks to get a summary of artist
    allfeatures = pandas.DataFrame.append(allfeatures, aud_mean, ignore_index=True)     # Append all summaries of artists to single dataframe
    print("#%d. Audio features for %s extracted.\n" %(i+1,artists[i]))

allfeatures = allfeatures.set_index([pandas.Index(artists)])    # Set index of features from artists list
# print(allfeatures.head())

allfeatures.to_csv('audio_features.csv',sep=',')    # Save dataframe to CSV to perform analysis in ipynb
print("\n\nData saved to audio_features.csv\n")
time_it()