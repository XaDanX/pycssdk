from dataclasses import dataclass
import pymem


@dataclass
class Memory:
    handle: pymem.Pymem
    client: None
    engine: None
