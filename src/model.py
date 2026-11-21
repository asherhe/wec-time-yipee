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
    grid_cost: float

@dataclass
class EnergyAlloc:
    solar: float
    battery: float
    grid: float

    def total(self):
        return self.solar + self.battery + self.grid

@dataclass
class EnergyOutput:
    buildings: list[EnergyAlloc]
    generator: float

