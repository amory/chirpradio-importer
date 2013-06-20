"""
 from chirpradio-machine: do_dump_new_artists_in_dropbox
"""
import logging

from flask.ext.restful import Resource

from chirp.library import artists, dropbox


class Dropbox(Resource):

    def dump_dropbox(self):
        drop = dropbox.Dropbox()
        tracks = []

        def sort_albums(albums):
            # first sort by title then artist
            result = sorted(albums, key=lambda album: album.get('title'))
            result = sorted(result, key=lambda album: album.get('artist'))
            return result

        for au_file in drop.tracks():
            try:
                tpe1 = au_file.mutagen_id3['TPE1'].text[0] # artist
                tit2 = au_file.mutagen_id3['TIT2'].text[0] # track title
                trck = au_file.mutagen_id3['TRCK'].text[0].split('/')[0] # track number
                talb = au_file.mutagen_id3['TALB'].text[0] # album
                track = {'number': trck, 'title': tit2, 'artist': tpe1, 'album': talb, 'path': au_file.path}
                tracks.append(track)
            except Exception, e:
                tracks.append({'path': au_file.path})
                logging.exception(e)
        albums = []
        album_titles = set(track.get('album') for track in tracks)
        for i, album_title in enumerate(album_titles):
            if album_title:
                album = {'album_id': i+1, 'artist': [], 'title': album_title, 'path': None,
                         'tracks': [], 'path': None, 'messages': [], 'status': None}
                for track in tracks:
                    if track.get('album') == album_title:
                        path = '/'.join(track.get('path').split('/')[:-1])
                        album['path'] = path
                        album['tracks'].append(track)
                        album['artist'].append(track.get('artist'))
                artists_list = list(set(album.get('artist')))
                album['artist'] = artists_list if len(artists_list) > 1 else artists_list[0]
                if type(album.get('artist')) != list:
                    if artists.standardize(album.get('artist')) == None:
                        album['status'] = 'warning'
                        album['messages'].append({'message': "New artist name. Check the artist list", 'status': 'warning'})
                albums.append(album)
        albums = sort_albums(albums)
        return {'albums': albums}

    def get(self):
        return self.dump_dropbox()
