from dataclasses import dataclass
import numpy as np

@dataclass
class BrakePadInput:
    total_mass: float
    initial_velocity: float
    stopping_distance: float
    pad_area: float
    pad_wear_rate: float
    pad_thickness: float

@dataclass
class BrakePadOutput:
    heat_flux: str
    wear_life: str

def calculate_brakepad(inputs: BrakePadInput) -> BrakePadOutput:
    initial_velocity_ms = inputs.initial_velocity * 1000 / 3600
    pad_area_m2 = inputs.pad_area / 10000

    deceleration = initial_velocity_ms**2 / (2 * inputs.stopping_distance)
    stopping_time = initial_velocity_ms / deceleration if deceleration > 0 else 0
    heat_energy = 0.5 * inputs.total_mass * initial_velocity_ms**2
    heat_flux = heat_energy / (pad_area_m2 * stopping_time) if (pad_area_m2 * stopping_time) > 0 else 0
    wear_life = (inputs.pad_thickness / inputs.pad_wear_rate) * 1000 if inputs.pad_wear_rate > 0 else float('inf')

    return BrakePadOutput(
        heat_flux=f'{heat_flux / 1000:.2f} kW/m²',
        wear_life=f'{wear_life:.2f} km'
    )
