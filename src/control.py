from .model import EnergyOutput, HourlyState


class Control:
    def update(self, state: HourlyState) -> EnergyOutput:
        return EnergyOutput(
            buildings=[],
            generator=0.0,
        )
