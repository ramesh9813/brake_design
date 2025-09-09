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
        stopping_distance = float(request.form['stopping_distance'])
        wheel_radius = float(request.form['wheel_radius'])
        # Assumed initial velocity (60 km/h)
        initial_velocity = 16.67 # m/s
        deceleration = (initial_velocity**2) / (2 * stopping_distance)
        # Material properties (placeholders for now)
        density = 7850  # kg/m^3
        yield_strength = 350e6  # Pa
        modulus = 200e9  # Pa
        specific_heat = 450  # J/kg*K

        # --- Basic Calculation Logic (Placeholder) ---
        # This is a simplified calculation. A real-world scenario would be more complex.
        total_mass = mass_vehicle + mass_rider
        braking_force = total_mass * deceleration
        
        # Assuming a simple relationship for brake disc dimensions
        outer_diameter = np.sqrt(braking_force / 1000) * 0.1 
        inner_diameter = outer_diameter * 0.6
        thickness = outer_diameter * 0.05
        
        # Simplified stress calculation
        max_stress = (braking_force * 0.1) / (np.pi * (outer_diameter**2 - inner_diameter**2) * thickness)
        
        # Braking torque
        braking_torque = braking_force * wheel_radius


        return render_template('disc_brake.html', results={
            'outer_diameter': f'{outer_diameter * 1000:.2f} mm',
            'inner_diameter': f'{inner_diameter * 1000:.2f} mm',
            'thickness': f'{thickness * 1000:.2f} mm',
            'max_stress': f'{max_stress / 1e6:.2f} MPa',
            'braking_force': f'{braking_force:.2f} N',
            'braking_torque': f'{braking_torque:.2f} Nm'
        })
    return render_template('disc_brake.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)
