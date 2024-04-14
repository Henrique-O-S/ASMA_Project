import spade
import re
from spade import agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour, FSMBehaviour, State
from spade.message import Message
from spade.template import Template
from aux_funcs import evaluate_proposals
import json

ASK_ORDERS = "[AskOrders]"
AWAIT_ORDERS = "[AwaitOrders]"
ANSWER_PROPOSALS = "[AnswerProposals]"

class DroneAgent(agent.Agent):
    def __init__(self, jid, password, capacity, autonomy, velocity, initialPos, centers=[], orders=[]):
        super().__init__(jid, password)
        self.capacity = capacity
        self.current_capacity = capacity
        self.autonomy = autonomy
        self.velocity = velocity
        self.initialPos = initialPos
        self.latitude = 0
        self.longitude = 0
        self.number = int(self.extract_numeric_value(jid))
        self.centers = centers
        self.orders = orders
        self.proposals=[]

    async def setup(self):
        print(
            f"Drone agent {self.number} started at ({self.latitude}, {self.longitude}) with capacity {self.capacity}, autonomy {self.autonomy} and velocity {self.velocity}")
        
        fsm = self.DroneFSMBehaviour()
        fsm.add_state(name=ASK_ORDERS, state=self.AskOrders(), initial=True)
        fsm.add_state(name=AWAIT_ORDERS, state=self.AwaitOrders())
        fsm.add_state(name=ANSWER_PROPOSALS, state=self.AnswerProposals())
        fsm.add_transition(source=ASK_ORDERS, dest=AWAIT_ORDERS)
        fsm.add_transition(source=AWAIT_ORDERS, dest=ANSWER_PROPOSALS)
        fsm.add_transition(source=AWAIT_ORDERS, dest=ASK_ORDERS)
        fsm.add_transition(source=ANSWER_PROPOSALS, dest=ASK_ORDERS)
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

    class AskOrders(State):
        async def run(self):
            print(f"Drone agent asking orders:")

            # Send message to drones asking for their availability
            for center in self.agent.centers:
                print(f"Asking orders from center {center}")
                msg = spade.message.Message(to=str(center))
                msg.body = "[AskOrders]-" + str(self.agent.current_capacity)
                await self.send(msg)

            self.set_next_state(AWAIT_ORDERS)

    class AwaitOrders(State):
        async def run(self):
            print("Waiting for orders from the center")
            proposals = []
            for center in self.agent.centers:
                msg = await self.receive(timeout=10)  # Wait for a message for 10 seconds
                if msg:
                    body_parts = msg.body.split("-")  # Split message body into parts
                    if len(body_parts) == 2 and body_parts[0] == "[OrdersAssigned]":
                        assigned_orders_str = body_parts[1]
                        assigned_orders = json.loads(assigned_orders_str)  # Convert string representation of list to actual list
                        print(f"Received orders from center {msg.sender}: {assigned_orders}")
                        proposals.append((re.match(r"center(\d+)@localhost", (str(msg.sender))).group(1), assigned_orders))
                    else:
                        print("Received unrecognized message")
                else:
                    print("Did not receive any instructions after 10 seconds")
                    break
                    

            if proposals:
                self.agent.proposals = proposals
                self.set_next_state(ANSWER_PROPOSALS)
            else:
                self.set_next_state(ASK_ORDERS)

    class AnswerProposals(State):
        async def run(self):
            print("Answering proposals")
            # Evaluate and select the best proposal
            best_proposal = evaluate_proposals(self.agent.proposals)
            if best_proposal:
                center_id, orders = best_proposal
                print(f"Selected proposal from center {center_id}: {orders}")
                # Add orders from the best proposal to self.orders
                self.agent.orders.extend(orders)
                # Send acceptance message to the selected center
                reply = Message(to=("center"+center_id+"@localhost"))
                reply.body = "[Accepted]"
                await self.send(reply)

                # Send rejection messages to other centers
                for other_proposal in self.agent.proposals:
                    if other_proposal[0] != center_id:
                        print(f"Rejecting proposal from center {other_proposal[0]}")
                        rejection_msg = Message(to=("center"+other_proposal[0]+"@localhost"))
                        rejection_msg.body = "[Rejected]"
                        await self.send(rejection_msg)
            else:
                print("No proposals received")
                self.set_next_state(ASK_ORDERS)

            self.agent.proposals = []
            self.agent.orders = [] # Should be removed after the next step is implemented
            print("SUCESSO MALUCO")
            self.set_next_state(ASK_ORDERS) # Should be substituted after the next step is implemented
            
