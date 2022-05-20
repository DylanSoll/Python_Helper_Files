from json import loads
from numpy import isin
import requests
from time import strptime, time
def validate_date(date):
    if date == 'latest':
        return 'latest'
    try:
        strptime(date, '%Y-%m-%d')
    except ValueError:
        return 'latest'
    return date

class spotifyMusicHandler:
    def __init__(self, API_key): 
        """Create handler for spotify api

        Args:
            API_key (string): API key for spoitfy
        """        
        self.SEARCH_OPTIONS = {'albums', 'artists', 'episodes', 'genres', 'playlists', 'podcasts', 'tracks', 'users', 'multi'}
        self.VALID_COUNTRY_CODES = {'global', 'us', 'gb', 'ae', 'ar', 'at', 'au', 'be', 'bg', 'bo', 'br', 'by', 'ca', 'ch', 'cl' ,'co'
        'cr', 'cy', 'cz', 'de', 'dk', 'do', 'ec', 'ee', 'eg', 'es', 'fi', 'fr', 'gr', 'gt', 'hk', 'hn', 'hu', 'id', 'ie', 'il',
        'in', 'is', 'it', 'jp', 'kr', 'kz', 'lt', 'lu', 'lv', 'ma', 'mx', 'my', 'ng', 'ni', 'nl', 'no', 'nz', 'pa', 'pe', 'ph',
        'pl', 'pt', 'py', 'ro', 'ru', 'sa', 'se', 'sg', 'sk', 'sv', 'th', 'tr', 'tw', 'ua', 'uy', 've', 'vn', 'za'}

        self.URL = "https://spotify23.p.rapidapi.com" #base URL
        self.headers = { #creates headers param
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com", 
            "X-RapidAPI-Key": API_key
        }
        return

    def get_info(self, URL, HTTPmethod, parameters):
        """A general function to connect to the spotify API

        Args:
            URL (str): ending URL of the spotify api target
            HTTPmethod (str): HTTP method to send to server 'GET' OR 'POST ETC.
            parameters (dict): Parameters to pass along to API

        Returns:
            dict: {results, duration}
        """            
        init_time = time() #starts initial time
        response = requests.request(HTTPmethod, str(self.URL + URL), headers=self.headers, params=parameters)
        duration = time() - init_time #calculates the duration      
        return {'results':loads(response.text), 'duration': duration} #returns a dict of duration and results

    def get_options(self):
        """Get a dictionary of valid option types for the API

        Returns:
            dict: Dicitonary of available options.
        """        
        options_dict = {
            'search_options': self.SEARCH_OPTIONS,
            'country_codes': self.VALID_COUNTRY_CODES,
        } #creates a dictionary of all the diffent options
        return options_dict

    def get_tracks(self, tracksID):
        """Get tracks, can do multiple tracks if tracksID entered like id1,id2,id3

        Args:
            tracksID (str): ids of tracks data to be retrieved

        Returns:
            dict: returned data and duration
        """        
        if not isinstance(tracksID, str): #makes sure it is a string
            return False #otherwise exit function and say no results
        tracksID = tracksID.replace(' ', '') #removes all white spaces
        return self.get_info('/tracks/', 'GET', {"ids":tracksID}) #returns the dict generated by self.get_info()

    def get_track_credits(self, trackID):
        """Gets the track credits from the id

        Args:
            tracksID (str): single id for a song

        Returns:
            dict: Dictionary of results and duration
        """        
        if not isinstance(trackID, str): #same as get_tracks
            return False
        return self.get_info('/track_credits/', 'GET', {"id":trackID})

    def get_track_lyrics(self, trackID):
        """Gets the track lyrics from the id

        Args:
            tracksID (str): single id for a song

        Returns:
            dict: Dictionary of results and duration
        """        
        if not isinstance(trackID, str): #same as get_tracks
            return False
        return self.get_info('/track_lyrics/', 'GET', {"id":trackID})
    
    def get_all_track_data(self, trackID):
        """Get all available trackdata from the trackID

        Args:
            trackID (str): Specific and single trackID

        Returns:
            dict: dictionary of all results
        """        
        if not isinstance(trackID, str): #ensures trackID is string
            return False #otherwise return no data
        init_time = time() #create start time
        track_data = self.get_info('/tracks/', 'GET', {"ids":trackID} ) #generate basic track data
        track_credits = self.get_info('/track_credits/', 'GET', {"id":trackID}) #generate track credits
        track_lyrics = self.get_info('/track_lyrics/', 'GET', {"id":trackID}) #generates track lyrics
        track_data['results']['tracks'][0]['credits'] = track_credits['results']['credits'] #inserts data into main dict
        track_data['results']['tracks'][0]['lyrics'] = track_lyrics['results']['lyrics'] #inserts data into main dict
        track_data['duration'] = (time()-init_time) #updates duration
        return track_data

    def get_from_search(self, query, query_type = "multi",offset = 0, limit = 20, num_top_results = 5):
        """Gets data from search query

        Args:
            query (str): Search value
            query_type (str, optional): query type. Options: albums, artists, episodes, genres, playlists, podcasts, tracks, users or multi. Defaults to "multi".
            offset (int, optional): position search starts in. Defaults to 0 (first result).
            limit (int, optional): limit of results. Defaults to 20.
            num_top_results (int, optional): Number of top results to show. Defaults to 5.

        Returns:
            dict: dict of results and duration 
        """                
        #convert query string to URL friendly format
        if not isinstance(query, str):
            return False
        sanitised_query = query.strip() #removes all trailing white space
        if query_type not in self.SEARCH_OPTIONS:
            query_type = 'multi'  #reverts to default option
        
        querystring = {"q":sanitised_query,"type":query_type,"offset":offset,"limit":limit,"numberOfTopResults":num_top_results}
        return self.get_info('/search', 'GET', querystring)
    
    def get_from_search_with_preview(self, query, query_type = "multi",offset = 0, limit = 20, num_top_results = 5):
        """Gets data from search query

        Args:
            query (str): Search value
            query_type (str, optional): query type. Options: albums, artists, episodes, genres, playlists, podcasts, tracks, users or multi. Defaults to "multi".
            offset (int, optional): position search starts in. Defaults to 0 (first result).
            limit (int, optional): limit of results. Defaults to 20.
            num_top_results (int, optional): Number of top results to show. Defaults to 5.

        Returns:
            dict: dict of results and duration 
        """                
        init_time = time()
        track_list = self.get_from_search(query_type, query_type, offset, limit,num_top_results)['results']['tracks']['items']
        id_list = [] #creates blank list

        for item in track_list: #adds all id to a list
            id_list.append(item['data']['id'])
        ids_str = ','.join(id_list) #uses join to make a single string of ids
        tracks = self.get_tracks(ids_str) #gets all track data
        tracks['duration'] = str(init_time - time()) #updates duration
        return tracks #returns the data

    def get_albums(self, albumsID):
        """Get albums, can do multiple albums if albumsID entered like id1,id2,id3

        Args:
            albumsID (str): ids of albums data to be retrieved

        Returns:
            dict: returned data and duration
        """        
        if not isinstance(albumsID, str): #makes sure it is a string
            return False #otherwise exit function and say no results
        albumsID = albumsID.replace(' ', '') #removes all white spaces
        return self.get_info('/albums/', 'GET', {"ids":albumsID}) #returns the dict generated by self.get_info()

    def get_album_tracks(self, albumID, offset = 0, limit = 300):
        """Gets the album tracks from the AlbumID

        Args:
            albumID (str): ID of the album
            offset (int, optional): Starting position of tracks to be returned. Defaults to 0.
            limit (int, optional): Limit on tracks returned. Defaults to 300.

        Returns:
            dict: the data in a dictionary, keys are 'results' and 'duration'
        """         
        if not isinstance(albumID, str): #makes sure it is a string
            return False #otherwise exit function and say no results
        albumID = albumID.replace(' ', '') #removes all white spaces
        querystring = {"id":albumID,"offset":offset,"limit":limit}
        return self.get_info('/album_tracks/', 'GET', querystring) #returns the dict generated by self.get_info()

    def get_album_metadata(self, albumID):
        """Get albums metadata from ID

        Args:
            albumsID (str): id of album data to be retrieved

        Returns:
            dict: returned data and duration
        """        
        if not isinstance(albumID, str): #makes sure it is a string
            return False #otherwise exit function and say no results
        albumID = albumID.replace(' ', '') #removes all white spaces
        return self.get_info('/album_metadata/', 'GET', {"id":albumID}) #returns the dict generated by self.get_info()

    def get_charts(self, chart_type = 'regional', country = 'global', recurrence = 'daily', date = "latest"):
        """Gets the chart for a region, on a time frame

        Args:
            chart_type (str, optional): Regional or viral chart. Defaults to 'regional'.
            country (str, optional): Country code of charts. see self.VALID_COUNTRY_CODES. Defaults to 'global'.
            recurrence (str, optional): Size of the charts. Refreshes daily or weekly. Defaults to 'daily'.
            date (str, optional): Date of chart -- latest for live. Format is 'YYYY-MM-DD'. Defaults to "latest".

        Returns:
            dict: dict of response and duration
        """        
        if chart_type not in ['viral', 'regional']:
            chart_type = 'regional' #ensures the type is valid
        if country not in self.VALID_COUNTRY_CODES:
            country = 'global' #ensures the country charts are valid
        if recurrence not in ['daily', 'weekly']: 
            recurrence = 'daily'#ensures the recurrence is correct
        date = validate_date(date)
        querystring = {"type":chart_type,"country":country,"recurrence":recurrence,"date":date} 
        return self.get_info('/charts/', 'GET', querystring) #returns the dict generated by self.get_info()

    def get_radio_playlist(self, radio_id, radio_type="artist"):
        """Gets radio playlist

        Args:
            radio_id (str): id of radio (user or track id)
            radio_type (str, optional): playlist type -- "artist" or "track". Defaults to "artist".

        Returns:
            dict: dict of response and duration
        """        
        if radio_type not in ['artist', 'track']: #ensures radio_type is valid
            radio_type = 'artist'
        uri = f"spotify:{radio_type}:{radio_id}" #creates URI for the API
        return self.get_info('/seed_to_playlist/', 'GET', {'uri':uri}) #returns the dict generated by self.get_info()

    def get_user_profile(self, userID, playlist_limit = 10, artist_limit = 10):
        """Get the profile data of a user

        Args:
            userID (str): ID of the user
            playlist_limit (int, optional): limit of playlists returned. Defaults to 10.
            artist_limit (int, optional): limit of artists returned. Defaults to 10.

        Returns:
            dict: dict of response and duration
        """        
        try:
            int(playlist_limit) #tries to convert playlist limit to int
        except:
            playlist_limit = 10 #if error, must me invalid, redefine
        try:
            int(artist_limit) #repeat for artist_limit
        except:
            artist_limit = 10
        querystring = {"id":userID,"playlistLimit":playlist_limit,"artistLimit":artist_limit} #generates query strict
        return self.get_info('/user_profile/', 'GET', querystring) #returns the dict generated by self.get_info()

    def get_user_followers(self, userID):
        """Get the following data of a user

        Args:
            userID (str): ID of the user

        Returns:
            dict: dict of results and duration
        """        
        if not isinstance(userID, str):
            return False #ensures userid is a string
        return self.get_info('/user_followers/', 'GET', {"id":userID}) #returns the dict generated by self.get_info()

if __name__ == '__main__':    
    SPOTIFY = spotifyMusicHandler('YOUR KEY HERE')
    print(SPOTIFY.get_albums('3IBcauSj5M2A6lTeffJzdv,3IBcauSj5M2A6lTeffJzdv'))
