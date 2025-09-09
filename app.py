from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disc-brake', methods=['GET', 'POST'])
def disc_brake():
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

if __name__ == '__main__':
    app.run(debug=True)
