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

    def update(self, state: HourlyState) -> EnergyOutput:
        lec_load = 0.0  # lecture halls, no solar power
        solar_load = 0.0  # can be powered by solar
        for load in state.loads:
            if load.type == "lecture_hall":
                lec_load += load.load
            else:
                solar_load += load.load

        GEN_COST = 1.0
        SOLAR_LIMIT = 200.0

        has_solar = state.random_event != RandomEvent.CLOUDY_WEATHER

        battery_use = 0.0
        solar_use = 0.0
        grid_use = 0.0
        gen_units = 0.0

        if has_solar:
            solar_use += min(solar_load, SOLAR_LIMIT)
            solar_load -= solar_use

        total_load = lec_load + solar_load

        # if grid_use < GEN_COST:
        #     grid_use += total_load
        #     total_load = 0.0

        grid_use += total_load
        total_load = 0.0

        # build output tables
        buildings = [EnergyAlloc(0, 0, 0) for l in state.loads]
        # exhuast solar
        for i, l in enumerate(state.loads):
            if l.type != "lecture_hall":
                buildings[i].solar = min(solar_use, l.load)
                solar_use -= buildings[i].solar
        # use up battery and grid
        for i, l in enumerate(state.loads):
            energy_req = l.load - buildings[i].total()

            battery_alloc = min(energy_req, battery_use)
            buildings[i].battery += battery_alloc
            battery_use -= battery_alloc
            energy_req -= battery_alloc

            grid_alloc = min(energy_req, grid_use)
            buildings[i].grid += grid_alloc
            grid_use -= grid_alloc
            energy_req -= grid_alloc

            assert(energy_req == 0)

        return EnergyOutput(
            buildings=buildings,
            generator=gen_units
        )

