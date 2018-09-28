import numpy as np
from itertools import cycle
from pymoab import types
from .InterpolationMethod import InterpolationMethodBase


class LPEW2(InterpolationMethodBase):

    def _get_volumes_sharing_face_and_node(self, node, volume):
        vols_around_node = self.mtu.get_bridge_adjacencies(node, 0, 3)
        adj_vols = self.mtu.get_bridge_adjacencies(volume, 2, 3)
        volumes_sharing_face_and_node = set(vols_around_node).difference({adj_vols})
        return list(volumes_sharing_face_and_node)

    def _arrange_auxiliary_verts(self, node, volume):
        T = {}
        adj_vols = self._get_volumes_sharing_face_and_node(node, volume)
        adj_vols = [list(adj_vols[i])[0] for i in range(len(adj_vols))]
        aux_verts_bkp = list(set(self.mtu.get_bridge_adjacencies(volume,
                                 3, 0)).difference(set([node])))
        aux_faces = list(set(self.mtu.get_bridge_adjacencies(volume,
                                                             3, 2)))
        for face in aux_faces:
            nodes_in_aux_face = list(set(self.mtu.get_bridge_adjacencies(
                                         face, 2, 0)).difference(set([node])
                                                                 )
                                     )
            if len(nodes_in_aux_face) == 3:
                    aux_faces.remove(face)
        aux_verts = cycle(aux_verts_bkp)
        for index, aux_vert in zip([1, 3, 5], aux_verts):
            T[index] = aux_vert
        for aux_face in aux_faces:
            aux_verts = list(set(self.mtu.get_bridge_adjacencies(
                                         aux_face, 2, 0)).difference(set(
                                                                     [node]
                                                                     )))
            adj_vol = set(self.mtu.get_bridge_adjacencies(aux_face,
                          2, 3)).difference(set([volume]))
            aux1 = list(T.keys())[list(T.values()).index(aux_verts[0])]
            aux2 = list(T.keys())[list(T.values()).index(aux_verts[1])]
            if aux1 + aux2 != 6:
                index = (aux1 + aux2) / 2
                T[int(index)] = (aux_face,
                                 self.mtu.get_average_position([aux_face]),
                                 adj_vol)
            else:
                T[6] = (aux_face, self.mtu.get_average_position([aux_face]),
                        adj_vol)
        aux_verts = cycle(aux_verts_bkp)
        for index, aux_vert in zip([1, 3, 5], aux_verts):
            T[index] = (aux_vert,
                        self.mtu.get_average_position([node, aux_vert])
                        )
        T[7] = T[1]

        return T

    def _get_auxiliary_volumes(self, node, volume):
        faces_in_volume = set(self.mtu.get_bridge_adjacencies(
                                      volume, 3, 2))
        faces_sharing_vertice = set(self.mtu.get_bridge_adjacencies(
                                            node, 0, 2))
        faces_sharing_vertice = faces_in_volume.intersection(
                                        faces_sharing_vertice)
        adj_vols = []
        for face in faces_sharing_vertice:
            volumes_sharing_face = set(self.mtu.get_bridge_adjacencies(
                                            face, 2, 3))
            side_volume = volumes_sharing_face - {volume}
            adj_vols.append(side_volume)
        return adj_vols

    def _flux_term(self, vector_1st, permeab, vector_2nd, face_area=1.0):
        aux_1 = np.dot(vector_1st, permeab)
        aux_2 = np.dot(aux_1, vector_2nd)
        flux_term = aux_2 / face_area
        return flux_term

    def _r_range(sefl, j, r):
        size = ((j - r + 5) % 6) + 1
        last_val = ((j + 4) % 6) + 1

        prod = [((last_val - k) % 6) + 1 for k in range(1, size+1)]
        return prod[::-1]

    def _zeta_lpew2(self, args):
        pass

    def _delta_lpew2(self, args):
        pass

    def _phi_lpew2(self, args):
        pass

    def _A_lpew2(self, args):
        pass

    def _interpolate(self, args, neumann=False):
        pass

    def _get_sub_volume(self, args):
        pass

    def _neta_lpew2(self, args):
        pass

    def _csi_lpew2(self, args):
        pass
