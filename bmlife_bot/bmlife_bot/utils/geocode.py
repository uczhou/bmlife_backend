from opencage.geocoder import OpenCageGeocode

key = ''
geocoder = OpenCageGeocode(key)


def get_coordinate(query):
    results = geocoder.geocode(query)

    return results[0]['geometry']['lat'], results[0]['geometry']['lng']
