import geopandas
from model.Elevation import Elevation
from model.StartLocation import StartLocation

class LocationsCollection :

    geom_serie  = None
    coordinates_collection: geopandas.GeoSeries
    last_envelope = None
    mnt_elevation :Elevation


    def __init__(self, mnt_elevation_input :Elevation, geom_serie_input):
        self.geom_serie = geom_serie_input
        self.coordinates_collection = geopandas.GeoSeries(self.geom_serie).get_coordinates()
        self.mnt_elevation = mnt_elevation_input

    def renew_list(self, envelope):
        if self.last_envelope is None:
            self.last_envelope = envelope
            return self.coordinates_collection
        self.last_envelope = envelope
        self.coordinates_collection = self.coordinates_collection.difference(self.last_envelope)
        return self.coordinates_collection.length

    def pick_nearest(self) -> StartLocation:
        if self.last_envelope is None:
            return StartLocation(self.mnt_elevation, self.coordinates_collection[0])
        else:
            return StartLocation(self.mnt_elevation, self.coordinates_collection.sindex.nearest(self.last_envelope))
    @classmethod
    def all_x_y_locations(self):
        return self.coordinates_collection.get_coordinates()