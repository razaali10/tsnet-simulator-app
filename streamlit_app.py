
import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TSNET Transient Simulator", layout="wide")
st.title("💧 TSNET Transient Simulator")

# Upload INP file
st.sidebar.header("Upload EPANET .inp File")
inp_file = st.sidebar.file_uploader("Choose .inp file", type=["inp"])

# Select event type
event_type = st.sidebar.selectbox("Select Transient Event", [
    "valve_closure", "pump_shutdown", "surge_tank", "air_chamber", "pressure_relief_valve"
])

# Input parameters
params = {"event_type": event_type}
if event_type == "valve_closure":
    params.update({
        "pipe_id": st.sidebar.text_input("Pipe ID"),
        "start_time": st.sidebar.number_input("Start Time (s)", value=10.0),
        "closure_time": st.sidebar.number_input("Closure Time (s)", value=2.0)
    })
elif event_type == "pump_shutdown":
    params.update({
        "pump_id": st.sidebar.text_input("Pump ID"),
        "start_time": st.sidebar.number_input("Shutdown Time (s)", value=10.0)
    })
elif event_type == "surge_tank":
    params.update({
        "node_id": st.sidebar.text_input("Node ID"),
        "diameter": st.sidebar.number_input("Diameter (m)", value=1.0),
        "elevation": st.sidebar.number_input("Elevation (m)", value=100.0)
    })
elif event_type == "air_chamber":
    params.update({
        "node_id": st.sidebar.text_input("Node ID"),
        "diameter": st.sidebar.number_input("Diameter (m)", value=1.0),
        "volume": st.sidebar.number_input("Volume (m³)", value=2.0),
        "n_index": st.sidebar.number_input("Polytropic Index", value=1.2)
    })
elif event_type == "pressure_relief_valve":
    params.update({
        "node_id": st.sidebar.text_input("Node ID"),
        "setting_pressure": st.sidebar.number_input("Relief Pressure (m)", value=50.0),
        "discharge_coeff": st.sidebar.number_input("Discharge Coefficient", value=0.6)
    })

# Common simulation controls
params.update({
    "tf": st.sidebar.number_input("Simulation Duration (s)", value=60.0),
    "dt": st.sidebar.number_input("Time Step (s)", value=0.01),
    "monitor_nodes": st.sidebar.text_input("Monitor Nodes (comma-separated)").split(","),
    "monitor_pipes": st.sidebar.text_input("Monitor Pipes (comma-separated)").split(",")
})

if st.sidebar.button("Run Simulation") and inp_file:
    with st.spinner("Running TSNET simulation..."):
        files = {"inp_file": inp_file}
        data = {"transient_params": json.dumps(params)}
        response = requests.post("http://localhost:5000/run-simulation", files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        time = result["time"]
        st.success("✅ Simulation completed!")

        # Plot pressures
        if result["node_pressures"]:
            st.subheader("Node Pressures")
            df_nodes = pd.DataFrame(result["node_pressures"], index=time)
            for col in df_nodes.columns:
                fig = px.line(df_nodes, y=col, title=f"Pressure at Node {col}", labels={"index": "Time (s)", col: "Pressure (m)"})
                st.plotly_chart(fig, use_container_width=True)

        # Plot velocities
        if result["pipe_velocities"]:
            st.subheader("Pipe Velocities")
            df_pipes = pd.DataFrame(result["pipe_velocities"], index=time)
            for col in df_pipes.columns:
                fig = px.line(df_pipes, y=col, title=f"Velocity in Pipe {col}", labels={"index": "Time (s)", col: "Velocity (m/s)"})
                st.plotly_chart(fig, use_container_width=True)

        # Download CSVs
        st.sidebar.download_button("Download Node Pressures CSV", df_nodes.to_csv().encode(), "node_pressures.csv", "text/csv")
        st.sidebar.download_button("Download Pipe Velocities CSV", df_pipes.to_csv().encode(), "pipe_velocities.csv", "text/csv")
    else:
        st.error(f"❌ Error: {response.json().get('error')}")
