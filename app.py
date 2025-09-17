from flask import Flask, render_template, request, url_for
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disc', methods=['GET', 'POST'])
def disc():
    if request.method == 'POST':
        # Get inputs from the form
        mass_vehicle = float(request.form['mass_vehicle'])
        mass_rider = float(request.form['mass_rider'])
        initial_velocity_kmh = float(request.form['initial_velocity'])
        stopping_distance = float(request.form['stopping_distance'])
        wheel_radius = float(request.form['wheel_radius'])
        friction_coefficient = float(request.form['friction_coefficient'])
        caliper_piston_area_cm2 = float(request.form['caliper_piston_area'])
        hydraulic_pressure_mpa = float(request.form['hydraulic_pressure'])
        number_of_discs = int(request.form['number_of_discs'])
        material_density = float(request.form['material_density'])
        material_specific_heat = float(request.form['material_specific_heat'])
        material_yield_strength_mpa = float(request.form['material_yield_strength'])
        max_outer_diameter_mm = float(request.form['max_outer_diameter'])
        initial_disc_thickness_mm = float(request.form['initial_disc_thickness'])

        # --- Unit Conversions ---
        initial_velocity_ms = initial_velocity_kmh * 1000 / 3600
        caliper_piston_area_m2 = caliper_piston_area_cm2 / 10000
        hydraulic_pressure_pa = hydraulic_pressure_mpa * 1e6
        material_yield_strength_pa = material_yield_strength_mpa * 1e6
        max_outer_diameter_m = max_outer_diameter_mm / 1000
        initial_disc_thickness_m = initial_disc_thickness_mm / 1000

        # --- Calculation Logic ---
        total_mass = mass_vehicle + mass_rider
        deceleration = initial_velocity_ms**2 / (2 * stopping_distance)
        braking_force = total_mass * deceleration
        braking_torque = braking_force * wheel_radius

        # Disc geometry
        outer_diameter_m = max_outer_diameter_m
        inner_diameter_m = outer_diameter_m * 0.6  # Placeholder
        thickness_m = initial_disc_thickness_m
        effective_radius_m = (outer_diameter_m + inner_diameter_m) / 2 # Approximation

        # Performance calculations
        min_service_thickness_m = thickness_m * 0.8 # 20% wear
        disc_mass = np.pi * ((outer_diameter_m/2)**2 - (inner_diameter_m/2)**2) * thickness_m * material_density
        heat_energy = 0.5 * total_mass * initial_velocity_ms**2
        temp_rise = heat_energy / (disc_mass * material_specific_heat) if disc_mass > 0 else 0

        # Stress and safety factor
        clamping_force = hydraulic_pressure_pa * caliper_piston_area_m2
        frictional_force = 2 * clamping_force * friction_coefficient # For one disc with two pads
        # Simplified stress calculation (placeholder, real-world stress analysis is complex)
        max_stress = (frictional_force * effective_radius_m) / (np.pi * (outer_diameter_m**2 - inner_diameter_m**2) * thickness_m) if (outer_diameter_m**2 - inner_diameter_m**2) > 0 else 0
        safety_factor = material_yield_strength_pa / max_stress if max_stress > 0 else float('inf')


        return render_template('disc_brake.html', results={
            'braking_force': f'{braking_force:.2f} N',
            'braking_torque': f'{braking_torque:.2f} Nm',
            'effective_radius': f'{effective_radius_m * 1000:.2f} mm',
            'outer_diameter': f'{outer_diameter_m * 1000:.2f} mm',
            'inner_diameter': f'{inner_diameter_m * 1000:.2f} mm',
            'thickness': f'{thickness_m * 1000:.2f} mm',
            'min_service_thickness': f'{min_service_thickness_m * 1000:.2f} mm',
            'disc_mass': f'{disc_mass:.2f} kg',
            'heat_energy': f'{heat_energy / 1000:.2f} kJ',
            'temp_rise': f'{temp_rise:.2f} °C',
            'safety_factor': f'{safety_factor:.2f} (Simplified)'
        })
    return render_template('disc_brake.html', results=None)

