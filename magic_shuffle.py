import spotipy

if __name__ == '__main__':
    # Connect to Spotify.
    scope = 'user-modify-playback-state'
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Retrieve all tracks in the playlist.
    uri = '1vwZPe9NJDYdDIF176jCjI' # Delftse Hout
    playlist = sp.playlist_tracks(uri)
    playlist_items = playlist['items']
    while playlist['next']:
        playlist = sp.next(playlist)
        playlist_items.extend(playlist['items'])

    # Retrieve tracks per user.
    tracks_per_user = {}
    for pl_item in playlist_items:
        user_id = pl_item['added_by']['id']
        track_id = pl_item['track']['id']
        track_name = pl_item['track']['name']

        if user_id not in tracks_per_user:
            tracks_per_user[user_id] = set()
        tracks_per_user[user_id].add((track_id, track_name))

    # Retrieve the display names for each user ID.
    user_names = {
        user_id: sp.user(user_id)['display_name']
        for user_id in tracks_per_user
    }

    # Per iteration, add a single track per user to the queue.
    iterations = 5
    for i in range(iterations):
        print(f'[Iteration {i}]')
        for user_id in tracks_per_user:
            tracks = tracks_per_user[user_id]
            user_name = user_names[user_id]
            if len(tracks) > 0:
                track_id, track_name = tracks.pop()
                print(f'Adding {user_name}\'s track: {track_name}')
                sp.add_to_queue(track_id)
        print()