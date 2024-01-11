import os
from tinydb import TinyDB, Query
from users import User  # Stellen Sie sicher, dass die User-Klasse korrekt importiert ist
from datetime import datetime, timedelta

class Device():
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('devices')

    # Constructor
    def __init__(self, device_name: str, managed_by_user_id: str, end_of_life: datetime,
                 first_maintenance: datetime, maintenance_interval: int, maintenance_cost: float):
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.__last_update = datetime.now()
        self.__creation_date = datetime.now()
        self.end_of_life = end_of_life
        self.first_maintenance = first_maintenance
        self.next_maintenance = first_maintenance
        self.__maintenance_interval = maintenance_interval
        self.__maintenance_cost = maintenance_cost

    def __str__(self):
        return f'Device {self.device_name} ({self.managed_by_user_id})'

    def __repr__(self):
        return f'Device({self.device_name}, {self.managed_by_user_id})'

    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    @classmethod
    def load_data_by_device_name(cls, device_name):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.device_name == device_name)
        if result:
            data = result[0]
            return cls(data['device_name'], data['managed_by_user_id'],
                       data['end_of_life'], data['first_maintenance'],
                       data['__maintenance_interval'], data['__maintenance_cost'])
        else:
            return None

    def update_last_update(self):
        self.__last_update = datetime.now()

    def schedule_next_maintenance(self):
        self.next_maintenance += timedelta(days=self.__maintenance_interval)

    def perform_maintenance(self):
        # Hier können Wartungsaktionen durchgeführt werden
        # Zum Beispiel: Protokollieren, dass die Wartung durchgeführt wurde
        self.update_last_update()
        self.schedule_next_maintenance()

    def is_due_for_maintenance(self):
        return datetime.now() >= self.next_maintenance