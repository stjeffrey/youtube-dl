from __future__ import unicode_literals

from .common import InfoExtractor
from youtube_dl.utils import compat_urllib_request
import youtube_dl.utils

class MSBuildIE(InfoExtractor):
    IE_DESC = 'MS Build 2019'
    #_VALID_URL = r'https?://(mybuild\.)?techcommunity\.microsoft\.com/sessions/(?P<id>[0-9]+)'
    _VALID_URL = r'https://api.mybuild.techcommunity.microsoft.com/api/session/search'
    #_VALID_URL = r'https?://medius.studios.ms/Embed/Video-nc/(?P<id>[A-Z0-9\-]+)'

    _TEST = {
        #'url': 'https://medius.studios.ms/Embed/Video-nc/B19-BDL2046?latestplayer=true',
        'url': 'https://api.mybuild.techcommunity.microsoft.com/api/session/search',
        'md5': '55f5e8981c1c80a64706a44b74833de8',
        'info_dict': {
            'id': 'B19-BDL2046',
            'ext': 'mp4',
            'title': '\'Look Back\' on C#',
            'description': 'Take a C# Historical Journey with Technical Fellow and TypeScript creator, ...',
            'duration': None,
            'upload_date': None,
            'uploader': 'Microsoft'
        },
        'params': {
            # m3u8 download
            'skip_download': True,
        },
        'expected_warnings': ['HTTP Error 404: Not Found'],
    }

    def _real_extract(self, url):
        video_id = 1
        data = '{"itemsPerPage":10,"searchText":"*","searchPage":1,"sortOption":"None","searchFacets":{"facets":[],"personalizationFacets":[],"dateFacet":[{"startDateTime":"2019-05-06T15:00:00.000Z","endDateTime":"2019-05-07T02:44:59.000Z"},{"startDateTime":"2019-05-07T15:00:00.000Z","endDateTime":"2019-05-08T02:44:59.000Z"},{"startDateTime":"2019-05-08T15:00:00.000Z","endDateTime":"2019-05-09T02:44:59.000Z"}]},"recommendedItemIds":[],"favoritesIds":[],"mustHaveOnDemandVideo":True}'.encode('utf-8')
        request = compat_urllib_request.Request(url,data)
        response = compat_urllib_request.urlopen(url, data).read().decode('utf-8')
        
        videos = self._parse_json(response, 1)
        #info_response = self._download_webpage(request, video_id) 
        #video_id = self._match_id(url)
        #webpage = self._download_webpage(url, video_id)
        entries = []
        for video in videos['data']:
            if video['downloadVideoLink'] != '':
                entries.append({
                'id': video['sessionCode'],
                'title': video['title'],
                'description': video['description'],
                'uploader': 'Microsoft',
                'url': video['downloadVideoLink'],
                'ext': 'mp4'
                })

        # entries = [{
        #     '_type': 'url_transparent',
        #     'url': smuggle_url(episode['webplay_url'], {'no_bangumi_tip': 1}),
        #     'ie_key': BiliBiliIE.ie_key(),
        #     'timestamp': parse_iso8601(episode.get('update_time'), delimiter=' '),
        #     'episode': episode.get('index_title'),
        #     'episode_number': int_or_none(episode.get('index')),
        # } for episode in season_info['episodes']]
        # entries = sorted(entries, key=lambda entry: entry.get('episode_number'))

        return self.playlist_result(entries)

        # return {
        #     'id': video_id,
        #     'title': self._og_search_title(webpage),
        #     'description': self._og_search_description(webpage),
        #     'uploader': 'Microsoft',
        #     'url': self._og_search_property('url', webpage),
        #     'ext': 'mp4'
        #     # TODO more properties (see youtube_dl/extractor/common.py)
        # }