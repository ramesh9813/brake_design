from dataclasses import dataclass
import numpy as np

@dataclass
class PistonInput:
    cylinder_bore: float
    stroke_length: float
    connecting_rod_length: float
    deck_height: float
    max_combustion_pressure: float
    piston_material_strength: float
    safety_factor: float

@dataclass
class PistonOutput:
    piston_diameter: str
    piston_clearance: str
    compression_height: str
    crown_thickness: str
    max_piston_force: str
    gudgeon_pin_outer_diameter: str
    gudgeon_pin_inner_diameter: str
    piston_skirt_length: str

def calculate_piston(inputs: PistonInput) -> PistonOutput:
    piston_clearance = 0.00075 * inputs.cylinder_bore
    piston_diameter = inputs.cylinder_bore - piston_clearance
    compression_height = inputs.deck_height - (inputs.stroke_length / 2) - inputs.connecting_rod_length
    allowable_stress = inputs.piston_material_strength / inputs.safety_factor
    crown_thickness = np.sqrt((3 * inputs.max_combustion_pressure * inputs.cylinder_bore**2) / (16 * allowable_stress))
    max_piston_force = inputs.max_combustion_pressure * (np.pi * inputs.cylinder_bore**2 / 4)
    gudgeon_pin_outer_diameter = 0.25 * inputs.cylinder_bore
    bending_moment = (max_piston_force * inputs.cylinder_bore) / 8
    required_section_modulus = bending_moment / allowable_stress
    try:
        gudgeon_pin_inner_diameter_calc = (gudgeon_pin_outer_diameter**4 - (32 * required_section_modulus * gudgeon_pin_outer_diameter) / np.pi)**(1/4)
        if isinstance(gudgeon_pin_inner_diameter_calc, complex):
            gudgeon_pin_inner_diameter = 'Invalid'
        else:
            gudgeon_pin_inner_diameter = f'{gudgeon_pin_inner_diameter_calc:.2f} mm'
    except (ValueError, TypeError):
        gudgeon_pin_inner_diameter = 'Invalid'
    max_rod_angle = np.arcsin((inputs.stroke_length / 2) / inputs.connecting_rod_length)
    max_thrust = max_piston_force * np.tan(max_rod_angle)
    allowable_bearing_pressure = 0.7
    skirt_area = max_thrust / allowable_bearing_pressure
    piston_skirt_length = skirt_area / inputs.cylinder_bore

    return PistonOutput(
        piston_diameter=f'{piston_diameter:.2f} mm',
        piston_clearance=f'{piston_clearance:.4f} mm',
        compression_height=f'{compression_height:.2f} mm',
        crown_thickness=f'{crown_thickness:.2f} mm',
        max_piston_force=f'{max_piston_force:.2f} N',
        gudgeon_pin_outer_diameter=f'{gudgeon_pin_outer_diameter:.2f} mm',
        gudgeon_pin_inner_diameter=gudgeon_pin_inner_diameter,
        piston_skirt_length=f'{piston_skirt_length:.2f} mm'
    )
