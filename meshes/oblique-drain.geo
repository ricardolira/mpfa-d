cl__1 = 1.;
sides = 1;
Point(1) = {0, 0, 0, cl__1};
Point(2) = {1, 0, 0, cl__1};
Point(3) = {1, 0.575, 0, cl__1};
Point(4) = {1, 0.58, 0, cl__1};
Point(5) = {1, 1, 0, cl__1};
Point(6) = {0, 1, 0, cl__1};
Point(7) = {0, 0.38, 0, cl__1};
Point(8) = {0, 0.375, 0, cl__1};
Point(9) = {0, 0.38, 1, cl__1};
Point(10) = {0, 1, 1, cl__1};
Point(14) = {1, 1, 1, 0.2};
Point(18) = {1, 0.58, 1, cl__1};
Point(24) = {0, 0.375, 1, cl__1};
Point(28) = {1, 0.575, 1, cl__1};
Point(34) = {0, 0, 1, cl__1};
Point(38) = {1, 0, 1, cl__1};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 8};
Line(4) = {8, 1};
Line(5) = {3, 4};
Line(6) = {4, 7};
Line(7) = {7, 8};
Line(8) = {7, 6};
Line(9) = {6, 5};
Line(10) = {5, 4};
Line(18) = {9, 10};
Line(19) = {10, 14};
Line(20) = {14, 18};
Line(21) = {18, 9};
Line(23) = {7, 9};
Line(24) = {6, 10};
Line(28) = {5, 14};
Line(32) = {4, 18};
Line(41) = {9, 24};
Line(42) = {24, 28};
Line(43) = {28, 18};
Line(50) = {8, 24};
Line(54) = {3, 28};
Line(63) = {24, 34};
Line(64) = {34, 38};
Line(65) = {38, 28};
Line(72) = {1, 34};
Line(76) = {2, 38};
Line Loop(12) = {8, 9, 10, 6};
Plane Surface(12) = {12};
Line Loop(14) = {-6, -5, 3, -7};
Plane Surface(14) = {14};
Line Loop(16) = {-3, -2, -1, -4};
Plane Surface(16) = {16};
Line Loop(25) = {-8, 23, 18, -24};
Ruled Surface(25) = {25};
Line Loop(29) = {-9, 24, 19, -28};
Ruled Surface(29) = {29};
Line Loop(33) = {-10, 28, 20, -32};
Ruled Surface(33) = {33};
Line Loop(37) = {-6, 32, 21, -23};
Ruled Surface(37) = {37};
Line Loop(38) = {-18, -21, -20, -19};
Plane Surface(38) = {38};
Line Loop(51) = {7, 50, -41, -23};
Ruled Surface(51) = {51};
Line Loop(55) = {-3, 54, -42, -50};
Ruled Surface(55) = {55};
Line Loop(59) = {5, 32, -43, -54};
Ruled Surface(59) = {59};
Line Loop(60) = {21, 41, 42, 43};
Plane Surface(60) = {60};
Line Loop(73) = {4, 72, -63, -50};
Ruled Surface(73) = {73};
Line Loop(77) = {1, 76, -64, -72};
Ruled Surface(77) = {77};
Line Loop(81) = {2, 54, -65, -76};
Ruled Surface(81) = {81};
Line Loop(82) = {-42, 63, 64, 65};
Plane Surface(82) = {82};
Surface Loop(1) = {12, 38, 25, 29, 33, 37};
Volume(1) = {1};
Surface Loop(2) = {14, 60, 37, 51, 55, 59};
Volume(2) = {2};
Surface Loop(3) = {16, 82, 55, 73, 77, 81};
Volume(3) = {3};
Physical Surface(101) = {25, 29, 33, 51, 59, 73, 77, 81};
Physical Surface(201) = {12, 14, 16, 38, 60, 82};
Physical Volume(1) = {1};
Physical Volume(2) = {2};
Physical Volume(3) = {3};
Transfinite Line {5, 43, 41, 7} = 1 Using Progression 1;
Transfinite Line {65, 42, 63, 64, 21, 18, 19, 20} = sides Using Progression 1;
Transfinite Line {54, 65, 76, 2, 10, 20, 32} = sides Using Progression 1;
Transfinite Line {4, 4, 72, 63, 50, 23, 18, 24, 8} = sides Using Progression 1;
Transfinite Line {42, 63, 64, 65, 21, 20, 19, 18} = sides Using Progression 1;
Transfinite Line {6, 1, 72, 64, 76, 28, 9, 24, 19} = sides Using Progression 1;
Transfinite Surface {77};
Transfinite Surface {16};
Transfinite Surface {14};
Transfinite Surface {12};
Transfinite Surface {29};
Transfinite Surface {38};
Transfinite Surface {60};
Transfinite Surface {82};
Transfinite Surface {81};
Transfinite Surface {59};
Transfinite Surface {33};
Transfinite Surface {29};
Transfinite Surface {25};
Transfinite Surface {51};
Transfinite Surface {73};
Transfinite Surface {16};
Transfinite Surface {55};
Transfinite Surface {37};
Transfinite Surface {16};
Transfinite Surface {16};
Transfinite Surface {16};
Transfinite Line {1, 2, 3, 4} = sides Using Progression 1;
Transfinite Surface {16};
