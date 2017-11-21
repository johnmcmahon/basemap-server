import urllib2

import ModestMaps
import PIL
import TileStache.Providers


class ExtendedProxy:
    """
    This class is essentially a clone of the built-in Proxy provider with the
    addition of the following:

        - ability to receive a dictionary of custom headers
        - mechanism to avoid trainwrecking during HTTP request failures

    Example configuration:

    {
        "class": "providers:ExtendedProxy",
        "kwargs": {
            "url": "https://example.com/tiles/{Z}/{X}/{Y}.png",
            "headers": {
                "Authorization": "Bearer 0123456789abcdef"
            }
        }
    }
    """

    def __init__(self, layer, url=None, headers=None, timeout=None):
        if not url:
            raise Exception('missing url parameter')

        if headers is None:
            headers = {}
        elif not isinstance(headers, dict):
            raise Exception('headers parameter if present must be a dictionary')

        self.headers = headers
        self.provider = ModestMaps.Providers.TemplatedMercatorProvider(url)
        self.timeout = timeout

    def renderTile(self, width, height, srs, coord):
        img = None
        urls = self.provider.getTileUrls(coord)

        # Tell urllib2 get proxies if set in the environment variables <protocol>_proxy
        # see: https://docs.python.org/2/library/urllib2.html#urllib2.ProxyHandler
        proxy_support = urllib2.ProxyHandler()
        url_opener = urllib2.build_opener(proxy_support)

        for url in urls:
            request = urllib2.Request(url)
            for key, value in self.headers.items():
                request.add_header(key, value)

            try:
                body = url_opener.open(request, timeout=self.timeout).read()
            except urllib2.HTTPError as err:
                raise TileStache.Core.TheTileLeftANote(
                    status_code=500,
                    emit_content_type=False,
                    content='error: upstream provider returned HTTP {}'.format(err.code),
                )

            tile = TileStache.Providers.Verbatim(body)

            if len(urls) == 1:
                #
                # if there is only one URL, don't bother
                # with PIL's non-Porter-Duff alpha channeling.
                #
                return tile
            elif img is None:
                #
                # for many URLs, paste them to a new image.
                #
                img = PIL.Image.new('RGBA', (width, height))

            img.paste(tile, (0, 0), tile)

        return img
