from Packages import *


image = PIL.Image.open('image1.jpg')

exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in image._getexif().items()
    if k in PIL.ExifTags.TAGS
}

# print(exif['GPSInfo'])

north = exif['GPSInfo'][2]
east = exif['GPSInfo'][4]

print(north)
print(east)

lat = ((((north[0] * 60) + north[1]) * 60) + north[2]) / 3600
lon = ((((east[0] * 60) + east[1]) * 60) + east[2]) / 3600

lat, lon = float(lat), float(lon)

print(lat, lon)


gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
gmap.marker(lat, lon, 'cornflowerblue')
gmap.draw("location.html")

geoLoc = Nominatim(user_agent="myapplication")
location = geoLoc.reverse(f"{lat}, {lon}")
print(location.address)

webbrowser.open("location.html", new=2)