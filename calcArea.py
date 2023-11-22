import json
from area import area

""" insert the feature into "featureToCalcArea.json" file in root folder """

# Open the featureToCalcArea.json file
with open("featureToCalcArea.json") as file:
    # Load its content and make a new dictionary
    geoJSON = json.load(file)
    # Print area in sq. meters
    print("square m: ", area(geoJSON['geometry']))
    # Print area in sq. km
    print("square km: ", area(geoJSON['geometry']) / (1000 * 1000))
