# watershed4objects

Watersheds are generally computed from an outflow point. 
In practical terms, in 'data repository' development projects, the engineers already have a reference hydrographic network. 
These developments therefore take geographical objects as input (like Polygons, Lines, or Points), not a single point.

[pyShed](https://github.com/mdbartos/pysheds)

Pending optimizations :

- multithread combined with previously overlapped points exclusion
- use the graph network as a grid.accumulation reference and avoid the computation on elevation
- Watershed.py and SmallerWatershed.py should be merged, with a type condition at launch (they're basically same thing, except one is for collections, and the other one is for single points). In the short term, it's useless and makes the code less readable.
