import random

from control import Control
from model import BuildingLoad, EnergyOutput, HourlyState, RandomEvent


class Testing:
    def __init__(self, control: Control, seed: int = 69420):
        self.control = control
        random.seed(seed)

    def run(self):
        self.total_cost = 0.0
        self.battery_charge = 0.0
        cases = self.generate()

        for hour, state in enumerate(cases):
            print(f"==== Hour {hour} ====")
            output = self.control.update(state)
            self.update(output, state)

        print(f"""\
========== run summary ========
TOTAL COST: {self.total_cost}
""")
        return self.total_cost

    def update(self, output: EnergyOutput, state: HourlyState):
        solar_use = 0.0
        battery_use = 0.0
        grid_use = 0.0
        for alloc in output.buildings:
            solar_use += alloc.solar
            battery_use += alloc.battery
            grid_use += alloc.grid

        assert solar_use <= 200.0
        assert self.battery_charge >= battery_use

        self.battery_charge += output.generator - battery_use
        self.total_cost += output.generator + grid_use * state.grid_price

        print(f"""\
Total cost        {self.total_cost}
Battery charge    {self.battery_charge}
Usage:
    Solar      {solar_use}
    Battery    {battery_use}
    Grid       {grid_use}
""")

    def generate(self) -> list[HourlyState]:
        HOURS = 24

        event_seq = random.choices(
            [
                RandomEvent.NONE,
                RandomEvent.CLOUDY_WEATHER,
                RandomEvent.GENERATOR_FAILURE,
                RandomEvent.BATTERY_FAILURE,
                RandomEvent.GRID_FAILURE,
            ],
            k=HOURS + 1,
        )

        num_buildings = random.randint(7, 10)
        buildings = random.choices(
            [
                "library",
                "laboratory",
                "lecture_hall",
                "student_centre",
                "student_residence",
            ],
            k=num_buildings,
        )

        states = []
        for i in range(HOURS):
            next_event = event_seq[i + 1]

            forecast = next_event == RandomEvent.CLOUDY_WEATHER
            if random.random() >= 0.75:  # 75% correctness
                forecast = not forecast

            # random ass curve that peaks during school hours, 9-17
            base_power = 1.0 / (1.0 + 0.05 * (i - 13.0) ** 2)

            building_loads = [
                int((base_power + 0.2 * (random.random() - 0.5)) * 65 + 5)
                for b in buildings
            ]

            states.append(
                HourlyState(
                    random_event=event_seq[i],
                    forecast=forecast,
                    loads=[
                        BuildingLoad(type, load)
                        for type, load in zip(buildings, building_loads)
                    ],
                    grid_price=0.5 + (2 - 0.5) * random.random(),
                )
            )

        return states
