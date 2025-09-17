from dataclasses import dataclass
import numpy as np

@dataclass
class RimInput:
    tyre_width_mm: int
    tyre_aspect_ratio: int
    rim_diameter_inches: float
    proposed_rim_width_inches: float

@dataclass
class RimOutput:
    tyre_designation: str
    recommended_rim_width_range: str
    compatibility_note: str
    compatibility_class: str
    bead_seat_diameter_mm: str
    flange_height_mm: str

def calculate_rim_compatibility(inputs: RimInput) -> RimOutput:
    rim_data = {}
    if 90 <= inputs.tyre_width_mm <= 100:
        rim_data = {'design': 2.50, 'min': 2.15, 'max': 2.75}
    elif 110 <= inputs.tyre_width_mm <= 120:
        rim_data = {'design': 3.50, 'min': 3.00, 'max': 3.75}
    elif 130 <= inputs.tyre_width_mm <= 140:
        rim_data = {'design': 4.00, 'min': 3.50, 'max': 4.50}
    elif 150 <= inputs.tyre_width_mm <= 160:
        rim_data = {'design': 4.50, 'min': 4.25, 'max': 5.00}
    elif 170 <= inputs.tyre_width_mm <= 180:
        rim_data = {'design': 5.50, 'min': 5.00, 'max': 6.00}
    elif 190 <= inputs.tyre_width_mm <= 200:
        rim_data = {'design': 6.00, 'min': 5.50, 'max': 6.50}
    else:
        rim_data = None

    if rim_data:
        recommended_range = f'{rim_data["min"]:.2f}" to {rim_data["max"]:.2f}" (Ideal: {rim_data["design"]:.2f}")'
        if rim_data['min'] <= inputs.proposed_rim_width_inches <= rim_data['max']:
            if inputs.proposed_rim_width_inches == rim_data['design']:
                compatibility_note = "Ideal: Proposed rim width matches the tyre's design width."
                compatibility_class = "ideal"
            else:
                compatibility_note = "Acceptable: Proposed rim width is within the permitted range."
                compatibility_class = "acceptable"
        else:
            compatibility_note = "Not Recommended: Proposed rim width is outside the permitted range for this tyre."
            compatibility_class = "not-recommended"
    else:
        recommended_range = "N/A"
        compatibility_note = "Tyre width is outside the standard range for this calculator."
        compatibility_class = "not-recommended"

    bead_seat_diameter_mm = inputs.rim_diameter_inches * 25.4
    flange_height_mm = 17.5

    return RimOutput(
        tyre_designation=f'{inputs.tyre_width_mm}/{inputs.tyre_aspect_ratio}-{int(inputs.rim_diameter_inches)}',
        recommended_rim_width_range=recommended_range,
        compatibility_note=compatibility_note,
        compatibility_class=compatibility_class,
        bead_seat_diameter_mm=f'{bead_seat_diameter_mm:.2f} mm',
        flange_height_mm=f'{flange_height_mm:.1f} mm'
    )
