import os

from preprocessor.benchmark_mesh_generator import BenchMeshGenerator

# from mpfad.interpolation.IDW import IDW
from solvers.interpolation.LPEW3 import LPEW3

# from mpfad.interpolation.LSW import LSW

from single_phase_cases.benchmark_fvca import BenchmarkFVCA

# from single_phase_cases.oblique_drain import ObliqueDrain
# from single_phase_cases.discrete_maximum_principle import
# DiscreteMaxPrinciple
# from single_phase_cases.mpfad_mge_tests import TestCasesMGE

interpolations = [LPEW3]
benchmark_fvca_cases = [1, 2, 3, 4, 5]
fvcaMeshesB = [
    BenchMeshGenerator(str(case)).generate_mesh()
    for case in benchmark_fvca_cases
]
for mesh in fvcaMeshesB:
    for im in interpolations:
        log_name_1 = ("test_case_3_" + im.__name__ + "_" + mesh).replace(
            ".h5m", ""
        )
        # log_name_2 = ("test_case_2_" + im.__name__ + "_" + mesh).strip(
        #     ".h5m"
        # )
        BenchmarkFVCA(mesh, im).benchmark_case_3(log_name_1)
        # BenchmarkFVCA(mesh, im).benchmark_case_2(log_name_2)
        # TestCasesMGE(mesh, im).run_case(log_name_1, "mge_test_case_3")
        os.remove(mesh)

# meshes = []
# cases_dmp = ["16x16x16"]
# for case in cases_dmp:
#     for im in interpolations:
#         log_name = "monotonicity_test_" + im.__name__ + "_" + case
#         mesh_dmp = "meshes/monotone_" + case + ".msh"
#         DiscreteMaxPrinciple(mesh_dmp, im).run_dmp(log_name)
#         DiscreteMaxPrinciple(mesh_dmp, im).run_lai_sheng_dmp_test()
# meshes = {
#     "meshes/oblique-drain-new.msh": "distort",
#     "meshes/mesh_slanted_mesh.h5m": "coarse_mesh",
# }
# for setCase, logName in meshes.items():
#     for im in interpolations:
#         print(setCase, logName)
#         ObliqueDrain(setCase).runCase(im, logName)
