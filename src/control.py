from model import EnergyOutput, HourlyState


class Control:
    def update(self, state: HourlyState) -> EnergyOutput:
        return EnergyOutput(
            buildings=[],
            generator=0.0,
        )


loop through buildings
split buildings into two lists
    lecture hall as one and then the rest as the other
two sums:
    one sum is lecture hall load sums
    other is oother ones' load sum
    see if load sum <= 200
        if it is load_other sum = 0.0
        else load_other -= 200
if price-of-grid > 1:
    use battery; if load_other sum < current_battery: load_other sum = 0
        current battery -= load_other_sum;
    else: load_other_sum -= current_battery
    current_battery = 0 
if lecture_hall_sum <= current_battery:
    lecture_hall_sum = 0;
else lecture_hall_sum -= current_battery;
current_battery = 0

grid = grid_price * (load_other_sum + lecture_hall_sum)
