# device.py
import os
from tinydb import TinyDB, Query
from serializer import serializer
from datetime import datetime, timedelta

class Device:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    def __init__(self, device_name: str, managed_by_user_id: str, maintenance_interval: timedelta = timedelta(days=90), maintenance_cost: float = 0.0):
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.maintenance_interval = maintenance_interval
        self.maintenance_cost = maintenance_cost  

    def store_data(self):
        print("Storing data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)

        data_to_store = {
            'device_name': self.device_name,
            'managed_by_user_id': self.managed_by_user_id,
            'is_active': self.is_active,
            'maintenance_interval': self.maintenance_interval.days,
            'maintenance_cost': float(self.maintenance_cost)
        }

        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(data_to_store, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(data_to_store)
            print("Data inserted.")

    def calculate_next_maintenance_date(self):
        # Dummy logic for demonstration purposes
        last_maintenance_date = datetime.now()
        next_maintenance_date = last_maintenance_date + self.maintenance_interval
        return next_maintenance_date.strftime("%d-%m-%Y")
    
    def calculate_maintenance_costs_per_quarter(self):
        # Dummy logic for demonstration purposes
        return self.maintenance_cost
    @classmethod
    def load_all_devices(cls):
        """Load all devices from the database."""
        DeviceQuery = Query()
        result = cls.db_connector.all()
        devices = []

        for data in result:
            device = cls(
                data['device_name'],
                data['managed_by_user_id'],
                maintenance_interval=timedelta(days=data.get('maintenance_interval', 90)),
                maintenance_cost=data.get('maintenance_cost', 0.0)  # Lade die Wartungskosten
            )
            device.is_active = data['is_active']
            devices.append(device)

        return devices

    @classmethod
    def device_exists(cls, device_name):
        print("Checking if device exists...")
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.device_name == device_name)

        if result:
            print("Device already exists.")
            return True
        else:
            print("Device does not exist.")
            return False

    def __str__(self):
        return f'Device {self.device_name} ({self.managed_by_user_id})'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def load_data_by_device_name(cls, device_name):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.device_name == device_name)

        if result:
            data = result[0]
            return cls(data['device_name'], data['managed_by_user_id'])
        else:
            return None

if __name__ == "__main__":
    device1 = Device("Device1", "one@mci.edu", maintenance_interval=timedelta(days=60), maintenance_cost=100.0)
    device2 = Device("Device2", "two@mci.edu", maintenance_interval=timedelta(days=30), maintenance_cost=200.0)
    device3 = Device("Device3", "two@mci.edu", maintenance_interval=timedelta(days=30), maintenance_cost=300.0)
    device4 = Device("Device4", "four@mci.edu", maintenance_interval=timedelta(days=45), maintenance_cost=400.0)  
    device5 = Device("Drucker", "five@mci.edu", maintenance_interval=timedelta(days=60), maintenance_cost=500.0)  
    device6 = Device("Kopierer", "six@mci.edu", maintenance_interval=timedelta(days=90), maintenance_cost=600.0)
    device7 = Device("Roboterarm", "seven@mci.edu", maintenance_interval=timedelta(days=90), maintenance_cost=600.0)
    device8 = Device("Computer", "eight@mci.edu", maintenance_interval=timedelta(days=90), maintenance_cost=600.0)
  


    device1.store_data()
    device2.store_data()
    device3.store_data()
    device4.store_data()
    device5.store_data()
    device6.store_data()
    device7.store_data()
    device8.store_data()

    loaded_device = Device.load_data_by_device_name('Device2')
    if loaded_device:
        print(f"Loaded Device: {loaded_device}")
    else:
        print("Device not found.")