@app.route('/caliper', methods=['GET', 'POST'])
def caliper():
    if request.method == 'POST':
        # Get inputs from the form
        required_braking_torque = float(request.form['required_braking_torque'])
        number_of_pistons = int(request.form['number_of_pistons'])
        hydraulic_pressure_mpa = float(request.form['hydraulic_pressure'])
        pad_contact_area_cm2 = float(request.form['pad_contact_area'])
        number_of_discs = int(request.form['number_of_discs'])
        caliper_material_yield_strength_mpa = float(request.form['caliper_material_yield_strength'])
        disc_effective_radius = float(request.form['disc_effective_radius'])
        friction_coefficient = float(request.form['friction_coefficient'])

        # --- Unit Conversions ---
        hydraulic_pressure_pa = hydraulic_pressure_mpa * 1e6
        pad_contact_area_m2 = pad_contact_area_cm2 / 10000
        caliper_material_yield_strength_pa = caliper_material_yield_strength_mpa * 1e6

        # --- Calculation Logic ---
        total_clamp_force = required_braking_torque / (friction_coefficient * disc_effective_radius * number_of_discs * 2)
        clamp_force_per_piston = total_clamp_force / number_of_pistons
        piston_area = clamp_force_per_piston / hydraulic_pressure_pa
        piston_diameter_mm = 2 * np.sqrt(piston_area / np.pi) * 1000
        brake_torque_delivered = total_clamp_force * friction_coefficient * disc_effective_radius * number_of_discs * 2
        
        # Simplified stress calculation (placeholder, real-world stress analysis is complex)
        pad_pressure = total_clamp_force / pad_contact_area_m2 if pad_contact_area_m2 > 0 else 0

        return render_template('caliper_design.html', results={
            'total_clamp_force': f'{total_clamp_force:.2f} N',
            'clamp_force_per_piston': f'{clamp_force_per_piston:.2f} N',
            'piston_diameter': f'{piston_diameter_mm:.2f} mm',
            'brake_torque_delivered': f'{brake_torque_delivered:.2f} Nm',
            'pad_pressure': f'{pad_pressure / 1e6:.2f} MPa'
        })
    return render_template('caliper_design.html', results=None)

@app.route('/brakepad', methods=['GET', 'POST'])
def brakepad():
    if request.method == 'POST':
        # Get inputs from the form
        total_mass = float(request.form['total_mass'])
        initial_velocity_kmh = float(request.form['initial_velocity'])
        stopping_distance = float(request.form['stopping_distance'])
        pad_area_cm2 = float(request.form['pad_area'])
        pad_wear_rate = float(request.form['pad_wear_rate'])
        pad_thickness_mm = float(request.form['pad_thickness'])

        # --- Unit Conversions ---
        initial_velocity_ms = initial_velocity_kmh * 1000 / 3600
        pad_area_m2 = pad_area_cm2 / 10000

        # --- Calculation Logic ---
        deceleration = initial_velocity_ms**2 / (2 * stopping_distance)
        stopping_time = initial_velocity_ms / deceleration if deceleration > 0 else 0
        heat_energy = 0.5 * total_mass * initial_velocity_ms**2
        heat_flux = heat_energy / (pad_area_m2 * stopping_time) if (pad_area_m2 * stopping_time) > 0 else 0
        wear_life = (pad_thickness_mm / pad_wear_rate) * 1000 if pad_wear_rate > 0 else float('inf')

        return render_template('brake_pad_design.html', results={
            'heat_flux': f'{heat_flux / 1000:.2f} kW/m²',
            'wear_life': f'{wear_life:.2f} km'
        })
    return render_template('brake_pad_design.html', results=None)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/tyre', methods=['GET', 'POST'])
