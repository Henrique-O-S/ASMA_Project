import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class UpdatePointsBehaviour(CyclicBehaviour):
    def __init__(self, agent, interval):
        super().__init__()
        self.agent = agent
        self.interval = interval  # Interval in seconds between updates

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
            self, interval=0.1))  # Add the cyclic behaviour

    def update_visualization(self):
        self.centers[1].latitude += 0.01
        print("gato")
        self.drones[0].longitude += 0.01

        centers_data = [{'name': center.name, 'lat': center.latitude,
                        'lng': center.longitude} for center in self.centers]
        orders_data = [{'name': order.order_id, 'lat': order.latitude, 'lng': order.longitude}
                       for center in self.centers for order in center.orders]
        drones_data = [{'name': "drone_" + str(drone.number), 'lat': drone.latitude, 'lng': drone.longitude,
                        'orders': [order.order_id for order in drone.orders]} for drone in self.drones]
        self.socketio.emit(
            'map_updated', {'center_data': centers_data, 'order_data': orders_data, 'drone_data': drones_data})
