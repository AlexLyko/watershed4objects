# watershed4objects

Watersheds are generally computed from an outflow point. 
In practical terms, in 'data repository' development projects, the engineers already have a reference hydrographic graph. 
These developments therefore take geographical objects as input (like Polygons, Lines, or Points), not a single point.

Consider it as a [pyShed](https://github.com/mdbartos/pysheds) wrapper.

Pending optimizations :

- multithread combined with previously overlapped points exclusion
- use the graph network as a grid.accumulation reference and avoid the computation on elevation
- Watershed.py and SmallerWatershed.py should be merged, with a type condition at launch (they're basically same thing, except one is for collections, and the other one is for single points). In the short term, it's useless and makes the code less readable.
- Should go and try, wether the use of "check" for flow accumulation in Elevation.py, and the "acc" variable, is better in "self" def or in "cls". At a glance the use of an instance is more logical, but if you only have a single MNT, you can afford only one var (a @class method)...


![image](https://github.com/AlexLyko/watershed4objects/assets/17929890/2af62449-41d5-4c37-b121-c7d61b0259e2)

Error use case is shown as "Error 1" below (a part of the watershed is missing uppward B point):
![image](https://github.com/AlexLyko/watershed4objects/assets/17929890/a389c35d-c113-4fb1-ab63-ec531efa2576)

You already have the blue lines, so you can use the points from the blue graph for computing the new watershed from B :
![image](https://github.com/AlexLyko/watershed4objects/assets/17929890/ed53a4d6-53ae-4245-ad38-87111a172f3a)

