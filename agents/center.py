import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class CenterAgent(Agent):
    def __init__(self, jid, password, center_id, latitude, longitude, weight, orders, drones=[]):
        super().__init__(jid, password)
        self.center_id = center_id
        self.latitude = latitude
        self.longitude = longitude
        self.weight = weight
        self.orders = orders
        self.drones = drones

    async def setup(self):
        print(
            f"Center agent {self.center_id} started at ({self.latitude}, {self.longitude}) with weight {self.weight}")
        b = ProcessOrdersBehaviour()
        self.add_behaviour(b)

    def get_center_id(self):
        return self.center_id

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_weight(self):
        return self.weight

    def get_orders(self):
        return self.orders

    def get_drones(self):
        return self.drones


class ProcessOrdersBehaviour(OneShotBehaviour):
    async def run(self):
        print(f"Center agent processing orders:")
        for order in self.agent.orders:
            print(order)
        for drone in self.agent.drones:
            print(drone)

        # Here you can add your logic to process orders, e.g., assign them to delivery drivers, update statuses, etc.

        await self.agent.stop()


if __name__ == "__main__":
    print("This module defines the CenterAgent class. It should be imported in other scripts.")
