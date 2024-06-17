from shapely import geometry

from model.Elevation import Elevation
from decimal import Decimal

class StartLocation:

    x: Decimal
    y: Decimal
    x_snap: Decimal
    x_snap: Decimal
    mnt_elevation :Elevation


    def __init__(self, mnt_elevation_input: Elevation, geom_input: geometry):
        self.mnt_elevation = mnt_elevation_input
        self.x = geom_input.x
        self.y = geom_input.y

    def get_elevation(self):
        self.mnt_elevation.check()
        return self.mnt_elevation_input


    def prepare(self):
        self.mnt_elevation.check()
        if self.x_snap is None:
            self.x_snap, self.y_snap = self.mnt_elevation.grid.snap_to_mask(self.start_location.acc > 1000, (self.x, self.y))
        return self.mnt_elevation_input



