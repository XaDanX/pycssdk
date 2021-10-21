from sdk.offsets import *
import pymem
from sdk.entity import Entity


class EntityList:
    def __init__(self, mem):
        self.mem = mem
        self.entity_list = []

    def update(self):
        self.entity_list.clear()
        for index in range(1, 32):
            try:
                ent = self.mem.handle.read_int(self.mem.client + dwEntityList + index * 0x10)
            except pymem.exception.MemoryReadError:
                continue
            if ent != 0:
                self.entity_list.append(
                    Entity(self.mem, ent)
                )

    def player(self):
        return self.mem.handle.read_int(self.mem.client + dwEntityList + 0 * 0x10)
