// Gmsh project created on Tue Jun 28 14:53:33
// Generate 9.5X9.5X2.5 cm Volumetric Mesh for Sofa Collision Model

//define mesh size for the volumetric mesh
lc = 1e-2;

Point(1) = {0,     0,     0,     lc};
Point(2) = {0,     0,     0.095, lc};
Point(3) = {0.095, 0,     0.095, lc};
Point(4) = {0.095, 0,     0, lc};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Curve Loop(1) = {1,2,3,4};

Plane Surface(1) = {1};

Extrude {0,0.025,0} {Surface{1};}


//export .msh file
Mesh 3;
Save "phantom.msh";