def tyre():
    if request.method == 'POST':
        # Get inputs from the form
        bike_type = request.form['bike_type']
        vehicle_mass = float(request.form['vehicle_mass'])
        rim_diameter = float(request.form['rim_diameter'])
        aspect_ratio = float(request.form['aspect_ratio'])
        section_width = float(request.form['section_width'])

        # --- Calculation Logic ---
        section_height = (aspect_ratio / 100) * section_width
        overall_diameter = (2 * section_height) + (rim_diameter * 25.4)

        tread_thickness_map = {
            'commuter': 7,
            'sports': 8,
            'superbike': 8.5,
            'cruiser_touring': 9,
            'offroad': 11
        }
        tread_thickness = tread_thickness_map.get(bike_type, 8) # Default to 8 if not found

        sidewall_thickness = 0.08 * section_height
        bead_size = 17.5 # Average of 15-20
        crown_radius = 1.7 * section_width

        load_per_tyre = (vehicle_mass * 9.81) / 2
        inflation_pressure = 225000 # Average of 200-250 kPa in Pa
        contact_patch_area = load_per_tyre / inflation_pressure

        return render_template('tyre_design.html', results={
            'section_height': f'{section_height:.2f} mm',
            'overall_diameter': f'{overall_diameter:.2f} mm',
            'tread_thickness': f'{tread_thickness:.2f} mm',
            'sidewall_thickness': f'{sidewall_thickness:.2f} mm',
            'bead_size': f'{bead_size:.2f} mm',
            'crown_radius': f'{crown_radius:.2f} mm',
            'contact_patch_area': f'{contact_patch_area:.4f} m²'
        })
    return render_template('tyre_design.html', results=None)

@app.route('/piston', methods=['GET', 'POST'])
def piston():
    if request.method == 'POST':
        # Get inputs from the form
        cylinder_bore = float(request.form['cylinder_bore'])
        stroke_length = float(request.form['stroke_length'])
        connecting_rod_length = float(request.form['connecting_rod_length'])
        deck_height = float(request.form['deck_height'])
        max_combustion_pressure = float(request.form['max_combustion_pressure'])
        piston_material_strength = float(request.form['piston_material_strength'])
        safety_factor = float(request.form['safety_factor'])

        # --- Calculation Logic ---
        # Piston Diameter and Clearance
        piston_clearance = 0.00075 * cylinder_bore
        piston_diameter = cylinder_bore - piston_clearance

        # Compression Height
        compression_height = deck_height - (stroke_length / 2) - connecting_rod_length

        # Crown Thickness
        allowable_stress = piston_material_strength / safety_factor
        crown_thickness = np.sqrt((3 * max_combustion_pressure * cylinder_bore**2) / (16 * allowable_stress))

        # Max Piston Force
        max_piston_force = max_combustion_pressure * (np.pi * cylinder_bore**2 / 4)

        # Gudgeon Pin
        gudgeon_pin_outer_diameter = 0.25 * cylinder_bore
        bending_moment = (max_piston_force * cylinder_bore) / 8
        required_section_modulus = bending_moment / allowable_stress
        try:
            gudgeon_pin_inner_diameter_calc = (gudgeon_pin_outer_diameter**4 - (32 * required_section_modulus * gudgeon_pin_outer_diameter) / np.pi)**(1/4)
            if isinstance(gudgeon_pin_inner_diameter_calc, complex):
                gudgeon_pin_inner_diameter = 'Invalid' # Indicates parameters result in non-real solution
            else:
                gudgeon_pin_inner_diameter = f'{gudgeon_pin_inner_diameter_calc:.2f} mm'
        except (ValueError, TypeError):
            gudgeon_pin_inner_diameter = 'Invalid'

        # Piston Skirt Length
        max_rod_angle = np.arcsin((stroke_length / 2) / connecting_rod_length)
        max_thrust = max_piston_force * np.tan(max_rod_angle)
        allowable_bearing_pressure = 0.7 # MPa, typical value
        skirt_area = max_thrust / allowable_bearing_pressure
        piston_skirt_length = skirt_area / cylinder_bore

        return render_template('piston_design.html', results={
            'piston_diameter': f'{piston_diameter:.2f} mm',
            'piston_clearance': f'{piston_clearance:.4f} mm',
            'compression_height': f'{compression_height:.2f} mm',
            'crown_thickness': f'{crown_thickness:.2f} mm',
            'max_piston_force': f'{max_piston_force:.2f} N',
            'gudgeon_pin_outer_diameter': f'{gudgeon_pin_outer_diameter:.2f} mm',
            'gudgeon_pin_inner_diameter': gudgeon_pin_inner_diameter,
            'piston_skirt_length': f'{piston_skirt_length:.2f} mm'
        })

    return render_template('piston_design.html', results=None)

