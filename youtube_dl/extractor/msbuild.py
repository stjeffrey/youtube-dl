from __future__ import unicode_literals

from .common import InfoExtractor
import youtube_dl.utils

class MSBuildIE(InfoExtractor):
    IE_DESC = 'MS Build 2019'
    _VALID_URL = r'https?://(mybuild\.)?techcommunity\.microsoft\.com/sessions/(?P<id>[0-9]+)'
    #_VALID_URL = r'https?://medius.studios.ms/Embed/Video-nc/(?P<id>[A-Z0-9\-]+)'

    _TEST = {
        #'url': 'https://medius.studios.ms/Embed/Video-nc/B19-BDL2046?latestplayer=true',
        'url': 'https://mybuild.techcommunity.microsoft.com/sessions/77385?source=sessions#top-anchor',
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
        #youtube_dl.utils.std_headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        youtube_dl.utils.std_headers['User-Agent'] = 'Android'
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        
        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
            'uploader': 'Microsoft',
            'url': self._og_search_property('url', webpage),
            'ext': 'mp4'
            # TODO more properties (see youtube_dl/extractor/common.py)
        }