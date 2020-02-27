import geopy.distance

coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)

print(geopy.distance.distance(coords_1, coords_2).km)

coords_3 = (46.5355668, 6.5799793)
coords_4 = (46.5359335, 6.5791643)

print(geopy.distance.great_circle(coords_3, coords_4).km)

coords_5 = (46.5341841, 6.5983288)
coords_6 = (46.5248736, 6.5991119)
print(geopy.distance.great_circle(coords_5, coords_6).km)