@app.route('/connectingrod', methods=['GET', 'POST'])
def connectingrod():
    if request.method == 'POST':
        # Get inputs from the form
        piston_diameter = float(request.form['piston_diameter'])
        max_combustion_pressure = float(request.form['max_combustion_pressure'])
        reciprocating_mass = float(request.form['reciprocating_mass'])
        crank_radius = float(request.form['crank_radius'])
        piston_pin_diameter = float(request.form['piston_pin_diameter'])
        crankpin_diameter = float(request.form['crankpin_diameter'])
        max_engine_rpm = float(request.form['max_engine_rpm'])
        rod_material_yield_strength = float(request.form['rod_material_yield_strength'])
        bolt_material_yield_strength = float(request.form['bolt_material_yield_strength'])
        safety_factor = float(request.form['safety_factor'])

        # --- Calculation Logic ---
        # Shank Design (based on buckling load, dimensions for Big End)
        max_gas_force = max_combustion_pressure * (np.pi * piston_diameter**2 / 4)
        allowable_compressive_stress = rod_material_yield_strength / safety_factor
        shank_area = max_gas_force / allowable_compressive_stress
        # Assuming I-section with proportions A = 11t^2, we find 't'
        t = np.sqrt(shank_area / 11)
        web_and_flange_thickness = t

        # Dimensions at the Big End of the shank
        big_end_shank_height = 5 * t
        big_end_flange_width = 4 * t

        # Dimensions at the Small End of the shank (tapered)
        taper_ratio = 0.8 # Common design ratio
        small_end_shank_height = big_end_shank_height * taper_ratio
        small_end_flange_width = big_end_flange_width * taper_ratio

        # Bolt Design (based on inertia)
        angular_velocity = max_engine_rpm * 2 * np.pi / 60
        max_inertial_force = reciprocating_mass * (crank_radius / 1000) * angular_velocity**2
        force_per_bolt = max_inertial_force / 2
        allowable_bolt_stress = bolt_material_yield_strength / safety_factor
        required_bolt_core_area = force_per_bolt / allowable_bolt_stress
        bolt_core_diameter = np.sqrt(4 * required_bolt_core_area / np.pi)
        bolt_diameter = bolt_core_diameter / 0.85 # Approximation for nominal diameter

        # Rod End Dimensions (empirical)
        small_end_wall_thickness = piston_pin_diameter * 0.35
        small_end_outer_diameter = piston_pin_diameter + (2 * small_end_wall_thickness)
        big_end_wall_thickness = crankpin_diameter * 0.35
        big_end_outer_diameter = crankpin_diameter + (2 * big_end_wall_thickness)

        return render_template('connecting_rod_design.html', results={
            'big_end_shank_height': f'{big_end_shank_height:.2f} mm',
            'big_end_flange_width': f'{big_end_flange_width:.2f} mm',
            'small_end_shank_height': f'{small_end_shank_height:.2f} mm',
            'small_end_flange_width': f'{small_end_flange_width:.2f} mm',
            'web_and_flange_thickness': f'{web_and_flange_thickness:.2f} mm',
            'bolt_diameter': f'{bolt_diameter:.2f} mm',
            'small_end_outer_diameter': f'{small_end_outer_diameter:.2f} mm',
            'small_end_wall_thickness': f'{small_end_wall_thickness:.2f} mm',
            'big_end_outer_diameter': f'{big_end_outer_diameter:.2f} mm',
            'big_end_wall_thickness': f'{big_end_wall_thickness:.2f} mm'
        })

    return render_template('connecting_rod_design.html', results=None)

