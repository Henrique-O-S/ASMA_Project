from spade import agent
from spade.behaviour import OneShotBehaviour


class DroneAgent(agent.Agent):
    def __init__(self, jid, password, capacity, autonomy, velocity, initialPos, orders=[]):
        super().__init__(jid, password)
        self.capacity = capacity
        self.autonomy = autonomy
        self.velocity = velocity
        self.initialPos = initialPos
        self.latitude = 0
        self.longitude = 0
        self.number = int(self.extract_numeric_value(jid))
        self.orders = orders

    async def setup(self):
        print(
            f"Drone agent {self.number} started at ({self.latitude}, {self.longitude}) with capacity {self.capacity}, autonomy {self.autonomy} and velocity {self.velocity}")
        b = DroneBehaviour()
        self.add_behaviour(b)

    def extract_numeric_value(self, value_str):
        """
        Extracts the numeric value from a string containing numeric value followed by units.
        Example: "20km/h" -> 20
        """
        numeric_part = ""
        for char in value_str:
            if char.isdigit() or char == ".":
                numeric_part += char
        return float(numeric_part) if numeric_part else None

    def get_number(self):
        return self.number

    def get_capacity(self):
        return self.capacity

    def get_autonomy(self):
        return self.autonomy

    def get_velocity(self):
        return self.velocity

    def get_orders(self):
        return self.orders
    
    def get_latitude(self):
        return self.latitude
    
    def get_longitude(self):
        return self.longitude


class DroneBehaviour(OneShotBehaviour):
    async def run(self):
        print(f"Drones orders:")
        for order in self.agent.orders:
            print(order)

        # Here you can add your logic to process orders, e.g., assign them to delivery drivers, update statuses, etc.

        await self.agent.stop()
