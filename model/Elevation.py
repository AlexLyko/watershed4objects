from pysheds.grid import Grid


class Elevation:
    grid = None
    dem = None
    elevation_filepath = None
    pit_filled_dem = None
    flooded_dem = None
    inflated_dem = None
    dirmap = None
    fdir = None
    acc = None

    def __init__(self, elevation_filepath_input):
        self.elevation_filepath = elevation_filepath_input

    def solve_elevation_model(self, force = False):
        if force or self.acc is None:
            self.grid = Grid.from_raster(self.elevation_filepath)
            self.dem = self.grid.read_raster(self.elevation_filepath)
            self.pit_filled_dem = self.grid.fill_pits(self.dem)
            self.flooded_dem = self.grid.fill_depressions(self.pit_filled_dem)
            self.inflated_dem = self.grid.resolve_flats(self.flooded_dem)
            self.dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
            self.fdir = self.grid.flowdir(self.inflated_dem, dirmap=self.dirmap)
            self.acc = self.grid.accumulation(self.fdir, dirmap=self.dirmap)

    def check(self):
        if self.acc is None:
            self.solve_elevation_model()
