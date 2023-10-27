from dataclasses import dataclass, field

from model.method import Method


@dataclass
class Resource:
    url: str
    method: Method = Method.GET
    body: str = ''
    headers: dict[str, str] = field(default_factory=dict)
