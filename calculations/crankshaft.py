from dataclasses import dataclass
import numpy as np

@dataclass
class CrankshaftInput:
    piston_diameter: float
    max_combustion_pressure: float
    cylinder_bore_spacing: float
    crankshaft_material_yield_strength: float
    allowable_bearing_pressure: float
    safety_factor: float

@dataclass
class CrankshaftOutput:
    crankpin_diameter: str
    crankpin_length: str
    main_journal_diameter: str
    main_journal_length: str
    crank_web_thickness: str
    crank_web_width: str

def calculate_crankshaft(inputs: CrankshaftInput) -> CrankshaftOutput:
    max_gas_force = inputs.max_combustion_pressure * (np.pi * inputs.piston_diameter**2 / 4)
    allowable_bending_stress = inputs.crankshaft_material_yield_strength / inputs.safety_factor
    bending_moment = max_gas_force * (inputs.cylinder_bore_spacing / 1000) / 2
    crankpin_diameter_m = ( (32 * bending_moment) / (np.pi * (allowable_bending_stress * 1e6)) )**(1/3)
    crankpin_diameter = crankpin_diameter_m * 1000
    projected_area_crankpin = max_gas_force / (inputs.allowable_bearing_pressure * 1e6)
    crankpin_length_m = projected_area_crankpin / crankpin_diameter_m
    crankpin_length = crankpin_length_m * 1000
    main_journal_diameter = 1.15 * crankpin_diameter
    projected_area_main = max_gas_force / (inputs.allowable_bearing_pressure * 1e6)
    main_journal_length_m = projected_area_main / (main_journal_diameter / 1000)
    main_journal_length = main_journal_length_m * 1000
    crank_web_thickness = 0.5 * crankpin_diameter
    crank_web_width = 1.25 * crankpin_diameter

    return CrankshaftOutput(
        crankpin_diameter=f'{crankpin_diameter:.2f} mm',
        crankpin_length=f'{crankpin_length:.2f} mm',
        main_journal_diameter=f'{main_journal_diameter:.2f} mm',
        main_journal_length=f'{main_journal_length:.2f} mm',
        crank_web_thickness=f'{crank_web_thickness:.2f} mm',
        crank_web_width=f'{crank_web_width:.2f} mm'
    )
