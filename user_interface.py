### Erste Streamlit App

import streamlit as st
from queries import find_devices
from devices import Device
from users import User
from validate_email_address import validate_email

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

# Navigation
selected_option = st.sidebar.selectbox("Menü", ["Geräteverwaltung", "Nutzerverwaltung"])

if selected_option == "Geräteverwaltung":
    # Geräteverwaltung
    st.write("## Geräteverwaltung")

    # Gerät erstellen oder ändern
    device_action = st.sidebar.radio("Gerät anlegen/ändern", ["Neues Gerät", "Gerät ändern"])

    if device_action == "Neues Gerät":
        # Wenn ein neues Gerät erstellt wird
        with st.form("New Device"):

            device_name = st.text_input("Gerätename")
            managed_by_user_id = st.text_input("Geräte-Verantwortlicher (Nutzer-ID)")
        
            # Platzieren Sie den Submit-Button unter dem Eingabefeld
            submitted_new_device = st.form_submit_button("Neues Gerät hinzufügen")

            if submitted_new_device and not Device.device_exists(device_name):
                if User.user_exists(managed_by_user_id):
                    new_device = Device(device_name, managed_by_user_id)
                    new_device.store_data()
                    st.write("Neues Gerät hinzugefügt.")
                else:
                    st.warning("Dieser Benutzer ist nicht angelegt.")
            elif Device.device_exists(device_name):
                st.warning("Gerät mit diesem Namen existiert bereits.")

    elif device_action == "Gerät ändern":
        # Bestehendes Gerät ändern
        devices_in_db = find_devices()

        if devices_in_db:
            current_device_name = st.selectbox(
                'Gerät auswählen',
                options=devices_in_db, key="sbDevice")

            if current_device_name in devices_in_db:
                loaded_device = Device.load_data_by_device_name(current_device_name)
                st.write(f"Loaded Device: {loaded_device}")

            with st.form("Device"):
                st.write(loaded_device.device_name)

                checkbox_val = st.checkbox("Is active?", value=loaded_device.is_active)
                loaded_device.is_active = checkbox_val

                text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                loaded_device.managed_by_user_id = text_input_val

                # Submit button
                submitted = st.form_submit_button("Submit")

                if User.user_exists(loaded_device.managed_by_user_id):
                    
                    if submitted:
                        loaded_device.store_data()
                        st.write("Data stored.")
                        st.rerun()

elif selected_option == "Nutzerverwaltung":
    st.write("## Nutzerverwaltung")

    with st.form("User"):
        user_name = st.text_input("Nutzername")
        email = st.text_input("E-Mail-Adresse")

        submitted_user = st.form_submit_button("Nutzer anlegen")

        if submitted_user:
            # Methode in der User-Klasse aufrufen
            result_message = User.validate_and_create_user(user_name, email)
            st.write(result_message)