import random
from control import Control
from model import BuildingLoad, HourlyState, RandomEvent


class Testing:
    def __init__(self, control: Control):
        self.control = control

    def run(self):
        self.total_cost = 0.0
        self.battery_charge = 0.0
        cases = self.generate()

        for hour, state in enumerate(cases):
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

        states = []
        for i in range(HOURS):
            next_event = event_seq[i + 1]

            forecast = next_event == RandomEvent.CLOUDY_WEATHER
            if random.random() >= 0.75:  # 75% correctness
                forecast = not forecast

            states.append(
                HourlyState(
                    random_event=event_seq[i],
                    forecast=forecast,
                    loads=[],
                    grid_price=0.5 * (2 - 0.5) * random.random(),
                )
            )
        return states
