# ProjRot

ProjRot is code written in C that can do different things related to manipulating Hessians, among which projection of torsional modes. 

It requires a single input file named RPHt_input_data.dat. See 'examples' directory.
There is also an auxiliary file named dist_rotpr.dat which is used to set atom-atom distance cutoffs that are used internal rotors are defined. 

These primarily affect projections of structures that are located either (1) maxima or (2) non-stationary points on the potential energy surface. Either may be more correct depending on the structure being analyzed. 
