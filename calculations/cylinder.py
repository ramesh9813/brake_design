from dataclasses import dataclass
import numpy as np

@dataclass
class CylinderInput:
    cylinder_bore_diameter: float
    stroke_length: float
    max_combustion_pressure: float
    cylinder_material_strength: float
    safety_factor: float

@dataclass
class CylinderOutput:
    cylinder_wall_thickness: str
    outer_cylinder_diameter: str
    cylinder_length: str
    cylinder_flange_diameter: str
    cylinder_flange_thickness: str
    fin_note: str

def calculate_cylinder(inputs: CylinderInput) -> CylinderOutput:
    allowable_stress = inputs.cylinder_material_strength / inputs.safety_factor
    reboring_allowance = 1.5
    wall_thickness = ((inputs.max_combustion_pressure * inputs.cylinder_bore_diameter) / (2 * allowable_stress)) + reboring_allowance
    outer_cylinder_diameter = inputs.cylinder_bore_diameter + (2 * wall_thickness)
    cylinder_length = 1.15 * inputs.stroke_length
    flange_thickness = 1.3 * wall_thickness
    flange_diameter = 1.5 * outer_cylinder_diameter
    fin_note = "For air-cooled engines, fins are required. Typical dimensions are: Thickness (1.5-3mm), Height (25-50mm), and Spacing (2-5mm). Their final design requires detailed heat transfer analysis."

    return CylinderOutput(
        cylinder_wall_thickness=f'{wall_thickness:.2f} mm',
        outer_cylinder_diameter=f'{outer_cylinder_diameter:.2f} mm',
        cylinder_length=f'{cylinder_length:.2f} mm',
        cylinder_flange_diameter=f'{flange_diameter:.2f} mm',
        cylinder_flange_thickness=f'{flange_thickness:.2f} mm',
        fin_note=fin_note
    )
