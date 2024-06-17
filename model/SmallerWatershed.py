from abc import ABC

import rasterio
from pysheds.grid import Grid

from model.Watershed import Watershed
from model.StartLocation import StartLocation
from shapely import geometry, ops

## Class for a unique point computation
# PyShed computation is trully processed here, in small_solve

class SmallerWatershed(Watershed, ABC) :

    start_location: StartLocation
    grid = None
    shapes = None
    catchment_polygon = None

    def __init__(self, sl_input):
        # super().__init__(sl_input)
        self.start_location = sl_input

    def small_solve(self):
        with rasterio.Env():
            self.start_location.prepare()
            grid = Grid.from_raster(self.start_location.get_elevation())
            catch = grid.catchment(
                x=self.start_location.x_snap,
                y=self.start_location.y_snap,
                fdir=self.start_location.get_elevation().fdir,
                dirmap=self.start_location.get_elevation().dirmap,
                xytype='coordinate')
            grid.clip_to(catch)
            self.grid = grid
            self.shapes = grid.polygonize()
            self.catchment_polygon = ops.unary_union(
                [geometry.shape(shape) for shape, value in self.shapes])
            return self.catchment_polygon



