import TileStache
import yaml


with open('tilestache.yaml') as f:
    config = yaml.safe_load(f)

application = TileStache.WSGITileServer(config)
