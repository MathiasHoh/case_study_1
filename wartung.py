#Wartungssystem
from datetime import datetime,timedelta
from queries import find_devices
class Wartungskalender:
    @staticmethod
    def naechste_wartungen_abrufen():
        devices = find_devices()  # Funktion, die alle Geräte abruft
        wartungen = []
        for device in devices:
            naechste_wartung = device['created_at'] + timedelta(days=90)
            wartungen.append({
                'geraete_id': device['device_name'],
                'naechste_wartung': naechste_wartung.strftime("d%-m%-Y%")
            })
        return wartungen

    @staticmethod
    def wartungskosten_pro_quartal_berechnen():
        anzahl_geraete = len(find_devices())
        kosten_pro_geraet = 50
        return anzahl_geraete * kosten_pro_geraet
