from dataclasses import dataclass
import numpy as np

@dataclass
class WristPinInput:
    piston_diameter: float
    max_gas_pressure: float
    wrist_pin_material_yield_strength: float

@dataclass
class WristPinOutput:
    wrist_pin_outer_diameter: str
    wrist_pin_inner_diameter: str
    bearing_pressure: str
    bending_stress: str
    safety_factor: str

def calculate_wrist_pin(inputs: WristPinInput) -> WristPinOutput:
    # Simplified formulas based on common engineering practices
    
    # Outer diameter is often 0.25 to 0.4 of piston diameter
    wrist_pin_outer_diameter = inputs.piston_diameter * 0.35
    
    # Inner diameter is often 0.6 of outer diameter for hollow pins
    wrist_pin_inner_diameter = wrist_pin_outer_diameter * 0.6
    
    # Max gas force on piston
    max_gas_force = (np.pi / 4) * (inputs.piston_diameter**2) * inputs.max_gas_pressure
    
    # Bearing area
    bearing_area = wrist_pin_outer_diameter * (inputs.piston_diameter * 0.4) # Approximate length
    bearing_pressure = max_gas_force / bearing_area if bearing_area > 0 else 0
    
    # Bending moment (simplified)
    length_between_bosses = inputs.piston_diameter * 0.5 # Approximate
    bending_moment = (max_gas_force * length_between_bosses) / 8
    
    # Section modulus
    section_modulus = (np.pi / 32) * ((wrist_pin_outer_diameter**4 - wrist_pin_inner_diameter**4) / wrist_pin_outer_diameter)
    
    bending_stress = bending_moment / section_modulus if section_modulus > 0 else 0
    
    safety_factor = inputs.wrist_pin_material_yield_strength / bending_stress if bending_stress > 0 else float('inf')

    return WristPinOutput(
        wrist_pin_outer_diameter=f'{wrist_pin_outer_diameter:.2f} mm',
        wrist_pin_inner_diameter=f'{wrist_pin_inner_diameter:.2f} mm',
        bearing_pressure=f'{bearing_pressure:.2f} MPa',
        bending_stress=f'{bending_stress:.2f} MPa',
        safety_factor=f'{safety_factor:.2f}'
    )
