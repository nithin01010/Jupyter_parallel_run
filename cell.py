from dataclasses import dataclass, field


@dataclass
class Cell:
    id: int
    source: str
    read: set = field(default_factory=set)
    write: set = field(default_factory=set)
