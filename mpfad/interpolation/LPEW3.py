import numpy as np
from .InterpolationMethod import InterpolationMethodBase
# from mpfad.helpers.geometric import get_tetra_volume
# from mpfad.helpers.geometric import _area_vector


class LPEW3(InterpolationMethodBase):

    def _area_vector(self, nodes, ref_node):
        ref_vect = nodes[0] - ref_node
        AB = nodes[1] - nodes[0]
        AC = nodes[2] - nodes[0]
        area_vector = np.cross(AB, AC) / 2.0
        if np.dot(area_vector, ref_vect) < 0.0:
            area_vector = - area_vector
            return [area_vector, -1]
        return [area_vector, 1]

    def _lambda_lpew3(self, node, aux_node, face):
        adj_vols = self.mtu.get_bridge_adjacencies(face, 2, 3)
        face_nodes = self.mtu.get_bridge_adjacencies(face, 2, 0)
        ref_node = list(set(face_nodes) - (set([node]) | set([aux_node])))
        face_nodes_crds = self.mb.get_coords(face_nodes)
        face_nodes_crds = np.reshape(face_nodes_crds, (3, 3))
        ref_node = self.mb.get_coords(ref_node)
        aux_node = self.mb.get_coords([aux_node])
        node = self.mb.get_coords([node])
        lambda_l = 0.0
        for a_vol in adj_vols:
            vol_perm = self.mb.tag_get_data(self.perm_tag, a_vol)
            vol_perm = np.reshape(vol_perm, (3, 3))
            vol_cent = self.mesh_data.get_centroid(a_vol)
            vol_nodes = self.mb.get_adjacencies(a_vol, 0)
            sub_vol = np.append(face_nodes_crds, vol_cent)
            sub_vol = np.reshape(sub_vol, (4, 3))
            tetra_vol = self.mesh_data.get_tetra_volume(sub_vol)
            ref_node_i = list(set(vol_nodes) - set(face_nodes))
            ref_node_i = self.mb.get_coords(ref_node_i)
            N_int = self._area_vector([node, aux_node, vol_cent], ref_node)[0]
            N_i = self._area_vector(face_nodes_crds, ref_node_i)[0]
            lambda_l += self._flux_term(N_i, vol_perm, N_int)/(3.0*tetra_vol)
        return lambda_l

    def _neta_lpew3(self, node, vol, face):
        vol_perm = self.mb.tag_get_data(self.perm_tag, vol)
        vol_perm = np.reshape(vol_perm, (3, 3))
        vol_nodes = self.mb.get_adjacencies(vol, 0)
        face_nodes = self.mtu.get_bridge_adjacencies(face, 2, 0)
        face_nodes_crds = self.mb.get_coords(face_nodes)
        face_nodes_crds = np.reshape(face_nodes_crds, (3, 3))
        ref_node = list(set(vol_nodes) - set(face_nodes))
        ref_node = self.mb.get_coords(ref_node)
        vol_nodes_crds = self.mb.get_coords(list(vol_nodes))
        vol_nodes_crds = np.reshape(vol_nodes_crds, (4, 3))
        tetra_vol = self.mesh_data.get_tetra_volume(vol_nodes_crds)
        vol_nodes = set(vol_nodes)
        vol_nodes.remove(node)
        face_nodes_i = self.mb.get_coords(list(vol_nodes))
        face_nodes_i = np.reshape(face_nodes_i, (3, 3))
        node = self.mb.get_coords([node])
        N_out = self._area_vector(face_nodes_i, node)[0]
        N_i = self._area_vector(face_nodes_crds, ref_node)[0]
        neta = self._flux_term(N_out, vol_perm, N_i)/(3.0 * tetra_vol)
        return neta

    def _csi_lpew3(self, face, vol):
        vol_perm = self.mb.tag_get_data(self.perm_tag, vol)
        vol_perm = np.reshape(vol_perm, (3, 3))
        vol_cent = self.mesh_data.get_centroid(vol)
        face_nodes = self.mtu.get_bridge_adjacencies(face, 2, 0)
        face_nodes = self.mb.get_coords(face_nodes)
        face_nodes = np.reshape(face_nodes, (3, 3))
        N_i = self._area_vector(face_nodes, vol_cent)[0]
        sub_vol = np.append(face_nodes, vol_cent)
        sub_vol = np.reshape(sub_vol, (4, 3))
        tetra_vol = self.mesh_data.get_tetra_volume(sub_vol)
        csi = self._flux_term(N_i, vol_perm, N_i)/(3.0*tetra_vol)
        return csi

    def _sigma_lpew3(self, node, vol):
        node_crds = self.mb.get_coords([node])
        adj_faces = set(self.mtu.get_bridge_adjacencies(node, 0, 2))
        vol_faces = set(self.mtu.get_bridge_adjacencies(vol, 3, 2))
        in_faces = list(adj_faces & vol_faces)
        vol_cent = self.mesh_data.get_centroid(vol)
        clockwise = 1.0
        counterwise = 1.0
        for a_face in in_faces:
            aux_nodes = set(self.mtu.get_bridge_adjacencies(a_face, 2, 0))
            aux_nodes.remove(node)
            aux_nodes = list(aux_nodes)
            aux_nodes_crds = self.mb.get_coords(aux_nodes)
            aux_nodes_crds = np.reshape(aux_nodes_crds, (2, 3))
            aux_vect = [node_crds, aux_nodes_crds[0], aux_nodes_crds[1]]
            clock_test = self._area_vector(aux_vect, vol_cent)[1]
            if clock_test < 0:
                aux_nodes[0], aux_nodes[1] = aux_nodes[1], aux_nodes[0]
            count = self._lambda_lpew3(node, aux_nodes[0], a_face)
            counterwise = counterwise * count
            clock = self._lambda_lpew3(node, aux_nodes[1], a_face)
            clockwise = clockwise * clock
        sigma = clockwise + counterwise
        return sigma

    def _phi_lpew3(self, node, vol, face):
        face_nodes = self.mtu.get_bridge_adjacencies(face, 2, 0)
        vol_nodes = self.mb.get_adjacencies(vol, 0)
        aux_node = set(vol_nodes) - set(face_nodes)
        aux_node = list(aux_node)
        adj_faces = set(self.mtu.get_bridge_adjacencies(node, 0, 2))
        vol_faces = set(self.mtu.get_bridge_adjacencies(vol, 3, 2))
        in_faces = adj_faces & vol_faces
        faces = in_faces - set([face])
        faces = list(faces)
        lambda_mult = 1.0
        for a_face in faces:
            lbd = self._lambda_lpew3(node, aux_node[0], a_face)
            lambda_mult = lambda_mult * lbd
        sigma = self._sigma_lpew3(node, vol)
        neta = self._neta_lpew3(node, vol, face)
        phi = lambda_mult * neta / sigma
        return phi

    def _psi_sum_lpew3(self, node, vol, face):
        face_nodes = self.mtu.get_bridge_adjacencies(face, 2, 0)
        vol_nodes = self.mb.get_adjacencies(vol, 0)
        aux_node = set(vol_nodes) - set(face_nodes)
        aux_node = list(aux_node)

        adj_faces = set(self.mtu.get_bridge_adjacencies(node, 0, 2))
        vol_faces = set(self.mtu.get_bridge_adjacencies(vol, 3, 2))
        in_faces = adj_faces & vol_faces
        faces = in_faces - set([face])
        faces = list(faces)
        phi_sum = 0.0
        for i in range(len(faces)):
            a_face_nodes = self.mtu.get_bridge_adjacencies(faces[i], 2, 0)
            other_node = set(face_nodes) - set(a_face_nodes)
            other_node = list(other_node)
            lbd_1 = self._lambda_lpew3(node, aux_node[0], faces[i])
            lbd_2 = self._lambda_lpew3(node, other_node[0], faces[i-1])
            neta = self._neta_lpew3(node, vol, faces[i])
            phi = lbd_1 * lbd_2 * neta
            phi_sum += + phi
        sigma = self._sigma_lpew3(node, vol)
        phi_sum = phi_sum / sigma
        return phi_sum

    def _partial_weight_lpew3(self, node, vol):
        vol_faces = self.mtu.get_bridge_adjacencies(vol, 3, 2)
        vols_neighs = self.mtu.get_bridge_adjacencies(vol, 2, 3)
        zepta = 0.0
        delta = 0.0
        for a_neigh in vols_neighs:
            neigh_faces = self.mtu.get_bridge_adjacencies(a_neigh, 3, 2)
            a_face = set(vol_faces) & set(neigh_faces)
            a_face = list(a_face)
            csi = self._csi_lpew3(a_face[0], vol)
            psi_sum_neigh = self._psi_sum_lpew3(node, a_neigh, a_face[0])
            psi_sum_vol = self._psi_sum_lpew3(node, vol, a_face[0])
            zepta += (psi_sum_vol + psi_sum_neigh) * csi
            phi_vol = self._phi_lpew3(node, vol, a_face[0])
            phi_neigh = self._phi_lpew3(node, a_neigh, a_face[0])
            delta += (phi_vol + phi_neigh) * csi
        p_weight = zepta - delta
        return p_weight

    def interpolate(self, node):
        vols_around = self.mtu.get_bridge_adjacencies(node, 0, 3)
        weights = np.array([])
        weight_sum = 0.0
        for a_vol in vols_around:
            p_weight = self._partial_weight_lpew3(node, a_vol)
            weights = np.append(weights, p_weight)
            weight_sum += p_weight
        weights = weights / weight_sum
        node_weights = {
            vol: weight for vol, weight in zip(vols_around, weights)}
        return node_weights
