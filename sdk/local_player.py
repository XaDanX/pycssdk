from sdk.entity import Entity
from sdk.offsets import *
import struct


class LocalPlayer(Entity):
    def __init__(self, mem, entity):
        super().__init__(mem, entity)

    def view_matrix(self):
        view = self.mem.handle.read_bytes(self.mem.client + dwViewMatrix, 64)
        matrix = struct.unpack("16f", view)
        return matrix
