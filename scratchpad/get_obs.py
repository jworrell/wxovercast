import urllib

OBS = "http://w1.weather.gov/xml/current_obs/all_xml.zip"
SVR_OUTLOOKS = "http://www.spc.noaa.gov/products/spcrss.xml"
TORNADO_TS = "http://www.spc.noaa.gov/products/spcwwrss.xml"
PDS = "http://www.spc.noaa.gov/products/spcpdswwrss.xml"
MESO = "http://www.spc.noaa.gov/products/spcmdrss.xml"
CONVECTIVE = "http://www.spc.noaa.gov/products/spcacrss.xml"
FIRE = "http://www.spc.noaa.gov/products/spcfwrss.xml"
AIRMETS = "http://aviationweather.gov/adds/dataserver_current/current/airsigmets.cache.xml.gz"
PIREPS = "http://aviationweather.gov/adds/dataserver_current/current/aircraftreports.cache.xml.gz"
ALT_METARS = "http://aviationweather.gov/adds/dataserver_current/current/metars.cache.csv.gz"

product_list = {1: (OBS,
                    "Observations",
                    "obs.zip"),
                2: (SVR_OUTLOOKS,
                    "Watches, discussions, and outlooks",
                    "spcrss.xml"),
                3: (TORNADO_TS,
                    "Tornado/severe thunderstorm watches only",
                    "spcwwrss.xml"),
                4: (PDS,
                    "Particularly Dangerous Situation bulletins only",
                    "spcpdsrss.xml"),
                5: (MESO,
                    "Mesoscale discussions only",
                    "spcmdrss.xml"),
                6: (CONVECTIVE,
                    "Convective outlooks only",
                    "spcacrss.xml"),
                7: (FIRE,
                    "Fire weather forecasts only",
                    "spcfwrss.xml"),
                8: (AIRMETS,
                    "Airmets and sigmets",
                    "airsigmets.cache.xml.gz"),
                9: (PIREPS,
                    "Aircraft reports only",
                    "aircraftreports.cache.xml.gz"),
                10: (ALT_METARS,
                     "Alternate source for metars, updates every 5 minutes",
                     "metars.cache.csv.gz")}


def check_status(org_func):
    '''
    Checks the HTML status code to ensure that we have a successful response
    before trying to download the zip file.
    '''
    def checked(product, save_as):
        print "Checking url:", product
        response = urllib.urlopen(product).getcode()
        print "Status code:", response
        if response == 200:
            org_func(product, save_as)
        else:
            print "The status code", response, "has terminated your request!"
    return checked


@check_status
def download_bulletins(product, save_as):
    '''
    Attempts to download the zip file, only after we have a successful html
    response and only if the zip is newer than the previous file.
    '''
    print "Downloading all ..."
    try:
        urllib.urlretrieve(product, save_as)
        print "Success!"
    except Exception, e:
        print "Download failed: ", e


def product_menu():
    '''
    Just a cheap little commandline menu to get me started.
    '''
    print "Please select the product to download. Enter 0 to quit."
    print
    for num, description in product_list.iteritems():
        print num, product_list[num][1]
    print
    choice = int(input("> "))  # TODO: A check on the user's input.
    if choice != 0 and choice in product_list:
        download_bulletins(product_list[choice][0], product_list[choice][2])


if __name__ == "__main__":
    product_menu()
