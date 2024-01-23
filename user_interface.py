### Erste Streamlit App

import streamlit as st
from queries import find_devices
from devices import Device
from users import User

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

# Navigation
selected_option = st.sidebar.selectbox("Menü", ["Geräteverwaltung", "Nutzerverwaltung"])

if selected_option == "Geräteverwaltung":
    # Geräteverwaltung
    st.write("## Geräteverwaltung")

    # Sub-navigation for Create/Modify Device
    device_action = st.sidebar.radio("Gerät anlegen/ändern", ["Neues Gerät", "Gerät ändern"])

    if device_action == "Neues Gerät":
        # If creating a new device
        with st.form("New Device"):
            st.write("Neues Gerät hinzufügen")

            device_name = st.text_input("Gerätename")
            managed_by_user_id = st.text_input("Geräte-Verantwortlicher (Nutzer-ID)")

            # Every form must have a submit button.
            submitted_new_device = st.form_submit_button("Neues Gerät hinzufügen")
            if submitted_new_device:
                # Check if user_id exists before creating the device
                if User.user_exists(managed_by_user_id):
                    new_device = Device(device_name, managed_by_user_id)
                    new_device.store_data()
                    st.write("Neues Gerät hinzugefügt.")
                else:
                    st.warning("Geräte-Verantwortlicher mit dieser ID existiert nicht.")

    elif device_action == "Gerät ändern":
        # Existing code for modifying existing device remains unchanged
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

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
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

            if not user_name.strip() or not email.strip():
                st.warning("Beide Felder müssen ausgefüllt werden!")
            else:

                # Überprüfen, ob der Benutzer bereits existiert
                existing_user = User.user_exists(email)

                if existing_user:
                    st.warning("Nutzer mit dieser E-Mail existiert bereits!")
                else:
                    new_user = User(user_name, email)
                    new_user.store_data()
                    st.write("Nutzer angelegt.")
            
