cl__1 = 10;
Point(1) = {0.5, 0.5, 0.5, 20};
Point(2) = {0, 0, 0, 20};
Point(3) = {0, 0, 1, 20};
Point(4) = {1, 1, 1, 20};
Point(5) = {1, 0, 1, 20};
Point(9) = {0, 1, 0, 20};
Point(10) = {0, 1, 1, 20};
Line(1) = {10, 4};
Line(2) = {4, 5};
Line(3) = {5, 3};
Line(4) = {3, 10};
Line(5) = {1, 10};
Line(6) = {1, 3};
Line(7) = {1, 4};
Line(9) = {1, 5};
Line(10) = {10, 2};
Line(11) = {2, 3};
Line(12) = {1, 2};
Line(13) = {10, 9};
Line(14) = {9, 4};
Line(15) = {1, 9};
Line Loop(17) = {15, -13, -5};
Plane Surface(17) = {17};
Line Loop(19) = {12, -10, -5};
Plane Surface(19) = {19};
Line Loop(22) = {1, 2, 3, 4};
Plane Surface(22) = {22};
Line Loop(24) = {2, -9, 7};
Plane Surface(24) = {24};
Line Loop(26) = {7, -14, -15};
Plane Surface(26) = {26};
Line Loop(28) = {13, 14, -1};
Plane Surface(28) = {28};
Line Loop(30) = {11, 4, 10};
Plane Surface(30) = {30};
Line Loop(32) = {6, -3, -9};
Plane Surface(32) = {32};
Line Loop(33) = {12, 11, -6};
Plane Surface(33) = {33};
Surface Loop(35) = {17, 19, 22, 24, 26, 28, 30, 32, 33};
Volume(35) = {35};
Physical Surface(102) = {30};
Physical Surface(201) = {22, 28};
Physical Volume(26) = {35};
Line(202) = {4, 3};
