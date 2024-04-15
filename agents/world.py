import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

# fps imports down bellow
#from dotenv import load_dotenv
import os

#load_dotenv()


class UpdatePointsBehaviour(CyclicBehaviour):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        #self.interval = float(os.getenv('UPDATE_INTERVAL'))  # Interval in seconds between updates
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

    async def setup(self):
        await super().setup()
        self.add_behaviour(UpdatePointsBehaviour(
            self))  # Add the cyclic behaviour

    def update_visualization(self):

        centers_data = [{'name': center.name, 'lat': center.latitude,
                        'lng': center.longitude} for center in self.centers]
        orders_data = [{'name': order.id, 'lat': order.latitude, 'lng': order.longitude}
                       for center in self.centers for order in center.orders]
        drones_data = [{'name': "drone_" + str(drone.number), 'lat': drone.latitude, 'lng': drone.longitude,
                        'orders': [order["id"] for order in drone.orders]} for drone in self.drones]
        self.socketio.emit(
            'map_updated', {'center_data': centers_data, 'order_data': orders_data, 'drone_data': drones_data})
