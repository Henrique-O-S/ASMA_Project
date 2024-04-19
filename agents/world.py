import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import time
import requests
import os

class UpdatePointsBehaviour(CyclicBehaviour):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.interval = 0.1

    async def run(self):
        self.agent.update_visualization()
        await asyncio.sleep(self.interval)


class WorldAgent(Agent):
    def __init__(self, jid, password, centers, drones, restrictions, app, socketio):
        super().__init__(jid, password)
        self.centers = centers
        self.drones = drones
        self.restrictions = restrictions
        self.app = app
        self.socketio = socketio
        self.start_time = None
        self.end_time = None

    async def setup(self):
        await super().setup()
        self.add_behaviour(UpdatePointsBehaviour(self))
        self.start_time = time.time()

    def update_visualization(self):
        centers_data = [{'name': center.name, 'lat': center.latitude,
                        'lng': center.longitude, 'num_orders': len(center.orders)} for center in self.centers]
        orders_data = [{'name': order.id, 'lat': order.latitude, 'lng': order.longitude}
                       for center in self.centers for order in center.orders]
        drones_data = [{'name': "drone_" + str(drone.number), 'lat': drone.latitude, 'lng': drone.longitude,
                        'orders': [order[0] for order in drone.orders]} for drone in self.drones]
        self.socketio.emit(
            'map_updated', {'center_data': centers_data, 'order_data': orders_data, 'drone_data': drones_data})
        # Check if all orders are delivered
        if all(len(center.orders) == 0 for center in self.centers) and all(len(drone.orders) == 0 for drone in self.drones):
            self.end_time = time.time()
            delivery_time = self.end_time - self.start_time
            print(f"All orders delivered in {delivery_time} seconds.")
            print("Simulation finished.")
            self.signal_end()
            self.stop()

    def signal_end(self):
        self.socketio.emit('simulation_end', {})
        print("Simulation ended.")
        os._exit(0)



