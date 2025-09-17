from dataclasses import dataclass
import numpy as np

@dataclass
class ChainSprocketInput:
    max_engine_power: float
    small_sprocket_rpm: float
    chain_type: str
    small_sprocket_teeth: int
    large_sprocket_teeth: int
    center_distance_mm: float

@dataclass
class ChainSprocketOutput:
    final_drive_ratio: str
    chain_pitch_mm: str
    chain_length_links: int
    chain_length_mm: str
    small_sprocket_pcd: str
    small_sprocket_od: str
    large_sprocket_pcd: str
    large_sprocket_od: str
    factor_of_safety: str
    viability_note: str
    viability_class: str

def calculate_chain_sprocket(inputs: ChainSprocketInput) -> ChainSprocketOutput:
    chain_data = {
        '520': {'pitch': 15.875, 'strength_N': 35000},
        '525': {'pitch': 15.875, 'strength_N': 40000},
        '530': {'pitch': 15.875, 'strength_N': 45000}
    }
    P = chain_data[inputs.chain_type]['pitch']
    T1 = inputs.small_sprocket_teeth
    T2 = inputs.large_sprocket_teeth
    C = inputs.center_distance_mm
    final_drive_ratio = T2 / T1
    L_p = 2*(C/P) + (T1+T2)/2 + ((T2-T1)/(2*np.pi))**2 * (P/C)
    chain_length_links = int(np.ceil(L_p / 2.) * 2)
    chain_length_mm = chain_length_links * P
    small_sprocket_pcd = P / np.sin(np.deg2rad(180 / T1))
    small_sprocket_od = P * (0.6 + (1 / np.tan(np.deg2rad(180 / T1))))
    large_sprocket_pcd = P / np.sin(np.deg2rad(180 / T2))
    large_sprocket_od = P * (0.6 + (1 / np.tan(np.deg2rad(180 / T2))))
    service_factor = 1.2
    design_power_kw = inputs.max_engine_power * service_factor
    chain_velocity_ms = (inputs.small_sprocket_rpm * T1 * P) / (60 * 1000)
    working_load_N = (design_power_kw * 1000) / chain_velocity_ms if chain_velocity_ms > 0 else 0
    breaking_strength_N = chain_data[inputs.chain_type]['strength_N']
    factor_of_safety = breaking_strength_N / working_load_N if working_load_N > 0 else float('inf')

    if factor_of_safety > 10:
        viability_note = "Chain selection is safe for the given load."
        viability_class = "viable"
    else:
        viability_note = "Warning: Factor of safety is low. Consider a stronger chain or different parameters."
        viability_class = "not-viable"

    return ChainSprocketOutput(
        final_drive_ratio=f'{final_drive_ratio:.2f}:1',
        chain_pitch_mm=f'{P:.3f} mm',
        chain_length_links=chain_length_links,
        chain_length_mm=f'{chain_length_mm:.2f}',
        small_sprocket_pcd=f'{small_sprocket_pcd:.2f} mm',
        small_sprocket_od=f'{small_sprocket_od:.2f} mm',
        large_sprocket_pcd=f'{large_sprocket_pcd:.2f} mm',
        large_sprocket_od=f'{large_sprocket_od:.2f} mm',
        factor_of_safety=f'{factor_of_safety:.2f}',
        viability_note=viability_note,
        viability_class=viability_class
    )
