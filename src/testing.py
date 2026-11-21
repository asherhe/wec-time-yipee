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
            battery_use = 0.0
            grid_use = 0.0
            for alloc in output.buildings:
                solar_use += alloc.solar
                battery_use += alloc.battery
                grid_use += alloc.grid

            assert solar_use <= 200.0
            assert battery_charge >= battery_use

            battery_charge += output.generator - battery_use
            total_cost += output.generator + grid_use * state.grid_price

            print(f"""\
Total cost        {total_cost}
Battery charge    {battery_charge}
Usage:
    Solar      {solar_use}
    Battery    {battery_use}
    Grid       {grid_use}
""")

        print(f"""\
========== run summary ========
TOTAL COST: {total_cost}
""")
        return total_cost

    def generate(self, hour) -> HourlyState:
        return HourlyState(
            random_event=RandomEvent.NONE,
            forecast=False,
            loads=[],
            grid_price=1.0,
        )
