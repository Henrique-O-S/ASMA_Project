from spade import agent
from spade.behaviour import CyclicBehaviour

class WorldAgent(agent.Agent):
    def __init__(self, jid, password, deliveryCenters, restrictions):
        super().__init__(jid, password)
        self.deliveryCenters = deliveryCenters
        self.restrictions = restrictions


class CreateWorldAgentsBehaviour(CyclicBehaviour):
    def __init__(self, drone_data):
        super().__init__()
        self.drone_data = drone_data

    async def on_start(self):
        for data in self.drone_data:
            drone_agent = WorldAgent(f"drone_{data['number']}@localhost", "password", data['capacity'], data['autonomy'], data['velocity'], data['number'])
            print(drone_agent)
        await drone_agent.start()

    async def run(self):
        print("gato")