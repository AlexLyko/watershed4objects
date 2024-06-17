import concurrent
from abc import ABC

from model.LocationsCollection import LocationsCollection
from model.Elevation import Elevation
from model.SmallerWatershed import SmallerWatershed
from shapely import geometry, ops
import concurrent.futures

## Main class, you can choose your strategy.
# Such as... ONE THREAD (use "solve") or MULTITHREAD (use "solve_multithread")

class Watershed(ABC):
    locations_collection: LocationsCollection
    mnt_elevation: Elevation
    solved_watershed: geometry = None
    workers_nb = 8

    def __init__(self, geom_input, elevation_filepath_input: str):
        self.mnt_elevation = Elevation(elevation_filepath_input)
        self.locations_collection = LocationsCollection(self.mnt_elevation, geom_input)

    """
        The "classic" solve runs through a list of points,
        which represents the "network": all the points are
        generate a BV.
        Each time we calculate a new BV, we delete the points 
        covered by the perimeter of the previous one and the 
        return is merged with the previously calculated watersheds.
        To create a "large catchment area". 
    """

    def solve(self):
        self.mnt_elevation.solve_elevation_model()
        merged_watershed = None
        while self.locations_collection.renew_list(merged_watershed) > 0:
            a_smaller_watershed = SmallerWatershed(self.locations_collection.pick_nearest(merged_watershed))
            merged_watershed = ops.unary_union([
                a_smaller_watershed.small_solve(),
                merged_watershed
            ])
        self.solved_watershed = merged_watershed

    """
        The "multithreaded" method uses threads.
        All that remains is to implement memory sharing between processes:
        so we calculate the BV of all the points, which are then merged. 
        Should calculate faster, but many more objects. 
    """

    def solve_multithread(self):
        self.mnt_elevation.solve_elevation_model()
        chunks = self.locations_collection.all_x_y_locations()
        all_catchment_polygons = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers_nb) as executor:
            futures = {executor.submit(process_chunk, chunk): i for i, chunk in enumerate(chunks)}
            for future in concurrent.futures.as_completed(futures):
                chunk_index = futures[future]
                try:
                    result = future.result()
                    if result:
                        for catchment_polygon in result:
                            all_catchment_polygons.append(catchment_polygon)
                    print(f"Chunk {chunk_index + 1}/{len(chunks)} processed")
                except Exception as e:
                    print(f"Error processing chunk {chunk_index + 1}: {e}")
        self.solved_watershed = ops.unary_union([all_catchment_polygons])

    @classmethod
    def get_geometry(self):
        if self.solved_watershed is None:
            self.solve()
        return self.solved_watershed


""" 
     Chunk process,
     "in the thread"
"""
def process_chunk(chunk):
    results = []
    for location in chunk.itertuples():
        result = SmallerWatershed(location).small_solve()
        if result[0] is not None:
            results.append(result)
    return results
