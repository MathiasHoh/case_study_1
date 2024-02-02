#Wartungssystem
from datetime import datetime,timedelta
from queries import find_devices
from serializer import serializer
from tinydb import TinyDB, Query
import os
class Wartungskalender:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('wartungen')

    @staticmethod
    def naechste_wartungen_abrufen():
        devices = find_devices()
        for device in devices:
            if 'created_at' in device and isinstance(device['created_at'], datetime):
                naechste_wartung = device['created_at'] + timedelta(days=90)
                wartung_data = {
                    'geraete_id': device['device_name'],
                    'naechste_wartung': naechste_wartung.strftime("%Y-%m-%d")  # Storing date as string in ISO format
                }
                # Store maintenance data into the database
                Wartungskalender.db_connector.insert(wartung_data)

        # Return the list of maintenance data (optional)
        return Wartungskalender.db_connector.all()

    @staticmethod
    def wartungskosten_pro_quartal_berechnen():
        anzahl_geraete = len(find_devices())
        kosten_pro_geraet = 1500
        return anzahl_geraete * kosten_pro_geraet
