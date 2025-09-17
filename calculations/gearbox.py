from dataclasses import dataclass
import numpy as np

@dataclass
class GearboxInput:
    max_engine_torque: float
    primary_drive_ratio: float
    first_gear_ratio: float
    top_gear_ratio: float
    number_of_gears: int
    gear_material_strength: float
    safety_factor: float
    module: float
    pinion_teeth_1st_gear: int

@dataclass
class GearboxOutput:
    all_gear_ratios: list
    pinion_teeth: int
    gear_teeth: int
    face_width: str
    pinion_pitch_diameter: str
    gear_pitch_diameter: str
    center_distance: str

def calculate_gearbox(inputs: GearboxInput) -> GearboxOutput:
    progression_factor = (inputs.first_gear_ratio / inputs.top_gear_ratio)**(1 / (inputs.number_of_gears - 1))
    all_gear_ratios = [inputs.first_gear_ratio / (progression_factor**(n)) for n in range(inputs.number_of_gears)]
    torque_input_shaft = inputs.max_engine_torque * inputs.primary_drive_ratio
    z1 = inputs.pinion_teeth_1st_gear
    z2 = round(z1 * inputs.first_gear_ratio)
    d1 = inputs.module * z1
    d2 = inputs.module * z2
    tangential_force = torque_input_shaft / (d1 / 2 / 1000)
    lewis_form_factor = 0.484 - (2.87 / z1)
    allowable_stress = inputs.gear_material_strength / inputs.safety_factor
    face_width_m = tangential_force / ((allowable_stress * 1e6) * np.pi * (inputs.module / 1000) * lewis_form_factor)
    face_width_mm = face_width_m * 1000
    center_distance = (d1 + d2) / 2

    return GearboxOutput(
        all_gear_ratios=[f'{r:.3f}:1' for r in all_gear_ratios],
        pinion_teeth=z1,
        gear_teeth=z2,
        face_width=f'{face_width_mm:.2f} mm',
        pinion_pitch_diameter=f'{d1:.2f} mm',
        gear_pitch_diameter=f'{d2:.2f} mm',
        center_distance=f'{center_distance:.2f} mm'
    )
