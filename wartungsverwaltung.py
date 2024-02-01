import streamlit as st
from datetime import datetime, timedelta
from devices import Device
from users import User

class Wartungsverwaltung:
    def __init__(self):
        self.load_devices()

    def load_devices(self):
        self.devices = Device.load_all_devices()

    def show_next_maintenance_dates(self):
        st.write("## Nächste Wartungstermine")

        for device in self.devices:
            next_maintenance_date = device.calculate_next_maintenance_date()
            st.write(f"{device.device_name}: {next_maintenance_date}")

    def show_maintenance_costs_per_quarter(self):
        st.write("## Wartungskosten pro Quartal")

        for device in self.devices:
            st.write(f"**{device.device_name}**: {self.calculate_maintenance_costs_per_quarter(device)}")

    def calculate_maintenance_costs_per_quarter(self, device):
        # Verwende die Methode aus dem Geräteobjekt
        return f"${device.calculate_maintenance_costs_per_quarter():.2f}"