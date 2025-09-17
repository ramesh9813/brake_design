from dataclasses import dataclass
import numpy as np

@dataclass
class TyreInput:
    bike_type: str
    vehicle_mass: float
    rim_diameter: float
    aspect_ratio: float
    section_width: float

@dataclass
class TyreOutput:
    section_height: str
    overall_diameter: str
    tread_thickness: str
    sidewall_thickness: str
    bead_size: str
    crown_radius: str
    contact_patch_area: str

def calculate_tyre(inputs: TyreInput) -> TyreOutput:
    section_height = (inputs.aspect_ratio / 100) * inputs.section_width
    overall_diameter = (2 * section_height) + (inputs.rim_diameter * 25.4)

    tread_thickness_map = {
        'commuter': 7,
        'sports': 8,
        'superbike': 8.5,
        'cruiser_touring': 9,
        'offroad': 11
    }
    tread_thickness = tread_thickness_map.get(inputs.bike_type, 8)

    sidewall_thickness = 0.08 * section_height
    bead_size = 17.5
    crown_radius = 1.7 * inputs.section_width

    load_per_tyre = (inputs.vehicle_mass * 9.81) / 2
    inflation_pressure = 225000
    contact_patch_area = load_per_tyre / inflation_pressure

    return TyreOutput(
        section_height=f'{section_height:.2f} mm',
        overall_diameter=f'{overall_diameter:.2f} mm',
        tread_thickness=f'{tread_thickness:.2f} mm',
        sidewall_thickness=f'{sidewall_thickness:.2f} mm',
        bead_size=f'{bead_size:.2f} mm',
        crown_radius=f'{crown_radius:.2f} mm',
        contact_patch_area=f'{contact_patch_area:.4f} m²'
    )
