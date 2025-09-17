from dataclasses import dataclass
import numpy as np

@dataclass
class DiscInput:
    mass_vehicle: float
    mass_rider: float
    initial_velocity: float
    stopping_distance: float
    wheel_radius: float
    friction_coefficient: float
    caliper_piston_area: float
    hydraulic_pressure: float
    number_of_discs: int
    material_density: float
    material_specific_heat: float
    material_yield_strength: float
    max_outer_diameter: float
    initial_disc_thickness: float

@dataclass
class DiscOutput:
    braking_force: str
    braking_torque: str
    effective_radius: str
    outer_diameter: str
    inner_diameter: str
    thickness: str
    min_service_thickness: str
    disc_mass: str
    heat_energy: str
    temp_rise: str
    safety_factor: str

def calculate_disc(inputs: DiscInput) -> DiscOutput:
    # --- Unit Conversions ---
    initial_velocity_ms = inputs.initial_velocity * 1000 / 3600
    caliper_piston_area_m2 = inputs.caliper_piston_area / 10000
    hydraulic_pressure_pa = inputs.hydraulic_pressure * 1e6
    material_yield_strength_pa = inputs.material_yield_strength * 1e6
    max_outer_diameter_m = inputs.max_outer_diameter / 1000
    initial_disc_thickness_m = inputs.initial_disc_thickness / 1000

    # --- Calculation Logic ---
    total_mass = inputs.mass_vehicle + inputs.mass_rider
    deceleration = initial_velocity_ms**2 / (2 * inputs.stopping_distance)
    braking_force = total_mass * deceleration
    braking_torque = braking_force * inputs.wheel_radius

    # Disc geometry
    outer_diameter_m = max_outer_diameter_m
    inner_diameter_m = outer_diameter_m * 0.6  # Placeholder
    thickness_m = initial_disc_thickness_m
    effective_radius_m = (outer_diameter_m + inner_diameter_m) / 2 # Approximation

    # Performance calculations
    min_service_thickness_m = thickness_m * 0.8 # 20% wear
    disc_mass = np.pi * ((outer_diameter_m/2)**2 - (inner_diameter_m/2)**2) * thickness_m * inputs.material_density
    heat_energy = 0.5 * total_mass * initial_velocity_ms**2
    temp_rise = heat_energy / (disc_mass * inputs.material_specific_heat) if disc_mass > 0 else 0

    # Stress and safety factor
    clamping_force = hydraulic_pressure_pa * caliper_piston_area_m2
    frictional_force = 2 * clamping_force * inputs.friction_coefficient # For one disc with two pads
    max_stress = (frictional_force * effective_radius_m) / (np.pi * (outer_diameter_m**2 - inner_diameter_m**2) * thickness_m) if (outer_diameter_m**2 - inner_diameter_m**2) > 0 else 0
    safety_factor = material_yield_strength_pa / max_stress if max_stress > 0 else float('inf')

    return DiscOutput(
        braking_force=f'{braking_force:.2f} N',
        braking_torque=f'{braking_torque:.2f} Nm',
        effective_radius=f'{effective_radius_m * 1000:.2f} mm',
        outer_diameter=f'{outer_diameter_m * 1000:.2f} mm',
        inner_diameter=f'{inner_diameter_m * 1000:.2f} mm',
        thickness=f'{thickness_m * 1000:.2f} mm',
        min_service_thickness=f'{min_service_thickness_m * 1000:.2f} mm',
        disc_mass=f'{disc_mass:.2f} kg',
        heat_energy=f'{heat_energy / 1000:.2f} kJ',
        temp_rise=f'{temp_rise:.2f} °C',
        safety_factor=f'{safety_factor:.2f} (Simplified)'
    )
