import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

class MySpotify:

    # Initialize Spotify object
    def __init__(self, client_id, client_secret, redirect_uri, username):
        print(datetime.now(), 'Initializing Spotify object (' + username + ')...')
        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri
        self.username = username
        self.scope = ''
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope, username=self.username))
        self.user_id = self.sp.me()['id']
        self.timezone_offset = -6
        self.playlists = defaultdict(set)
        self.play_history_filename = self.username + '_play_history.json'
        self.saved_tracks_filename = self.username + '_saved_tracks.json'
        self.init_scopes()
        self.init_play_history_file()
        self.init_saved_tracks_file()
        print(datetime.now(), 'Initializing Spotify object (' + username + ') completed.')

    def add_scope(self, scope):
        self.scope += str(scope).strip() + ' '

    def init_scopes(self):
        self.add_scope('user-library-read')
        self.add_scope('user-library-modify')
        self.add_scope('user-top-read')
        self.add_scope('user-read-recently-played')
        self.add_scope('playlist-modify-public')
        self.add_scope('playlist-modify-private')

    def init_play_history_file(self):
        if not os.path.exists(self.play_history_filename):
            print("Creating play history file '" + self.play_history_filename + "'.")
            with open(self.play_history_filename, 'w') as file_obj:
                output = {
                    "last_updated": "2000-01-01 00:00:00",
                    "play_history": []
                }
                json.dump(output, file_obj)
                file_obj.close()

    def init_saved_tracks_file(self):
        if not os.path.exists(self.saved_tracks_filename):
            print("Creating saved tracks file '" + self.saved_tracks_filename + "'.")
            with open(self.saved_tracks_filename, 'w') as file_obj:
                output = {
                    "last_updated": "2000-01-01 00:00:00",
                    "saved_tracks": []
                }
                json.dump(output, file_obj)
                file_obj.close()

    def load_playlists(self, stop_at=None):
        # get all spotify playlists and store them in dictionary 'self.playlists'
        i = 0
        playlists = self.sp.user_playlists(self.user_id, offset=i)['items']
        while playlists:
            for playlist in playlists:
                playlist_id = playlist['id']
                playlist_name = playlist['name']
                self.playlists[playlist_name].add(playlist_id)
                if playlist_name == stop_at:
                    return
                i += 1
            playlists = self.sp.user_playlists(self.user_id, offset=i)['items']

    def create_playlist(self, playlist_name):
        self.sp.user_playlist_create(self.user_id, playlist_name)
        self.load_playlists(stop_at=playlist_name)

    def get_playlist_names_based_on_date(self, date):
        year = str(date.year)
        month = date.strftime('%B')[:3]
        playlist_name_year = year
        playlist_name_month = year + ' - ' + month
        return {
            'month': playlist_name_month,
            'year': playlist_name_year,
            'all': 'All Songs'
        }

    def add_track_to_playlist(self, track_uri, playlist_name):
        playlist_ids = self.playlists[playlist_name]
        for playlist_id in playlist_ids:
            self.sp.playlist_add_items(playlist_id, [track_uri])

    def datetime_str_to_datetime_obj(self, datetime_string, offset=0):
        datetime_string = datetime_string.split('.')[0]         # Remove milliseconds
        datetime_string = datetime_string.split('Z')[0]         # Remove 'Z'
        datetime_string = datetime_string.replace('T', ' ')     # Replace 'T' with a space
        datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
        datetime_obj = self.adjust_timezone(datetime_obj, offset)
        return datetime_obj

    def adjust_timezone(self, x, hour_offset):
        return x + timedelta(hours=hour_offset)

    def get_saved_albums(self):
        results = []
        i = 0
        items = self.sp.current_user_saved_albums(limit=20, offset=i)['items']
        while items:
            for item in items:
                results.append(item)
                i += 1
                if i == 10: break
            items = self.sp.current_user_saved_albums(limit=20, offset=i)['items']

        track_uris = []
        for result in results:
            tracks = result['album']['tracks']['items']
            for track in tracks:
                track_uri = track['uri']
                track_uris.append(track_uri)

        i, j = 0, 100
        add_items = track_uris[i:j]
        while add_items:
            self.sp.playlist_add_items('spotify:playlist:6wdSWzbkdZbHnGa4mkg5AO', add_items)
            i = j
            j += 100
            add_items = track_uris[i:j]

    def update_play_history(self, show_log=True, return_output=False):

        print(datetime.now(), 'Updating play history...')

        # Open play history file
        with open(self.play_history_filename, 'r') as json_obj:
            contents = json.load(json_obj)
        last_updated = self.datetime_str_to_datetime_obj(contents['last_updated'])
        play_history = contents['play_history']

        # Get recently played tracks
        recently_played = self.sp.current_user_recently_played()
        recently_played = recently_played['items']
        recently_played = reversed(recently_played)

        # Add recently played tracks to play history
        i = 1
        for item in recently_played:

            # Get recently played track details
            track_uri = item['track']['uri']
            played_at = self.datetime_str_to_datetime_obj(item['played_at'], offset=self.timezone_offset)
            artist = item['track']['artists'][0]['name']
            track = item['track']['name']

            # Skip previously saved tracks
            if played_at <= last_updated:
                continue

            # Add new track
            track_details = {
                'played_at': str(played_at),
                'track_uri': track_uri,
                'artist': artist,
                'track': track
            }
            play_history.append(track_details)
            last_updated = played_at
            if show_log:
                print(datetime.now(), i, 'Recently Played:' + track_details)
            i += 1

        # Write play history to file
        output = {
            'last_updated': str(last_updated),
            'play_history': play_history
        }

        with open(self.play_history_filename, 'w') as file_obj:
            json.dump(output, file_obj)
            file_obj.close()

        print(datetime.now(), 'Updating play history completed.')

        # Optionally return a list of results
        if return_output:
            return output

    def show_play_history(self):
        with open(self.play_history_filename, 'r') as file_obj:
            contents = json.load(file_obj)
        for n, item in enumerate(contents['play_history'], start=1):
            print(n, item)

    def update_auto_playlist(self, target_playlist, source_playlists=None, days=None):

        print(datetime.now(), 'Updating auto playlist (' + target_playlist + ')...')

        # Get tracks on target playlist
        in_playlist = defaultdict(bool)
        i = 0
        playlist_items = self.sp.playlist_items(target_playlist, limit=100, offset=i)
        playlist_total = playlist_items['total']
        while i < playlist_total:
            for p in playlist_items['items']:
                in_playlist[p['track']['uri']] = True
                i += 1
            playlist_items = self.sp.playlist_items(target_playlist, limit=100, offset=i)

        # Get play history
        play_history = self.update_play_history(show_log=False, return_output=True)['play_history']

        # Create list of tracks to remove
        is_recently_played = defaultdict(bool)
        remove_tracks_list = []
        i = 1
        for p in play_history:

            # Skip not recently played tracks, defined by day window (if provided)
            played_at = self.datetime_str_to_datetime_obj(p['played_at'])
            if days and played_at.date() < date.today() - timedelta(days):
                continue

            # Add recently played tracks to remove list
            is_recently_played[p['track_uri']] = True
            if in_playlist[p['track_uri']]:
                in_playlist[p['track_uri']] = False
                remove_tracks_list.append(p['track_uri'])
                print(datetime.now(), i, 'Removed:', p)
                i += 1

        # Remove tracks from target playlist
        i, j = 0, 100
        remove_tracks = remove_tracks_list[i:j]
        while remove_tracks:
            self.sp.playlist_remove_all_occurrences_of_items(target_playlist, remove_tracks)
            i = j
            j += 100
            remove_tracks = remove_tracks_list[i:j]

        # Get tracks to add to target playlist
        add_tracks_list = []
        i = 0
        j = 1
        saved_tracks = self.sp.current_user_saved_tracks(limit=50, offset=i)['items']
        while saved_tracks:
            for saved_track in saved_tracks:
                i += 1
                track_uri = saved_track['track']['uri']
                if track_uri.find('spotify:track:') == -1:
                    continue
                if is_recently_played[track_uri] or in_playlist[track_uri]:
                    continue
                add_tracks_list.append(track_uri)
                in_playlist[track_uri] = True
                track_info = {
                    'track_uri': track_uri,
                    'artist': saved_track['track']['artists'][0]['name'],
                    'track': saved_track['track']['name']
                }
                print(datetime.now(), j, 'Added:', track_info)
                j += 1
            saved_tracks = self.sp.current_user_saved_tracks(limit=50, offset=i)['items']

        # Get tracks from other playlists to add
        while source_playlists:
            source_playlist = source_playlists.pop(0)
            playlist_items = self.sp.playlist_items(source_playlist, limit=100, offset=i)
            playlist_total = playlist_items['total']
            i = 0
            while i < playlist_total:
                for item in playlist_items['items']:
                    i += 1
                    track_uri = item['track']['uri']
                    if track_uri.find('spotify:track:') == -1:
                        continue
                    if is_recently_played[track_uri] or in_playlist[track_uri]:
                        continue
                    add_tracks_list.append(track_uri)
                    in_playlist[track_uri] = True
                    track_info = {
                        'track_uri': track_uri,
                        'artist': item['track']['artists'][0]['name'],
                        'track': item['track']['name']
                    }
                    print(datetime.now(), j, 'Added:', track_info)
                    j += 1
                playlist_items = self.sp.playlist_items(source_playlist, limit=100, offset=i)

        # Add tracks to target playlist.
        i, j = 0, 100
        add_tracks = add_tracks_list[i:j]
        while add_tracks:
            self.sp.playlist_add_items(target_playlist, add_tracks)
            i = j
            j += 100
            add_tracks = add_tracks_list[i:j]

        print(datetime.now(), 'Updating auto playlist (' + target_playlist + ') completed.')

    def update_saved_tracks(self):

        print(datetime.now(), 'Updating saved tracks...')

        self.load_playlists()

        # Init playlist buckets.
        playlist_months = defaultdict(str)
        playlist_years = defaultdict(str)
        playlist_all = defaultdict(str)

        # Open saved tracks json file.
        with open(self.saved_tracks_filename, 'r') as json_obj:
            contents = json.load(json_obj)
        last_updated = self.datetime_str_to_datetime_obj(contents['last_updated'])
        saved_tracks = contents['saved_tracks']

        new_saved_tracks = []
        new_last_updated = last_updated
        i = 0
        j = 1
        stop = False
        saved_tracks_list = self.sp.current_user_saved_tracks(limit=50, offset=i)['items']
        while saved_tracks_list and not stop:
            for saved_track in saved_tracks_list:
                i += 1
                track_uri = saved_track['track']['uri']
                added_at = self.datetime_str_to_datetime_obj(saved_track['added_at'], offset=self.timezone_offset)

                if track_uri.find('spotify:track:') == -1:
                    # Skip items that don't have the spotify track prefix.
                    continue

                if added_at <= last_updated:
                    # Stop when all new saved tracks have been seen.
                    stop = True
                    break

                track_info = {
                    'added_at': str(added_at),
                    'track_uri': track_uri,
                    'artist': saved_track['track']['artists'][0]['name'],
                    'track': saved_track['track']['name']
                }

                # Add track to saved tracks json file.
                new_saved_tracks.append(track_info)
                if added_at > new_last_updated:
                    new_last_updated = added_at

                # Assign to playlists by added_at date.
                playlists = self.get_playlist_names_based_on_date(added_at)
               

                print(datetime.now(), j, 'Saved Track:', track_info)
                j += 1

            # Move on to next chunk of saved tracks in Spotify.
            saved_tracks_list = self.sp.current_user_saved_tracks(limit=50, offset=i)['items']

        # Prepare final output for file.
        new_saved_tracks.reverse()
        output = {
            'last_updated': str(new_last_updated),
            'saved_tracks': saved_tracks + new_saved_tracks
        }

        # Write to json file.
        with open(self.saved_tracks_filename, 'w') as file_obj:
            json.dump(output, file_obj)
            file_obj.close()

        print(datetime.now(), 'Updating saved tracks completed.')

    def add_saved_tracks_to_playlist(self, target_playlist):

        print(datetime.now(), 'Adding saved tracks to playlist (' + target_playlist + ')...')

        # Get tracks on target playlist.
        in_playlist = defaultdict(bool)
        i = 0
        playlist_items = self.sp.playlist_items(target_playlist, limit=100, offset=i)
        playlist_total = playlist_items['total']
        while i < playlist_total:
            for p in playlist_items['items']:
                in_playlist[p['track']['uri']] = True
                i += 1
            playlist_items = self.sp.playlist_items(target_playlist, limit=100, offset=i)

        # Get saved tracks.
        with open(self.saved_tracks_filename, 'r') as json_obj:
            contents = json.load(json_obj)
        saved_tracks = contents['saved_tracks']

        # Create a list of saved tracks, removing duplicates.
        saved_track_list = []
        for saved_track in saved_tracks:
            if not in_playlist[saved_track['track_uri']]:
                saved_track_list.append(saved_track['track_uri'])
        saved_track_set = set(saved_track_list)
        saved_track_list = list(saved_track_set)
        print(datetime.now(), 'Added:', len(saved_track_list))

        # Add tracks to target playlist.
        i, j = 0, 100
        add_tracks = saved_track_list[i:j]
        while add_tracks:
            self.sp.playlist_add_items(target_playlist, add_tracks)
            i = j
            j += 100
            add_tracks = saved_track_list[i:j]

        print(datetime.now(), 'Adding saved tracks to playlist (' + target_playlist + ') completed.')





def update_playlists():

    global dave_spotify

    # Update play history and auto playlist.
    dave_spotify.update_auto_playlist('target_playlist', days=90)  # DETAILS REMOVED FOR PRIVACY

    # Update saved tracks and add them to saved track archive playlist.
    dave_spotify.update_saved_tracks()
    dave_spotify.add_saved_tracks_to_playlist('target_playlist')  # DETAILS REMOVED FOR PRIVACY

    print(datetime.now(), 'Done.\n')

# Create Spotify object.
dave_spotify = MySpotify('client_id', 'client_secret', 'redirect_uri', 'username')  # DETAILS REMOVED FOR PRIVACY

# Repeat by the hour.
update_playlists()
scheduler = BlockingScheduler()
scheduler.add_job(update_playlists, 'interval', hours=1)
scheduler.start()
