from spade import agent
from spade.behaviour import CyclicBehaviour

class DroneAgent(agent.Agent):
    def __init__(self, jid, password, capacity, autonomy, velocity, number):
        super().__init__(jid, password)
        self.capacity = capacity
        self.autonomy = autonomy
        self.velocity = velocity
        self.number = number


class CreateDroneAgentsBehaviour(CyclicBehaviour):
    def __init__(self, drone_data):
        super().__init__()
        self.drone_data = drone_data

    async def on_start(self):
        for data in self.drone_data:
            drone_agent = DroneAgent(f"drone_{data['number']}@localhost", "password", data['capacity'], data['autonomy'], data['velocity'], data['number'])
            print(drone_agent)
        await drone_agent.start()

    async def run(self):
        print("gato")