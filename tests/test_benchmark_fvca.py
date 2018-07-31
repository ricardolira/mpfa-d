import unittest
import numpy as np
from math import pi
from mpfad.MpfaD import MpfaD3D
from mpfad.interpolation.LPEW3 import LPEW3
from mesh_preprocessor import MeshManager


class InterpMethodTest(unittest.TestCase):

    def setUp(self):
        K = self.benchmark_1(0., 0., 0.)[0]
        self.mesh = MeshManager('mesh_tet5.h5m', dim=3)
        self.mesh.set_media_property('Permeability', {1: K}, dim_target=3)
        self.mesh.set_boundary_condition('Dirichlet', {101: 0.0},
                                         dim_target=2, set_nodes=True)
        self.mpfad = MpfaD3D(self.mesh)
        self.lpew3 = LPEW3(self.mesh)

    def benchmark_1(self, x, y, z):
        K = [1.0, 0.5, 0.0,
             0.5, 1.0, 0.5,
             0.0, 0.5, 1.0]
        u1 = 1 + np.sin(pi * x) * np.sin(pi * (y + 1/2)) * np.sin(pi * (z +
                                                                        1/3))
        return K, u1

    def benchmark_2(self, x, y, z):
        k_xx = y ** 2 + z ** 2 + 1
        k_xy = - x * y
        k_xz = - x * z
        k_yx = - x * y
        k_yy = x ** 2 + z ** 2 + 1
        k_yz = - y * z
        k_zx = - x * z
        k_zy = - y * z
        k_zz = x ** 2 + y ** 2 + 1

        K = [k_xx, k_xy, k_xz,
             k_yx, k_yy, k_yz,
             k_zx, k_zy, k_zz]

        u2 = ((x ** 3 * y ** 2 * z) + x * np.sin(2 * pi * x * z)
                                       * np.sin(2 * pi * x * y)
                                       * np.sin(2 * pi * z))

        return K, u2

    def benchmark_3(self, x, y, z):
        K = [1E-0, 0E-0, 0E-0,
             0E-0, 1E-0, 0E-0,
             0E-0, 0E-0, 1E-3]
        u3 = np.sin(2 * pi * x) * np.sin(2 * pi * y) * np.sin(2 * pi * z)

        return K, u3

    # @unittest.skip("This test is a pass")
    def test_benchmark_case_1(self):
        for node in self.mesh.get_boundary_nodes():
            x, y, z = self.mesh.mb.get_coords([node])
            g_D = self.benchmark_1(x, y, z)[1]
            self.mesh.mb.tag_set_data(self.mesh.dirichlet_tag, node, g_D)
        volumes = self.mesh.all_volumes
        for volume in volumes:
            self.mesh.mb.tag_set_data(self.mesh.perm_tag, volume,
                                      self.benchmark_1(0., 0., 0.,)[0])
        self.mpfad.run_solver(LPEW3(self.mesh).interpolate)
        rel2 = []
        u_sol = []
        for volume in volumes:
            x_c, y_c, z_c = self.mesh.get_centroid(volume)
            analytical_solution = self.benchmark_1(x_c, y_c, z_c)[1]
            calculated_solution = self.mpfad.mb.tag_get_data(
                                  self.mpfad.pressure_tag, volume)[0][0]
            tetra_nodes = self.mpfad.mtu.get_bridge_adjacencies(volume, 3, 0)
            tetra_coords = self.mpfad.mb.get_coords(tetra_nodes).reshape([4,3])
            tetra_vol = self.mesh.get_tetra_volume(tetra_coords)
            u_sol.append(analytical_solution ** 2 * tetra_vol)
            rel2.append(np.absolute(analytical_solution - calculated_solution) ** 2
                        * tetra_vol)
        u_max = max(self.mpfad.mb.tag_get_data(
                              self.mpfad.pressure_tag, volumes))
        u_min = min(self.mpfad.mb.tag_get_data(
                              self.mpfad.pressure_tag, volumes))
        l2_norm = (np.dot(rel2, rel2)) ** (1 / 2)
        rl2_norm = (np.dot(rel2, rel2) / np.dot(u_sol, u_sol)) ** (1 / 2)
        non_zero_mat = np.nonzero(self.mpfad.A)[0]
        self.assertLessEqual(l2_norm, 6.13e-2)
        print("Test case 1", 'unkonws: ', len(volumes),
              'non zero mat: ', len(non_zero_mat), 'u_max: ', u_max,
              'u_min: ', u_min, 'l2_norm: ', l2_norm,
              'relative_l2_norm: ', rl2_norm)
        self.mpfad.record_data('benchmark_1.vtk')

    @unittest.skip('not ready for testing')
    def test_benchmark_case_2(self):
        for node in self.mesh.get_boundary_nodes():
            x, y, z = self.mesh.mb.get_coords([node])
            g_D = self.benchmark_2(x, y, z)[1]
            self.mesh.mb.tag_set_data(self.mesh.dirichlet_tag, node, g_D)
        volumes = self.mesh.all_volumes
        for volume in volumes:
            x_c, y_c, z_c = self.mesh.get_centroid(volume)
            perm = self.benchmark_2(x_c, y_c, z_c)[0]
            self.mesh.mb.tag_set_data(self.mesh.perm_tag, volume, perm)
        self.mpfad.run_solver(LPEW3(self.mesh).interpolate)

        rel2 = []
        u_sol = []
        for volume in volumes:
            x_c, y_c, z_c = self.mesh.get_centroid(volume)
            analytical_solution = self.benchmark_2(x_c, y_c, z_c)[1]
            calculated_solution = self.mpfad.mb.tag_get_data(
                                  self.mpfad.pressure_tag, volume)[0][0]
            u_sol.append(analytical_solution ** 2)
            tetra_nodes = self.mpfad.mtu.get_bridge_adjacencies(volume, 3, 0)
            tetra_coords = self.mpfad.mb.get_coords(tetra_nodes).reshape([4,3])
            tetra_vol = self.mesh.get_tetra_volume(tetra_coords)
            u_sol.append(analytical_solution ** 2 * tetra_vol)
            rel2.append(np.absolute(analytical_solution - calculated_solution) ** 2
                        * tetra_vol)

        l2_norm = (sum(rel2)) ** (1 / 2)
        u_max = max(self.mpfad.mb.tag_get_data(
                              self.mpfad.pressure_tag, volumes))
        u_min = min(self.mpfad.mb.tag_get_data(
                              self.mpfad.pressure_tag, volumes))
        non_zero_mat = np.nonzero(self.mpfad.A)[0]
        # print("Test case 2", len(volumes), len(non_zero_mat), u_max, u_min, l2_norm)
