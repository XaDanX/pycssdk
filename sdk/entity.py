from sdk.offsets import *
from sdk.utils import Vec3


class Entity:
    def __init__(self, mem, entity):
        self.mem = mem
        self.ent_id = entity

    def health(self):
        return self.mem.handle.read_int(self.ent_id + m_iHealth)

    def team(self):
        return self.mem.handle.read_int(self.ent_id + m_iTeamNum)

    def dormant(self):
        return self.mem.handle.read_int(self.ent_id + m_bDormant)

    def position(self):
        x = self.mem.handle.read_float(self.ent_id + m_vecOrigin)
        y = self.mem.handle.read_float(self.ent_id + m_vecOrigin + 0x4)
        z = self.mem.handle.read_float(self.ent_id + m_vecOrigin + 0x8)
        return Vec3(x, y, z)

    def bone_pos(self, bone_id):
        base = self.mem.handle.read_int(self.ent_id + m_dwBoneMatrix)
        x = self.mem.handle.read_float(base + 0x30 * bone_id + 0x0c)
        y = self.mem.handle.read_float(base + 0x30 * bone_id + 0x1c)
        z = self.mem.handle.read_float(base + 0x30 * bone_id + 0x2c)
        return Vec3(x, y, z)

    def validate_enemy(self):
        if self.dormant() == 0 and self.health() > 0:
            return True

    def model_type(self):
        return self.mem.handle.read_string(self.ent_id + model_ambient_min)
