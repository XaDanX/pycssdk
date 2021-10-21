
import pymem

from sdk.memory import *
from sdk.entity_list import EntityList
from sdk.local_player import LocalPlayer

from overlay.overlay import Overlay

from sdk.utils import w2s

mem = pymem.Pymem("csgo.exe")
memory = Memory(mem, pymem.process.module_from_name(mem.process_handle, "client.dll").lpBaseOfDll, pymem.process.module_from_name(mem.process_handle, "engine.dll").lpBaseOfDll)


ent_list = EntityList(memory)
player = LocalPlayer(memory, ent_list.player())
ent_list.update()

ov = Overlay("Counter-Strike: Global Offensive")

while True:

    ov.overlay_loop()

    for entity in ent_list.entity_list:
        if entity.validate_enemy() and entity.team() != player.team():
            pos = entity.position()
            w2s_pos = w2s(pos, player.view_matrix())
            head_pos = pos
            head_pos.z += 75
            w2s_head = w2s(head_pos, player.view_matrix())
            if w2s_pos is not None and w2s_head is not None:
                head = w2s_head[1] - w2s_pos[1]
                width = head / 2
                center = width / -2

                ov.line(1920 / 2, 0, w2s_pos[0], w2s_pos[1], 2, (0.53, 0.12, 0.47))

                ov.corner_box(w2s_pos[0] + center, w2s_pos[1], width, head + 5, 2, (0.53, 0.12, 0.47), (0, 0, 0))
            else:
                ent_list.update()



