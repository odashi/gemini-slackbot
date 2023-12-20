import dataclasses
from typing import Literal


@dataclasses.dataclass
class Content:
    role: Literal["model", "user"]
    text: str
