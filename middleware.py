from gedgo import REDIS
from gedgo.tasks import geo_resolve_ip
import json
import time
import re

IGNORE_PATTERNS = [
    r'^/gedgo/media/',
    r'^/gedgo/\d+/(?:timeline|pedigree)'
]
IGNORE_PATTERNS = [re.compile(p) for p in IGNORE_PATTERNS]


class SimpleTrackerMiddleware(object):
    """
    Lightweight user page view tracking.
    """

    def process_response(self, request, response):
        # Don't process if REDIS isn't configured or non-200 response
        if REDIS is None or response.status_code != 200:
            return response

        # Only track non-superuser visitors
        if request.user is None or request.user.is_superuser \
                or not request.user.username:
            return response

        for pattern in IGNORE_PATTERNS:
            if pattern.match(request.path_info):
                return response

        try:
            pvc = int(REDIS.get('gedgo_page_view_count'))
        except TypeError:
            pvc = 0
        REDIS.set('gedgo_page_view_count', pvc + 1)

        page_view = {
            'ip': request.META['REMOTE_ADDR'],
            'path': request.path_info,
            'username': request.user.username,
            'time': int(time.time())
        }

        REDIS.lpush('gedgo_page_views', json.dumps(page_view))
        REDIS.ltrim('gedgo_page_views', 0, 100)

        stored = REDIS.keys('gedgo_ip_%s' % page_view['ip'])
        if stored is None:
            geo_resolve_ip.delay(page_view['ip'])

        return response