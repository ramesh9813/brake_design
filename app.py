from flask import Flask, render_template, request
import dataclasses

# Import all calculation modules and their data classes
from calculations.disc import DiscInput, calculate_disc
from calculations.caliper import CaliperInput, calculate_caliper
from calculations.brakepad import BrakePadInput, calculate_brakepad
from calculations.tyre import TyreInput, calculate_tyre
from calculations.piston import PistonInput, calculate_piston
from calculations.connecting_rod import ConnectingRodInput, calculate_connecting_rod
from calculations.crankshaft import CrankshaftInput, calculate_crankshaft
from calculations.clutch import ClutchInput, calculate_clutch
from calculations.gearbox import GearboxInput, calculate_gearbox
from calculations.chain_sprocket import ChainSprocketInput, calculate_chain_sprocket
from calculations.rim import RimInput, calculate_rim_compatibility
from calculations.cylinder import CylinderInput, calculate_cylinder
from calculations.wrist_pin import WristPinInput, calculate_wrist_pin

app = Flask(__name__)

# --- Helper Function to handle form data and errors ---
def process_request(form_data, input_dataclass, calculation_function, template_name):
    if request.method == 'POST':
        try:
            # Create an instance of the input dataclass from the form data
            inputs = input_dataclass(**{field.name: field.type(form_data.get(field.name)) for field in dataclasses.fields(input_dataclass)})
            results = calculation_function(inputs)
            return render_template(template_name, results=dataclasses.asdict(results))
        except (ValueError, TypeError, KeyError) as e:
            return render_template(template_name, error=f"Invalid or missing input: {e}")
    return render_template(template_name, results=None)

# --- Main Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# --- Design Tool Routes ---
@app.route('/disc', methods=['GET', 'POST'])
def disc():
    return process_request(request.form, DiscInput, calculate_disc, 'disc.html')

@app.route('/caliper', methods=['GET', 'POST'])
def caliper():
    return process_request(request.form, CaliperInput, calculate_caliper, 'caliper.html')

@app.route('/brakepad', methods=['GET', 'POST'])
def brakepad():
    return process_request(request.form, BrakePadInput, calculate_brakepad, 'brakepad.html')

@app.route('/tyre', methods=['GET', 'POST'])
def tyre():
    return process_request(request.form, TyreInput, calculate_tyre, 'tyre.html')

@app.route('/piston', methods=['GET', 'POST'])
def piston():
    return process_request(request.form, PistonInput, calculate_piston, 'piston.html')

@app.route('/connectingrod', methods=['GET', 'POST'])
def connectingrod():
    return process_request(request.form, ConnectingRodInput, calculate_connecting_rod, 'connectingrod.html')

@app.route('/crankshaft', methods=['GET', 'POST'])
def crankshaft():
    return process_request(request.form, CrankshaftInput, calculate_crankshaft, 'crankshaft.html')

@app.route('/clutch', methods=['GET', 'POST'])
def clutch():
    return process_request(request.form, ClutchInput, calculate_clutch, 'clutch.html')

@app.route('/gearbox', methods=['GET', 'POST'])
def gearbox():
    return process_request(request.form, GearboxInput, calculate_gearbox, 'gearbox.html')

@app.route('/chainsprocket', methods=['GET', 'POST'])
def chainsprocket():
    return process_request(request.form, ChainSprocketInput, calculate_chain_sprocket, 'chainsprocket.html')

@app.route('/rim', methods=['GET', 'POST'])
def rim():
    return process_request(request.form, RimInput, calculate_rim_compatibility, 'rim.html')

@app.route('/cylinder', methods=['GET', 'POST'])
def cylinder():
    return process_request(request.form, CylinderInput, calculate_cylinder, 'cylinder.html')

@app.route('/wristpin', methods=['GET', 'POST'])
def wristpin():
    return process_request(request.form, WristPinInput, calculate_wrist_pin, 'wristpin.html')

if __name__ == '__main__':
    app.run(debug=True)