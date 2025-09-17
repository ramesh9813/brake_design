from dataclasses import dataclass
import numpy as np

@dataclass
class CaliperInput:
    required_braking_torque: float
    number_of_pistons: int
    hydraulic_pressure: float
    pad_contact_area: float
    number_of_discs: int
    caliper_material_yield_strength: float
    disc_effective_radius: float
    friction_coefficient: float

@dataclass
class CaliperOutput:
    total_clamp_force: str
    clamp_force_per_piston: str
    piston_diameter: str
    brake_torque_delivered: str
    caliper_stress: str
    safety_factor: str

def calculate_caliper(inputs: CaliperInput) -> CaliperOutput:
    hydraulic_pressure_pa = inputs.hydraulic_pressure * 1e6
    pad_contact_area_m2 = inputs.pad_contact_area / 10000

    total_clamp_force = inputs.required_braking_torque / (inputs.friction_coefficient * inputs.disc_effective_radius * inputs.number_of_discs * 2)
    clamp_force_per_piston = total_clamp_force / inputs.number_of_pistons
    piston_area = clamp_force_per_piston / hydraulic_pressure_pa
    piston_diameter_mm = 2 * np.sqrt(piston_area / np.pi) * 1000
    brake_torque_delivered = total_clamp_force * inputs.friction_coefficient * inputs.disc_effective_radius * inputs.number_of_discs * 2
    
    # Simplified stress calculation (assuming a basic caliper geometry)
    caliper_cross_section_area = 0.001 # m^2, placeholder value
    caliper_stress = total_clamp_force / caliper_cross_section_area if caliper_cross_section_area > 0 else 0
    safety_factor = inputs.caliper_material_yield_strength / (caliper_stress / 1e6) if caliper_stress > 0 else float('inf')


    return CaliperOutput(
        total_clamp_force=f'{total_clamp_force:.2f} N',
        clamp_force_per_piston=f'{clamp_force_per_piston:.2f} N',
        piston_diameter=f'{piston_diameter_mm:.2f} mm',
        brake_torque_delivered=f'{brake_torque_delivered:.2f} Nm',
        caliper_stress=f'{caliper_stress / 1e6:.2f} MPa',
        safety_factor=f'{safety_factor:.2f}'
    )
