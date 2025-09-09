from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disc-design', methods=['GET', 'POST'])
def disc_design():
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
        effective_radius_m = (outer_diameter_m + inner_diameter_m) / 4 # Approximation

        # Performance calculations
        min_service_thickness_m = thickness_m * 0.8 # 20% wear
        disc_mass = np.pi * (outer_diameter_m**2 - inner_diameter_m**2) * thickness_m * material_density
        heat_energy = 0.5 * total_mass * initial_velocity_ms**2
        temp_rise = heat_energy / (disc_mass * material_specific_heat) if disc_mass > 0 else 0

        # Stress and safety factor
        clamping_force = hydraulic_pressure_pa * caliper_piston_area_m2
        frictional_force = 2 * clamping_force * friction_coefficient # For one disc with two pads
        # Simplified stress calculation
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
            'safety_factor': f'{safety_factor:.2f}'
        })
    return render_template('disc_brake.html', results=None)

@app.route('/caliper-design', methods=['GET', 'POST'])
def caliper_design():
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
        
        # Simplified stress calculation (placeholder)
        caliper_stress = (total_clamp_force * 0.1) / (pad_contact_area_m2 * 0.1) if pad_contact_area_m2 > 0 else 0
        safety_factor = caliper_material_yield_strength_pa / caliper_stress if caliper_stress > 0 else float('inf')

        return render_template('caliper_design.html', results={
            'total_clamp_force': f'{total_clamp_force:.2f} N',
            'clamp_force_per_piston': f'{clamp_force_per_piston:.2f} N',
            'piston_diameter': f'{piston_diameter_mm:.2f} mm',
            'brake_torque_delivered': f'{brake_torque_delivered:.2f} Nm',
            'caliper_stress': f'{caliper_stress / 1e6:.2f} MPa',
            'safety_factor': f'{safety_factor:.2f}'
        })
    return render_template('caliper_design.html', results=None)

@app.route('/brake-pad-design', methods=['GET', 'POST'])
def brake_pad_design():
    if request.method == 'POST':
        # Get inputs from the form
        disc_effective_radius = float(request.form['disc_effective_radius'])
        required_braking_torque = float(request.form['required_braking_torque'])
        friction_coefficient = float(request.form['friction_coefficient'])
        pad_wear_rate = float(request.form['pad_wear_rate'])
        pad_thickness_mm = float(request.form['pad_thickness'])
        pad_area_cm2 = float(request.form['pad_area'])
        pad_thermal_conductivity = float(request.form['pad_thermal_conductivity'])

        # --- Unit Conversions ---
        pad_area_m2 = pad_area_cm2 / 10000
        pad_thickness_m = pad_thickness_mm / 1000

        # --- Calculation Logic ---
        pad_material = f"Friction Coefficient: {friction_coefficient}"
        pad_area_thickness = f"{pad_area_cm2} cm², {pad_thickness_mm} mm"
        # Simplified thermal capacity calculation
        thermal_capacity = pad_area_m2 * pad_thickness_m * pad_thermal_conductivity * 1000
        wear_life = (pad_thickness_mm / pad_wear_rate) * 1000 if pad_wear_rate > 0 else float('inf')

        return render_template('brake_pad_design.html', results={
            'pad_material': pad_material,
            'pad_area_thickness': pad_area_thickness,
            'thermal_capacity': f'{thermal_capacity:.2f} W/K',
            'wear_life': f'{wear_life:.2f} km'
        })
    return render_template('brake_pad_design.html', results=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
