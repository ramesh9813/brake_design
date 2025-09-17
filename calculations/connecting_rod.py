from dataclasses import dataclass
import numpy as np

@dataclass
class ConnectingRodInput:
    piston_diameter: float
    max_combustion_pressure: float
    reciprocating_mass: float
    crank_radius: float
    piston_pin_diameter: float
    crankpin_diameter: float
    max_engine_rpm: float
    rod_material_yield_strength: float
    bolt_material_yield_strength: float
    safety_factor: float

@dataclass
class ConnectingRodOutput:
    big_end_shank_height: str
    big_end_flange_width: str
    small_end_shank_height: str
    small_end_flange_width: str
    web_and_flange_thickness: str
    bolt_diameter: str
    small_end_outer_diameter: str
    small_end_wall_thickness: str
    big_end_outer_diameter: str
    big_end_wall_thickness: str

def calculate_connecting_rod(inputs: ConnectingRodInput) -> ConnectingRodOutput:
    max_gas_force = inputs.max_combustion_pressure * (np.pi * inputs.piston_diameter**2 / 4)
    allowable_compressive_stress = inputs.rod_material_yield_strength / inputs.safety_factor
    shank_area = max_gas_force / allowable_compressive_stress
    t = np.sqrt(shank_area / 11)
    web_and_flange_thickness = t
    big_end_shank_height = 5 * t
    big_end_flange_width = 4 * t
    taper_ratio = 0.8
    small_end_shank_height = big_end_shank_height * taper_ratio
    small_end_flange_width = big_end_flange_width * taper_ratio
    angular_velocity = inputs.max_engine_rpm * 2 * np.pi / 60
    max_inertial_force = inputs.reciprocating_mass * (inputs.crank_radius / 1000) * angular_velocity**2
    force_per_bolt = max_inertial_force / 2
    allowable_bolt_stress = inputs.bolt_material_yield_strength / inputs.safety_factor
    required_bolt_core_area = force_per_bolt / allowable_bolt_stress
    bolt_core_diameter = np.sqrt(4 * required_bolt_core_area / np.pi)
    bolt_diameter = bolt_core_diameter / 0.85
    small_end_wall_thickness = inputs.piston_pin_diameter * 0.35
    small_end_outer_diameter = inputs.piston_pin_diameter + (2 * small_end_wall_thickness)
    big_end_wall_thickness = inputs.crankpin_diameter * 0.35
    big_end_outer_diameter = inputs.crankpin_diameter + (2 * big_end_wall_thickness)

    return ConnectingRodOutput(
        big_end_shank_height=f'{big_end_shank_height:.2f} mm',
        big_end_flange_width=f'{big_end_flange_width:.2f} mm',
        small_end_shank_height=f'{small_end_shank_height:.2f} mm',
        small_end_flange_width=f'{small_end_flange_width:.2f} mm',
        web_and_flange_thickness=f'{web_and_flange_thickness:.2f} mm',
        bolt_diameter=f'{bolt_diameter:.2f} mm',
        small_end_outer_diameter=f'{small_end_outer_diameter:.2f} mm',
        small_end_wall_thickness=f'{small_end_wall_thickness:.2f} mm',
        big_end_outer_diameter=f'{big_end_outer_diameter:.2f} mm',
        big_end_wall_thickness=f'{big_end_wall_thickness:.2f} mm'
    )
