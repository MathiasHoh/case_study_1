import streamlit as st
from datetime import datetime, timedelta
from devices import Device
from users import User
from tinydb import TinyDB, Query
from serializer import serializer
from tinydb import TinyDB, Query
import os

class ReservationSystem:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('reservations')

    @classmethod
    def reserve_device(cls, device_name, user_id, start_time, end_time):
        # Überprüfen, ob das Gerät für den angegebenen Zeitraum bereits reserviert ist
        existing_reservations = cls.db_connector.search(
            (Query().device_name == device_name) &
            ((Query().start_time <= start_time <= Query().end_time) | (Query().start_time <= end_time <= Query().end_time))
        )

        if existing_reservations:
            raise ValueError("Das Gerät ist für diesen Zeitraum bereits reserviert!")

        reservation_data = {
            'Gerät': device_name,
            'Benutzer': user_id,
            'Beginn': start_time,
            'Ende': end_time
        }

        cls.db_connector.insert(reservation_data)

    @classmethod
    def get_reservations_for_device(cls, device_name):
        ReservationQuery = Query()
        reservations = cls.db_connector.search(ReservationQuery.device_name == device_name)
        return reservations

