import geopy.distance
import yaml
import pandas as pd
# typical walking speed is 1.4 m/s adjust down slightly b/c not straght line
WALKINGSPEED = 1.3


class M1Stop():
    def __init__(self, name, coords):
        self.name = name
        self.lat = coords[0]
        self.long = coords[1]

    def getDistance(self, coords):
        dist = geopy.distance.distance((self.lat, self.long), coords).m
        return dist

    def getApproxTravelTime(self, coords):
        dist = self.getDistance(coords)
        return (dist/WALKINGSPEED)/60  # convert to minutes


class M1Line():
    def __init__(self):
        m1_file_path = 'src\\m1.yaml'
        with open(m1_file_path, encoding='utf8') as file:
            m1_stops = yaml.load(file, Loader=yaml.FullLoader)
        self.stops = [M1Stop(k, v) for k, v in m1_stops.items()]
        self.names = [k for k in m1_stops.keys()]

    def getStop(self, name):
        n_stop = self.names.index(name)
        return self.stops[n_stop]

    def getNearestM1Stop(self, coords, rank=0):
        times = [s.getApproxTravelTime(coords) for s in self.stops]
        nth_closest_index = getRankedList(times).index(rank)
        # if two are equidistant and both further than the n-1th stop,
        # picks one to be nth and the other to be n+1th,
        # and returns only the nth.
        return (self.stops[nth_closest_index].name, times[nth_closest_index])

    def getDFofNearestStops(self, coords_iterable):
        coords_list = [c[1:] for c in coords_iterable]
        nearest_stops = [self.getNearestM1Stop(c) for c in coords_list]
        output = pd.DataFrame(index=[i[0] for i in coords_iterable])
        output['NearestStop'] = [n[0] for n in nearest_stops]
        output['TimeToNearestStop'] = [n[1] for n in nearest_stops]
        return output


def getRankedList(inlist):
    indices = list(range(len(inlist)))
    indices.sort(key=lambda x: inlist[x])
    output = [0]*len(indices)
    for i, x in enumerate(indices):
        output[x] = i
    return output