@app.route('/crankshaft', methods=['GET', 'POST'])
def crankshaft():
    if request.method == 'POST':
        # Get inputs from the form
        piston_diameter = float(request.form['piston_diameter'])
        max_combustion_pressure = float(request.form['max_combustion_pressure'])
        cylinder_bore_spacing = float(request.form['cylinder_bore_spacing'])
        crankshaft_material_yield_strength = float(request.form['crankshaft_material_yield_strength'])
        allowable_bearing_pressure = float(request.form['allowable_bearing_pressure'])
        safety_factor = float(request.form['safety_factor'])

        # --- Calculation Logic ---
        # Max Gas Force
        max_gas_force = max_combustion_pressure * (np.pi * piston_diameter**2 / 4)

        # Allowable Stress
        allowable_bending_stress = crankshaft_material_yield_strength / safety_factor

        # Crankpin Design
        # Simplified bending moment calculation
        bending_moment = max_gas_force * (cylinder_bore_spacing / 1000) / 2 # In Nm
        # Diameter based on bending stress
        crankpin_diameter_m = ( (32 * bending_moment) / (np.pi * (allowable_bending_stress * 1e6)) )**(1/3)
        crankpin_diameter = crankpin_diameter_m * 1000 # In mm
        # Length based on bearing pressure
        projected_area_crankpin = max_gas_force / (allowable_bearing_pressure * 1e6)
        crankpin_length_m = projected_area_crankpin / crankpin_diameter_m
        crankpin_length = crankpin_length_m * 1000 # In mm

        # Main Journal Design (Empirical)
        main_journal_diameter = 1.15 * crankpin_diameter
        projected_area_main = max_gas_force / (allowable_bearing_pressure * 1e6) # Simplified load
        main_journal_length_m = projected_area_main / (main_journal_diameter / 1000)
        main_journal_length = main_journal_length_m * 1000 # In mm

        # Crank Web Design (Empirical)
        crank_web_thickness = 0.5 * crankpin_diameter
        crank_web_width = 1.25 * crankpin_diameter

        return render_template('crankshaft_design.html', results={
            'crankpin_diameter': f'{crankpin_diameter:.2f} mm',
            'crankpin_length': f'{crankpin_length:.2f} mm',
            'main_journal_diameter': f'{main_journal_diameter:.2f} mm',
            'main_journal_length': f'{main_journal_length:.2f} mm',
            'crank_web_thickness': f'{crank_web_thickness:.2f} mm',
            'crank_web_width': f'{crank_web_width:.2f} mm'
        })

    return render_template('crankshaft_design.html', results=None)

@app.route('/clutch', methods=['GET', 'POST'])
def clutch():
    if request.method == 'POST':
        # Get inputs from the form
        max_engine_torque = float(request.form['max_engine_torque'])
        outer_diameter = float(request.form['outer_diameter'])
        friction_coefficient = float(request.form['friction_coefficient'])
        allowable_surface_pressure = float(request.form['allowable_surface_pressure'])
        safety_factor = float(request.form['safety_factor'])

        # --- Calculation Logic ---
        # Required torque capacity
        torque_capacity = max_engine_torque * safety_factor

        # Assume inner diameter is a ratio of outer diameter (common practice)
        d_o = outer_diameter / 1000 # meters
        d_i = 0.6 * d_o # meters
        inner_diameter_mm = d_i * 1000

        # Mean radius based on Uniform Wear Theory
        mean_radius_m = (d_o + d_i) / 4
        mean_radius_mm = mean_radius_m * 1000

        # Number of friction surfaces (single plate clutch)
        n = 2

        # Required clamping force from springs
        required_clamping_force = torque_capacity / (n * friction_coefficient * mean_radius_m)

        # Actual surface pressure on the friction lining
        face_area = (np.pi / 4) * (d_o**2 - d_i**2)
        actual_surface_pressure = required_clamping_force / face_area # Pa
        actual_surface_pressure_mpa = actual_surface_pressure / 1e6

        # Check if the design is viable
        if actual_surface_pressure_mpa <= allowable_surface_pressure:
            viability_note = "Design is viable. Surface pressure is within allowable limits."
            viability_class = "viable"
        else:
            viability_note = "Design NOT viable. Surface pressure exceeds limits. Increase outer diameter or check parameters."
            viability_class = "not-viable"

        return render_template('clutch_design.html', results={
            'clutch_type': 'Single Plate Dry Clutch',
            'torque_capacity': f'{torque_capacity:.2f} Nm',
            'inner_diameter': f'{inner_diameter_mm:.2f} mm',
            'mean_radius': f'{mean_radius_mm:.2f} mm',
            'required_clamping_force': f'{required_clamping_force:.2f} N',
            'actual_surface_pressure': f'{actual_surface_pressure_mpa:.3f} MPa',
            'viability_note': viability_note,
            'viability_class': viability_class
        })

    return render_template('clutch_design.html', results=None)

