from bmlife_bot.utils.geocode import get_coordinate

query = '1179 Boylston St Boston,MA'

lat, lon = get_coordinate(query)

print(lat)
print(lon)

