from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.ops import split


"""""""""" input values """""""""
# bbox = min Longitude , min Latitude , max Longitude , max Latitude
bbox = [
    89.25702881854522,
    36.92684474955692,
    116.85433004104902,
    47.88565042992184
]
nx, ny = 10, 10  # number of columns and rows

featureName = "GobiAreas"  # base for all subareas
object_type = "Ground object"  # the same for all subareas
wikiLink = "https://en.wikipedia.org/wiki/Antarctica"  # the same for all subareas
""""""""""""""""""""""""""""""""

rec = [(bbox[0], bbox[1]), (bbox[0], bbox[3]),
       (bbox[2], bbox[3]), (bbox[2], bbox[1])]

polygon = Polygon(rec)


def separation() -> list:
    minx, miny, maxx, maxy = polygon.bounds
    dx = (maxx - minx) / nx  # width of a small part
    dy = (maxy - miny) / ny  # height of a small part
    horizontal_splitters = [LineString(
        [(minx, miny + i*dy), (maxx, miny + i*dy)]) for i in range(ny)]
    vertical_splitters = [LineString(
        [(minx + i*dx, miny), (minx + i*dx, maxy)]) for i in range(nx)]
    splitters = horizontal_splitters + vertical_splitters

    result = polygon
    for splitter in splitters:
        result = MultiPolygon(split(result, splitter))

    coordinates_list = [list(part.exterior.coords) for part in result.geoms]
    coordinates_list.reverse()  # reverse coordinates list
    return coordinates_list


def constructJSON(coordinates: list):
    features_list = []

    for x in range(len(coordinates)):
        featureCoordinates = [list(x) for x in coordinates[x]]
        feature = {
            "type": "Feature",
            "properties": {
                    "ADMIN": featureName + "_" + str(x+1),
                    "DATA": 12345,
                    "TYPE": object_type,
                    "WIKI": wikiLink
            },
            "bbox": [featureCoordinates[0][0], featureCoordinates[0][1], featureCoordinates[2][0], featureCoordinates[2][1]],
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    featureCoordinates
                ]
            }
        }
        features_list.append(feature)
    return features_list


def write_down(features):
    fileName = featureName + ".txt"
    with open(fileName, 'w') as f:
        for feature in features:
            f.write("," + str(feature).replace("\'", "\""))
            f.write('\n')


def main():
    coordinates = separation()
    featuresList = constructJSON(coordinates)
    write_down(featuresList)


if __name__ == '__main__':
    main()
