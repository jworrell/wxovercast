from kartograph import Kartograph

config = {
       "layers": [{
        "src": "ne_50m_admin_0_countries.shp",
        "filter": ["ISO", "is", "USA"]
    }],
    "bounds": {
        "mode": "bbox",
        "data": [-100,30,-60,60]
    }
}

K = Kartograph()
K.generate(config, outfile="mymap.svg")
