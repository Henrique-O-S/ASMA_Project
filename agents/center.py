import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour, CyclicBehaviour, FSMBehaviour, State
from spade.message import Message
from spade.template import Template
import datetime

STATE_ONE = "[AvailabilityCheck]"
STATE_TWO = "[AvailabilityCheckResponse]"
STATE_THREE = "STATE_THREE"

class CenterAgent(Agent):
    def __init__(self, jid, password, center_id, latitude, longitude, weight, orders, drones=[]):
        super().__init__(jid, password)
        self.center_id = center_id
        self.latitude = latitude
        self.longitude = longitude
        self.weight = weight
        self.orders = orders
        self.drones = drones
        self.dronesAvailable = []

    async def setup(self):
        print(
            f"Center agent {self.center_id} started at ({self.latitude}, {self.longitude}) with weight {self.weight}")
        
        fsm = self.CenterFSMBehaviour()
        fsm.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=self.StateTwo())
        fsm.add_state(name=STATE_THREE, state=self.StateThree())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)
        fsm.add_transition(source=STATE_TWO, dest=STATE_ONE)
        self.add_behaviour(fsm)

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
    
    class CenterFSMBehaviour(FSMBehaviour):
        async def on_start(self):
            print(f"FSM starting at initial state {self.current_state}")

        async def on_end(self):
            print(f"FSM finished at state {self.current_state}")
            await self.agent.stop()

    class StateOne(State):
        async def run(self):
            print(f"Center agent checking available drones:")

            # Send message to drones asking for their availability
            for drone in self.agent.drones:
                print(f"Checking availability of drone {drone.jid}")
                msg = spade.message.Message(to=str(drone.jid))
                msg.body = "[AvailabilityCheck]"
                await self.send(msg)
            self.set_next_state(STATE_TWO)


    class StateTwo(State):
        async def run(self):
            print("Center receive running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                if msg.body == "[Available]":
                    print(f"Drone {msg.sender} is available")
                    self.set_next_state(STATE_THREE)

            else:
                print("Did not received any message after 10 seconds")
                self.set_next_state(STATE_ONE)


    class StateThree(State):
        async def run(self):
            print("I'm at state three (final state)")
            msg = await self.receive(timeout=5)
            print(f"State Three received message {msg.body}")
            # no final state is setted, since this is a final state

    class CheckAvailableDronesBehaviour(PeriodicBehaviour):
        async def run(self):
            print(f"Center agent checking available drones:")

            # Send message to drones asking for their availability
            for drone in self.agent.drones:
                print(f"Checking availability of drone {drone.jid}")
                msg = spade.message.Message(to=str(drone.jid))
                msg.body = "[AvailabilityCheck]"
                await self.send(msg)

            #await self.agent.stop()

    class ReceiveMessageBehaviour(CyclicBehaviour):
        async def run(self):
            print("Center receive running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                if msg.body == "[Available]":
                    print(f"Drone {msg.sender} is available")

            else:
                print("Did not received any message after 10 seconds")
                self.kill()
    
class ProcessOrdersBehaviour(OneShotBehaviour):
    async def run(self):
        print(f"Center agent processing orders:")
        for order in self.agent.orders:
            print(order)
        for drone in self.agent.drones:
            print(drone)

        # Here you can add your logic to process orders, e.g., assign them to delivery drivers, update statuses, etc.

        #await self.agent.stop()


if __name__ == "__main__":
    print("This module defines the CenterAgent class. It should be imported in other scripts.")
