from __future__ import unicode_literals

from .common import InfoExtractor
from youtube_dl.utils import (
    compat_urllib_request,
    urlencode_postdata
)
import youtube_dl.utils
import re
import hashlib

class IdelloIE(InfoExtractor):
    IE_DESC = 'Idello.org'
    _LOGIN_REQUIRED = True
    _LOGIN_URL = 'https://www.idello.org/fr/api/v1/account/signin'
    # _VALID_URL = r'https://www.idello.org/fr/ressource'
    _VALID_URL = r'https?://.+?\.idello\.org/fr/ressource/(?P<name_or_id>.+)\?navcontext=(?P<video_id>.+)'
    _NETRC_MACHINE = 'idello'
    # _VALID_URL = r'https?://.+?\.idello\.org/(?:[^/]+/)?(?P<type>videos|show_videos|articles|feature|(?:[^/]+/\d+/video))(/.+)?/(?P<name_or_id>.+)'
    #_VALID_URL = r'https?://medius.studios.ms/Embed/Video-nc/(?P<id>[A-Z0-9\-]+)'

    _TEST = {
        #'url': 'https://medius.studios.ms/Embed/Video-nc/B19-BDL2046?latestplayer=true',
        'url': 'https://www.idello.org/fr/ressource/27391-Dense-Dense-Dense?navcontext=27394',
        'md5': '55f5e8981c1c80a64706a44b74833de8',
        'info_dict': {
            'id': '27394',
            'ext': 'mp4',
            'title': 'Dense, dense, dense!',
            'description': '',
            'duration': None,
            'upload_date': None,
            'uploader': ''
        },
        'params': {
            # m3u8 download
            'skip_download': True,
            'usenetrc': True,
        },
        'expected_warnings': ['HTTP Error 404: Not Found'],
    }

    def _login(self):
        print("about to login")
        username, password = self._get_login_info(netrc_machine=self._NETRC_MACHINE)
        
        if username is None:
            if self._LOGIN_REQUIRED:
                raise ExtractorError('No login info available, needed for using %s.' % self.IE_NAME, expected=True)
            return

        login_form_strs = {
            'username': username,
            'password': hashlib.md5(password).hexdigest(),
            "sigin_under_13": "false",
            "remember": 0
        }
        
        urlh = self._request_webpage(
            self._LOGIN_URL, None,
            note='Logging in', errnote='Unable to log in',
            data=urlencode_postdata(login_form_strs))
        
        cookie = urlh.headers.get('Set-Cookie')

        token = re.match(r"tfo-idello-session=(?P<token>.+); path", cookie).group('token')
        self._set_cookie('.www.idello.org', 'tfo-idello-session', token)

        data = {
            'action': 'login',
            'email': username,
            'password': password,
            'service': 'idello',
            'token': token,
        }
        try:
            self._download_webpage(
                self._LOGIN_URL, None, 'Logging in',
                data=urlencode_postdata(data), headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': self._LOGIN_URL,
                })
        except ExtractorError as e:
            if isinstance(e.cause, compat_HTTPError) and e.cause.code == 418:
                raise ExtractorError(
                    'Unable to log in: bad username or password',
                    expected=True)
            raise ExtractorError('Unable to log in')

    def _find_video_id(self, webpage):
        res_id = [
            r'"video_id"\s*:\s*"(.*?)"',
            r'class="hero-poster[^"]*?"[^>]*id="(.+?)"',
            r'data-video-id="(.+?)"',
            r'<object id="vid_(.+?)"',
            r'<meta name="og:image" content=".*/(.+?)-(.+?)/.+.jpg"',
            r'videoId&quot;\s*:\s*&quot;(.+?)&quot;',
            r'videoId["\']\s*:\s*["\']([^"\']+?)["\']',
        ]
        return self._search_regex(res_id, webpage, 'video id', default=None)

    def _real_initialize(self):
        self._login()

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('video_id')
        
        webpage = self._download_webpage(url, video_id)
        print(webpage.encode('utf-8'))
        video_id = self._find_video_id(webpage)
        return None
        info_dict = self._extract_jwplayer_data(
            webpage, video_id, require_title=False)

        info_dict.update({
            'id': video_id,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
        })

        return self.playlist_result(entries)
