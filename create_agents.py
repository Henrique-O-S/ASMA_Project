import csv
import asyncio
import os
import sys
from spade.agent import Agent
from agents.center import CenterAgent  # Importing the CenterAgent class
from agents.drone import DroneAgent  # Importing the DroneAgent class
from models.order import Order  # Importing the DroneAgent class

from aux_funcs import extract_numeric_value

def read_center_csv(filename):
    centers = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)  # Skip the header
        params = next(reader)  # Read the parameters
        center_id, latitude, longitude, weight = params
        latitude = float(latitude.replace(",", "."))
        longitude = float(longitude.replace(",", "."))
        weight = float(weight)
        orders = []
        for row in reader:
            order_id, order_latitude, order_longitude, order_weight = row
            orders.append(Order(order_id, order_latitude,
                          order_longitude, order_weight))
        centers.append(CenterAgent(center_id + "@localhost", "1234",
                                   center_id, latitude, longitude, weight, orders))
    return centers


def read_drone_csv(filename):
    drones = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)  # Skip the header
        for row in reader:
            drone_id, capacity, autonomy, velocity = row
            drones.append(DroneAgent(drone_id + "@localhost", "1234",
                                     extract_numeric_value(capacity), extract_numeric_value(autonomy), extract_numeric_value(velocity)))
    return drones


def main():
    center_files = ["data/delivery_center1.csv",
                    "data/delivery_center2.csv"]  # List of CSV files
    drone_file = "data/delivery_drones.csv"  # List of CSV files
    agents = []

    for filename in center_files:
        if os.path.exists(filename):
            centers = read_center_csv(filename)
            agents.extend(centers)
        else:
            print(f"File {filename} not found.")

    if os.path.exists(drone_file):
        drones = read_drone_csv(drone_file)
        for agent in agents:
            agent.drones = drones
        agents.extend(drones)
    else:
        print(f"File {filename} not found.")

    async def run_agents():
        for agent in agents:
            await agent.start(auto_register=True)

    asyncio.run(run_agents())


if __name__ == "__main__":
    main()
