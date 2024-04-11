from spade import agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour, FSMBehaviour, State
from spade.message import Message
from spade.template import Template

STATE_ONE = "[WaitAvailabilityCheck]"
STATE_TWO = "[WaitInstructions]"
STATE_THREE = "STATE_THREE"

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
        
        fsm = self.DroneFSMBehaviour()
        fsm.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=self.StateTwo())
        fsm.add_state(name=STATE_THREE, state=self.StateThree())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_ONE, dest=STATE_ONE)
        fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)
        fsm.add_transition(source=STATE_TWO, dest=STATE_ONE)
        self.add_behaviour(fsm)

        #b1 = self.ReceiveMessageBehaviour()
        #self.add_behaviour(b1)

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
    
    class DroneFSMBehaviour(FSMBehaviour):
        async def on_start(self):
            print(f"Drone FSM starting at initial state {self.current_state}")

        async def on_end(self):
            print(f"Drone FSM finished at state {self.current_state}")
            await self.agent.stop()

    class StateOne(State):
        async def run(self):
            print("Waiting for availability check from the center")
            msg = await self.receive(timeout=10)  # Wait for a message for 10 seconds
            if msg:
                if msg.body == "[AvailabilityCheck]":
                    print("Received availability check from center")
                    response_msg = Message(to=str(msg.sender))
                    response_msg.body = "[Available]"
                    await self.send(response_msg)
                    self.set_next_state(STATE_TWO)
                else:
                    print("Received unexpected message")
                    self.set_next_state(STATE_ONE)
            else:
                print("Did not receive availability check within 10 seconds")
                self.set_next_state(STATE_ONE)

    class StateTwo(State):
        async def run(self):
            print("Waiting for instructions from the center")
            msg = await self.receive(timeout=10)  # Wait for a message for 10 seconds
            if msg:
                print(f"Received instructions from center: {msg.body}")
                # Process the instructions (e.g., execute delivery)
                self.set_next_state(STATE_THREE)
            else:
                print("Did not receive any instructions after 10 seconds")
                self.set_next_state(STATE_ONE)

    class StateThree(State):
        async def run(self):
            print("Final state reached. Mission accomplished!")
        
    class ReceiveMessageBehaviour(CyclicBehaviour):
        async def run(self):
            print("Drone receive running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                if msg.body == "[AvailabilityCheck]":
                    print("Availability check received")
                    reply = msg.make_reply()
                    reply.body = "[Available]"
                    await self.send(reply)
            else:
                print("Did not received any message after 10 seconds")
                self.kill()


class DroneBehaviour(OneShotBehaviour):
    async def run(self):
        print(f"Drones orders:")
        for order in self.agent.orders:
            print(order)

        # Here you can add your logic to process orders, e.g., assign them to delivery drivers, update statuses, etc.

        await self.agent.stop()
