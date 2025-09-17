from dataclasses import dataclass
import numpy as np

@dataclass
class ClutchInput:
    max_engine_torque: float
    outer_diameter: float
    friction_coefficient: float
    allowable_surface_pressure: float
    safety_factor: float

@dataclass
class ClutchOutput:
    clutch_type: str
    torque_capacity: str
    inner_diameter: str
    mean_radius: str
    required_clamping_force: str
    actual_surface_pressure: str
    viability_note: str
    viability_class: str

def calculate_clutch(inputs: ClutchInput) -> ClutchOutput:
    torque_capacity = inputs.max_engine_torque * inputs.safety_factor
    d_o = inputs.outer_diameter / 1000
    d_i = 0.6 * d_o
    inner_diameter_mm = d_i * 1000
    mean_radius_m = (d_o + d_i) / 4
    mean_radius_mm = mean_radius_m * 1000
    n = 2
    required_clamping_force = torque_capacity / (n * inputs.friction_coefficient * mean_radius_m)
    face_area = (np.pi / 4) * (d_o**2 - d_i**2)
    actual_surface_pressure = required_clamping_force / face_area
    actual_surface_pressure_mpa = actual_surface_pressure / 1e6

    if actual_surface_pressure_mpa <= inputs.allowable_surface_pressure:
        viability_note = "Design is viable. Surface pressure is within allowable limits."
        viability_class = "viable"
    else:
        viability_note = "Design NOT viable. Surface pressure exceeds limits. Increase outer diameter or check parameters."
        viability_class = "not-viable"

    return ClutchOutput(
        clutch_type='Single Plate Dry Clutch',
        torque_capacity=f'{torque_capacity:.2f} Nm',
        inner_diameter=f'{inner_diameter_mm:.2f} mm',
        mean_radius=f'{mean_radius_mm:.2f} mm',
        required_clamping_force=f'{required_clamping_force:.2f} N',
        actual_surface_pressure=f'{actual_surface_pressure_mpa:.3f} MPa',
        viability_note=viability_note,
        viability_class=viability_class
    )
