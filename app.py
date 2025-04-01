from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import json
import pandas as pd
from tsnet.networkModel import NetworkModel

app = Flask(__name__)
CORS(app)

def run_tsnet_simulation(inp_file_path, transient_params):
    wn = NetworkModel(inp_file_path)

    if transient_params["event_type"] == "valve_closure":
        pipe_id = transient_params["pipe_id"]
        start_time = transient_params["start_time"]
        closure_time = transient_params["closure_time"]
        wn.add_valve(pipe_id=pipe_id, valve_type='TCV', start_time=start_time, closure_time=closure_time)

    elif transient_params["event_type"] == "pump_shutdown":
        pump_id = transient_params["pump_id"]
        start_time = transient_params["start_time"]
        wn.add_pump_shutdown(pump_id=pump_id, start_time=start_time)

    dt = transient_params.get("dt", 0.01)
    tf = transient_params.get("tf", 60.0)

    wn.simulate_transient(Tmax=tf, dt=dt)

    node_results = {}
    for node in transient_params["monitor_nodes"]:
        node_results[node] = wn.get_node_pressure(node)

    pipe_results = {}
    for pipe in transient_params["monitor_pipes"]:
        pipe_results[pipe] = wn.get_link_velocity(pipe)

    time_series = wn.time
    df_nodes = pd.DataFrame({node: data for node, data in node_results.items()}, index=time_series)
    df_pipes = pd.DataFrame({pipe: data for pipe, data in pipe_results.items()}, index=time_series)

    return {
        "node_pressures": df_nodes.to_dict(orient='list'),
        "pipe_velocities": df_pipes.to_dict(orient='list'),
        "time": list(time_series)
    }

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    if 'inp_file' not in request.files or 'transient_params' not in request.form:
        return jsonify({'error': 'Missing input file or parameters'}), 400

    inp_file = request.files['inp_file']
    transient_params = json.loads(request.form['transient_params'])

    with tempfile.NamedTemporaryFile(delete=False, suffix='.inp') as temp_file:
        inp_file.save(temp_file.name)
        inp_path = temp_file.name

    try:
        result = run_tsnet_simulation(inp_path, transient_params)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(inp_path)

if __name__ == '__main__':
    app.run(debug=True)
