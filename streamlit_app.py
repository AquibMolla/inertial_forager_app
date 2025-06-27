# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit.components.v1 as components
import matplotlib
matplotlib.use("Agg")

from simulate import simulate_forager

# Streamlit page settings
st.set_page_config(page_title="Inertial Forager Simulation")

# Custom CSS
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# App header
st.markdown("""
    <h2 style='text-align: center;'>Welcome to the Inertial Forager Simulation!</h2>
    <p style='text-align: center;'>
        This simulation models a forager searching for food in a grid world.
        Adjust parameters and click <strong>Run Simulation</strong> to begin!
    </p>
""", unsafe_allow_html=True)

# Optional image
try:
    st.image("app.jpeg", caption="Illustration of the Forager Model", use_container_width=True)
except:
    pass  # Optional

# Sidebar controls
with st.sidebar:
    st.header("Simulation Parameters")
    max_energy = st.slider("Full energy (1–20):", 1, 20, 10)
    laziness = st.slider("Laziness (0–1):", 0.0, 1.0, 0.5)

# Simulation + Animation
if st.button("Run Simulation"):
    width = height = 4 * max_energy
    with st.spinner("Running simulation..."):
        path, energy_history, space = simulate_forager(width, height, max_energy, laziness)
        lifetime = len(path)
        eaten = ((width + 1) * (height + 1)) - np.sum(space)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
        frames = len(path)

        def init():
            ax1.clear()
            ax2.clear()
            ax1.set_xlim(0, width)
            ax1.set_ylim(0, height)
            ax2.set_xlim(0, frames)
            ax2.set_ylim(0, max_energy + 2)
            ax1.set_title("Forager Path")
            ax2.set_title("Energy Level")
            ax1.grid(True, linestyle="--", alpha=0.3)
            ax2.grid(True, linestyle="--", alpha=0.3)

        def update(frame):
            ax1.clear()
            ax2.clear()
            ax1.set_xlim(0, width)
            ax1.set_ylim(0, height)
            ax2.set_xlim(0, frames)
            ax2.set_ylim(0, max_energy + 2)
            ax1.set_title("Forager Path")
            ax2.set_title("Energy Level")
            ax1.grid(True, linestyle="--", alpha=0.3)
            ax2.grid(True, linestyle="--", alpha=0.3)

            ax1.plot(path[:frame, 1], path[:frame, 0], "b-", alpha=0.6)
            ax1.plot(path[frame, 1], path[frame, 0], "ro", markersize=8)
            ax2.plot(energy_history[:frame], "r-")

        anim = FuncAnimation(fig, update, frames=frames, init_func=init, interval=60, blit=False)
        html = anim.to_jshtml()
        plt.close(fig)

        components.html(html, height=520)

        # Summary
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 10px; background-color: #f0f2f6; text-align: center;">
                    <h3>Lifetime</h3>
                    <p style="font-size: 24px; font-weight: bold;">{lifetime} steps</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 10px; background-color: #f0f2f6; text-align: center;">
                    <h3>Cabbages Eaten</h3>
                    <p style="font-size: 24px; font-weight: bold;">{eaten}</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #666;">
        <p>Developed by Md Aquib Molla | <a href="https://github.com/AquibMolla" target="_blank">GitHub</a></p>
    </div>
""", unsafe_allow_html=True)