@app.route('/gearbox', methods=['GET', 'POST'])
def gearbox():
    if request.method == 'POST':
        # Get inputs from the form
        max_engine_torque = float(request.form['max_engine_torque'])
        primary_drive_ratio = float(request.form['primary_drive_ratio'])
        first_gear_ratio = float(request.form['first_gear_ratio'])
        top_gear_ratio = float(request.form['top_gear_ratio'])
        number_of_gears = int(request.form['number_of_gears'])
        gear_material_strength = float(request.form['gear_material_strength'])
        safety_factor = float(request.form['safety_factor'])
        module = float(request.form['module'])
        pinion_teeth_1st_gear = int(request.form['pinion_teeth_1st_gear'])

        # --- Calculation Logic ---
        # 1. Gear Ratio Calculation (Geometric Progression)
        progression_factor = (first_gear_ratio / top_gear_ratio)**(1 / (number_of_gears - 1))
        all_gear_ratios = [first_gear_ratio / (progression_factor**(n)) for n in range(number_of_gears)]

        # 2. 1st Gear Pair Design (Lewis Bending Equation)
        # Torque at gearbox input shaft
        torque_input_shaft = max_engine_torque * primary_drive_ratio
        
        # Pinion and Gear teeth for 1st gear
        z1 = pinion_teeth_1st_gear
        z2 = round(z1 * first_gear_ratio)

        # Pitch diameters
        d1 = module * z1
        d2 = module * z2

        # Tangential force on pinion
        tangential_force = torque_input_shaft / (d1 / 2 / 1000) # Convert d1 to meters for radius

        # Lewis Form Factor (approximated for 20 deg pressure angle)
        lewis_form_factor = 0.484 - (2.87 / z1)

        # Allowable stress
        allowable_stress = gear_material_strength / safety_factor

        # Required face width
        face_width_m = tangential_force / ((allowable_stress * 1e6) * np.pi * (module / 1000) * lewis_form_factor)
        face_width_mm = face_width_m * 1000

        # Center distance
        center_distance = (d1 + d2) / 2

        return render_template('gearbox_design.html', results={
            'all_gear_ratios': [f'{r:.3f}:1' for r in all_gear_ratios],
            'pinion_teeth': z1,
            'gear_teeth': z2,
            'face_width': f'{face_width_mm:.2f} mm',
            'pinion_pitch_diameter': f'{d1:.2f} mm',
            'gear_pitch_diameter': f'{d2:.2f} mm',
            'center_distance': f'{center_distance:.2f} mm'
        })

    return render_template('gearbox_design.html', results=None)

@app.route('/chainsprocket', methods=['GET', 'POST'])
def chainsprocket():
    if request.method == 'POST':
        # Data for standard motorcycle chains
        chain_data = {
            '520': {'pitch': 15.875, 'strength_N': 35000},
            '525': {'pitch': 15.875, 'strength_N': 40000},
            '530': {'pitch': 15.875, 'strength_N': 45000}
        }

        # Get inputs from the form
        max_engine_power = float(request.form['max_engine_power'])
        small_sprocket_rpm = float(request.form['small_sprocket_rpm'])
        chain_type = request.form['chain_type']
        small_sprocket_teeth = int(request.form['small_sprocket_teeth'])
        large_sprocket_teeth = int(request.form['large_sprocket_teeth'])
        center_distance_mm = float(request.form['center_distance_mm'])

        # --- Calculation Logic ---
        P = chain_data[chain_type]['pitch']
        T1 = small_sprocket_teeth
        T2 = large_sprocket_teeth
        C = center_distance_mm

        # Final Drive Ratio
        final_drive_ratio = T2 / T1

        # Chain Length
        L_p = 2*(C/P) + (T1+T2)/2 + ((T2-T1)/(2*np.pi))**2 * (P/C)
        chain_length_links = int(np.ceil(L_p / 2.) * 2) # Round up to nearest even number
        chain_length_mm = chain_length_links * P

        # Sprocket Dimensions
        small_sprocket_pcd = P / np.sin(np.deg2rad(180 / T1))
        small_sprocket_od = P * (0.6 + (1 / np.tan(np.deg2rad(180 / T1))))
        large_sprocket_pcd = P / np.sin(np.deg2rad(180 / T2))
        large_sprocket_od = P * (0.6 + (1 / np.tan(np.deg2rad(180 / T2))))

        # Safety Analysis
        service_factor = 1.2
        design_power_kw = max_engine_power * service_factor
        chain_velocity_ms = (small_sprocket_rpm * T1 * P) / (60 * 1000)
        working_load_N = (design_power_kw * 1000) / chain_velocity_ms if chain_velocity_ms > 0 else 0
        breaking_strength_N = chain_data[chain_type]['strength_N']
        factor_of_safety = breaking_strength_N / working_load_N if working_load_N > 0 else float('inf')

        # Check viability
        if factor_of_safety > 10:
            viability_note = "Chain selection is safe for the given load."
            viability_class = "viable"
        else:
            viability_note = "Warning: Factor of safety is low. Consider a stronger chain or different parameters."
            viability_class = "not-viable"

        return render_template('chain_sprocket_design.html', results={
            'final_drive_ratio': f'{final_drive_ratio:.2f}:1',
            'chain_pitch_mm': f'{P:.3f} mm',
            'chain_length_links': chain_length_links,
            'chain_length_mm': f'{chain_length_mm:.2f}',
            'small_sprocket_pcd': f'{small_sprocket_pcd:.2f} mm',
            'small_sprocket_od': f'{small_sprocket_od:.2f} mm',
            'large_sprocket_pcd': f'{large_sprocket_pcd:.2f} mm',
            'large_sprocket_od': f'{large_sprocket_od:.2f} mm',
            'factor_of_safety': f'{factor_of_safety:.2f}',
            'viability_note': viability_note,
            'viability_class': viability_class
        })

    return render_template('chain_sprocket_design.html', results=None)

