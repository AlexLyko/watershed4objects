from shapely import Polygon, Point, LineString

from model import Watershed as sw

### Examples
if __name__ == '__main__':
    # First test, describing each step, not multithreaded
    this_bv1 = sw.Watershed(
        Polygon([(3, -1), (4, 0), (3, 1)]),
        "elevation-mnt-path-on-my-hdd")
    this_bv1.solve()
    watershed_geometry_1: Polygon = this_bv1.get_geometry()

    # Second test, all-in-wonder, not multithreaded
    watershed_geometry_2 = sw.Watershed([
        Point(1, 1),
        LineString([(1, -1), (1, 0)]),
        Polygon([(3, -1), (4, 0), (3, 1)]),
    ], "elevation-mnt-path-on-my-hdd").get_geometry()

    # First test, describing each step, multithreaded
    this_bv3 = sw.Watershed(
        Polygon([(3, -1), (4, 0), (3, 1)]),
        "elevation-mnt-path-on-my-hdd")
    this_bv3.solve_multithread()
    watershed_geometry_3: Polygon = this_bv3.get_geometry()
