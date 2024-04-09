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
    def __init__(self, jid, password, centers, restrictions, app, socketio):
        super().__init__(jid, password)
        self.centers = centers
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

        markers_data = [{'name': center.name, 'lat': center.latitude,
                        'lng': center.longitude} for center in self.centers]
        self.socketio.emit('map_updated', {'map_data': markers_data})
