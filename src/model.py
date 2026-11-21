from dataclasses import dataclass
from enum import Enum, auto


class RandomEvent(Enum):
    NONE = auto()
    CLOUDY_WEATHER = auto()
    GENERATOR_FAILURE = auto()
    BATTERY_FAILURE = auto()
    GRID_FAILURE = auto()

@dataclass
class BuildingLoad:
    type: str
    load: int

@dataclass
class HourlyState:
    random_event: RandomEvent
    forecast: bool # True if cloudy
    loads: list[BuildingLoad]
    grid_price: float

@dataclass
class EnergyAlloc:
    solar: float
    battery: float
    grid: float

@dataclass
class EnergyOutput:
    buildings: list[EnergyAlloc]
    generator: float

