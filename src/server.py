import json
import socket

from control import Control
from model import BuildingLoad, EnergyOutput, HourlyState, RandomEvent


def decode_state(data: dict):
    return HourlyState(
        random_event={
            "none": RandomEvent.NONE,
            "cloudy_weather": RandomEvent.CLOUDY_WEATHER,
            "generator_failure": RandomEvent.GENERATOR_FAILURE,
            "battery_failure": RandomEvent.BATTERY_FAILURE,
            "grid_failure": RandomEvent.GRID_FAILURE,
        }[data["random_event"]],
        forecast=data["forecast"] == "cloudy",
        loads=[
            BuildingLoad(type=load["type"], load=int(load["load"]))
            for load in data["loads"]
        ],
        grid_price=float(data["grid_price"]),
    )


def encode_out(out: EnergyOutput) -> dict:
    return {
        "buildings": [
            {"solar": a.solar, "battery": a.battery, "grid": a.grid}
            for a in out.buildings
        ],
        "generator": out.generator,
    }


class Server:
    """get inputs from testing server"""

    def __init__(self, host: str, port: int, control: Control):
        self.host = host
        self.port = port
        self.control = control

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            for _ in range(24):
                in_data = s.recv(1024).decode()
                hourly_state = decode_state(json.loads(in_data))
                print(hourly_state)
                out = self.control.update(hourly_state)
                out_data = json.dumps(encode_out(out))
                s.sendall(bytes(out_data, encoding="utf-8"))

if __name__ == "__main__":
    c = Control()
    s = Server("127.0.0.1", 8800, c)
    s.run()

