#Wartungssystem
from datetime import datetime,timedelta
from queries import find_devices
class Wartungskalender:
    @staticmethod
    def naechste_wartungen_abrufen():
        devices = find_devices()
        wartungen = []
        for device in devices:
            if 'created_at' in device and isinstance(device['created_at'], datetime):
                naechste_wartung = device['created_at'] + timedelta(days=90)
                wartungen.append({
                    'geraete_id': device['device_name'],
                    'naechste_wartung': naechste_wartung.strftime("%d-%m-%Y")
                })
        return wartungen


    @staticmethod
    def wartungskosten_pro_quartal_berechnen():
        anzahl_geraete = len(find_devices())
        kosten_pro_geraet = 50
        return anzahl_geraete * kosten_pro_geraet
