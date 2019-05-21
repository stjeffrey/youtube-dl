from __future__ import unicode_literals

from .common import InfoExtractor

class MSBuildIE(InfoExtractor):
    IE_DESC = 'MS Build 2019'
    _VALID_URL = r'https?://(mybuild\.)?techcommunity\.microsoft\.com/sessions/(?P<id>[0-9]+)'

    _TEST = {
        'url': 'https://mybuild.techcommunity.microsoft.com/sessions/77385?source=sessions#top-anchor',
        'md5': '55f5e8981c1c80a64706a44b74833de8',
        'info_dict': {
            'id': '77385',
            'ext': 'mp4',
            'title': '\'Look Back\' on C#',
            'description': 'Take a C# Historical Journey with Technical Fellow and TypeScript creator, Anders Hejlsberg.',
            'duration': 1181,
            'upload_date': '20140124',
        },
        'params': {
            # m3u8 download
            'skip_download': True,
        },
        'expected_warnings': ['HTTP Error 404: Not Found'],
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # TODO more code goes here, for example ...
        title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')

        return {
            'id': video_id,
            'title': title,
            'description': self._og_search_description(webpage),
            'uploader': 'Microsoft'
            # TODO more properties (see youtube_dl/extractor/common.py)
        }