@app.route('/rim', methods=['GET', 'POST'])
def rim():
    if request.method == 'POST':
        # Get inputs from the form
        tyre_width_mm = int(request.form['tyre_width_mm'])
        tyre_aspect_ratio = int(request.form['tyre_aspect_ratio'])
        rim_diameter_inches = float(request.form['rim_diameter_inches'])
        proposed_rim_width_inches = float(request.form['proposed_rim_width_inches'])

        # --- ETRTO Standard Data (Simplified Table) ---
        # This table maps tyre width to a design rim width and a min/max permitted range
        rim_data = {}
        if 90 <= tyre_width_mm <= 100:
            rim_data = {'design': 2.50, 'min': 2.15, 'max': 2.75}
        elif 110 <= tyre_width_mm <= 120:
            rim_data = {'design': 3.50, 'min': 3.00, 'max': 3.75}
        elif 130 <= tyre_width_mm <= 140:
            rim_data = {'design': 4.00, 'min': 3.50, 'max': 4.50}
        elif 150 <= tyre_width_mm <= 160:
            rim_data = {'design': 4.50, 'min': 4.25, 'max': 5.00}
        elif 170 <= tyre_width_mm <= 180:
            rim_data = {'design': 5.50, 'min': 5.00, 'max': 6.00}
        elif 190 <= tyre_width_mm <= 200:
            rim_data = {'design': 6.00, 'min': 5.50, 'max': 6.50}
        else:
            rim_data = None

        # --- Calculation & Compatibility Check ---
        if rim_data:
            recommended_range = f'{rim_data["min"]:.2f}" to {rim_data["max"]:.2f}" (Ideal: {rim_data["design"]:.2f}")'
            if rim_data['min'] <= proposed_rim_width_inches <= rim_data['max']:
                if proposed_rim_width_inches == rim_data['design']:
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

        # Standard Dimensions
        bead_seat_diameter_mm = rim_diameter_inches * 25.4
        flange_height_mm = 17.5 # For a standard 'J' contour motorcycle rim

        return render_template('rim_compatibility.html', results={
            'tyre_designation': f'{tyre_width_mm}/{tyre_aspect_ratio}-{int(rim_diameter_inches)}',
            'recommended_rim_width_range': recommended_range,
            'compatibility_note': compatibility_note,
            'compatibility_class': compatibility_class,
            'bead_seat_diameter_mm': f'{bead_seat_diameter_mm:.2f} mm',
            'flange_height_mm': f'{flange_height_mm:.1f} mm'
        })

    return render_template('rim_compatibility.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)