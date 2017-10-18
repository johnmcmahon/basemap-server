# basemap-server

> Batteries-included visualization basemap server using [Natural Earth Data](http://www.naturalearthdata.com), [TileStache](http://tilestache.org) and [Mapnik](http://mapnik.org).


## Usage

### Docker

```bash
docker build -t basemap-server .

docker run -p 8000:80 -it basemap-server

open index.html
```


## Themes

### `/grey/{z}/{x}/{y}.png`

![grey](themes/grey.png)


### `/sepia/{z}/{x}/{y}.png`

![sepia](themes/sepia.png)


### `/silver/{z}/{x}/{y}.png`

![silver](themes/silver.png)
