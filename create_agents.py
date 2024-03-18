import asyncio
from spade import agent
from agents.drone import CreateDroneAgentsBehaviour

from data.read_data import read_drone_data


if __name__ == "__main__":
    file_path = 'data/data.xlsx'  # Adjust the file path as needed
    sheet_name = 'Drones'      # Adjust the sheet name as needed

    # Read drone data
    drone_data = read_drone_data(file_path, sheet_name)

    # Create and start agents
    if drone_data:
        create_agents_behaviour = CreateDroneAgentsBehaviour(drone_data)
        agent_instance = agent.Agent("agent@localhost", "password")
        agent_instance.add_behaviour(create_agents_behaviour)

        async def setup():
            await agent_instance.start()
            await asyncio.sleep(5)  # Wait for 5 seconds

        # Run the setup coroutine using asyncio.run
        asyncio.run(setup())
