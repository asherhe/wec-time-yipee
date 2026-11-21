from model import BuildingLoad, EnergyAlloc, EnergyOutput, HourlyState, RandomEvent


class Control:
    def update(self, state: HourlyState) -> EnergyOutput:
        return EnergyOutput(
            buildings=[],
            generator=0.0,
        )


class PredictControl(Control):
    def __init__(self):
        self.battery_charge = 0.0

        # low-pass filter
        self.fc = 0.20  # cutoff frequency
        self.raw_loads: list[float] = []  # raw load history
        self.lp_loads: list[float] = []  # low-pass load history

        self.t0 = 0.0  # time when grid price exceeds 1.0
        self.t1 = 0.0  # time of maximum use
        self.t2 = 0.0  # time when grid price returns below 1.0

        self.hour = 0

    def get_loads(self) -> tuple[int, int]:
        lec_load = 0  # lecture halls, no solar power
        solar_load = 0  # can be powered by solar
        for load in self.state.loads:
            if load.type == "lecture_hall":
                lec_load += load.load
            else:
                solar_load += load.load
        return lec_load, solar_load

    def low_pass_calc(self, load: float):
        t = 1.0
        RC = 1.0 / (6.2832 * self.fc)
        alpha = t / (RC + t)

        self.raw_loads.append(load)
        prev_load = self.raw_loads[-1] if self.raw_loads else load
        self.lp_loads.append(prev_load + alpha * (load - prev_load))

    def build_output(self) -> EnergyOutput:
        # build output tables
        buildings = [EnergyAlloc(0, 0, 0) for l in self.state.loads]
        # exhuast solar
        for i, l in enumerate(self.state.loads):
            if l.type != "lecture_hall":
                buildings[i].solar = min(self.solar_use, l.load)
                self.solar_use -= buildings[i].solar

        # use up battery and grid
        additional_grid = 0.0  # unaccounted grid use
        for i, l in enumerate(self.state.loads):
            energy_req = l.load - buildings[i].total()

            battery_alloc = min(energy_req, self.battery_use)
            buildings[i].battery += battery_alloc
            self.battery_use -= battery_alloc
            energy_req -= battery_alloc

            grid_alloc = min(energy_req, self.grid_use)
            buildings[i].grid += grid_alloc
            self.grid_use -= grid_alloc
            energy_req -= grid_alloc

            additional_grid += energy_req
            buildings[i].grid += energy_req

        if additional_grid > 0.0:
            print(f"WARN: consumed {additional_grid} units of unaccounted grid power")

        self.battery_charge += self.gen_units

        return EnergyOutput(buildings=buildings, generator=self.gen_units)

    def update(self, state: HourlyState) -> EnergyOutput:
        self.hour += 1

        self.state = state

        lec_load, solar_load = self.get_loads()
        self.total_load = lec_load + solar_load
        # freeze original state
        LEC_LOAD_0, SOLAR_LOAD_0 = lec_load, solar_load
        TOTAL_LOAD_0 = self.total_load

        GEN_COST = 1.0
        SOLAR_LIMIT = 200.0

        has_solar = state.random_event != RandomEvent.CLOUDY_WEATHER

        self.battery_use = 0.0
        self.solar_use = 0.0
        self.grid_use = 0.0
        self.gen_units = 0.0

        self.low_pass_calc(self.total_load)

        if has_solar:
            self.solar_use += min(solar_load, SOLAR_LIMIT)
            solar_load -= self.solar_use
            self.total_load -= self.solar_use

        if state.grid_price <= GEN_COST and self.hour < 24:
            # it is cheaper to power the entire thing by grid
            # except for the final hour, discharge all battery in that case
            self.grid_use += self.total_load
            self.total_load = 0.0
        else:
            battery_alloc = min(self.battery_charge, self.total_load)
            self.battery_use += battery_alloc
            self.total_load -= battery_alloc
            self.battery_charge -= battery_alloc

        # linearly extrapolate next load
        next_load = self.lp_loads[-1]
        if len(self.lp_loads) > 1:
            next_load += self.lp_loads[-1] - self.lp_loads[-2]
        print(f"next (predicted) = {next_load}")
        if len(self.lp_loads) > 2:
            print(f"pred {self.lp_loads[-2] * 2 - self.lp_loads[-3]} actual {TOTAL_LOAD_0}")

        expected_solar = 200
        # TODO: using 200 as expected solar contribution
        target_battery = next_load - min(expected_solar, SOLAR_LOAD_0)
        self.gen_units = max(0, target_battery - self.battery_charge)

        return self.build_output()
