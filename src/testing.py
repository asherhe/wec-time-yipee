import random
from control import Control
from model import BuildingLoad, HourlyState, RandomEvent

class Testing:
    def __init__(self, control: Control):
        self.control = control
        self.hours = 24
        self.building_count = 10

    def run(self):
        total_cost = 0.0
        battery_charge = 0.0

        for hour in range(self.hours):
            print(f"==== Hour {hour} ====")

            state = self.generate(hour)
            output = self.control.update(state)
            
            solar_use = 0.0
            grid_use = 0.0
            for alloc in output.buildings:
                solar_use += alloc.solar
                battery_charge -= alloc.battery
                grid_use += alloc.grid

            assert(solar_use <= 200.0)
            assert(battery_charge >= 0.0)

            battery_charge += output.generator
            total_cost += output.generator + grid_use * state.grid_price
            print()

        return total_cost

     
    def generate(self, hour) -> HourlyState:
        ...

