import csv
import asyncio
import os
import sys
from spade.agent import Agent
from agents.center import CenterAgent  # Importing the CenterAgent class


def read_csv(filename):
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
            order_latitude = float(order_latitude.replace(",", "."))
            order_longitude = float(order_longitude.replace(",", "."))
            order_weight = float(order_weight)
            orders.append({
                "id": order_id,
                "latitude": order_latitude,
                "longitude": order_longitude,
                "weight": order_weight
            })
        centers.append(CenterAgent(center_id + "@localhost", "1234",
                                   center_id, latitude, longitude, weight, orders))
    return centers


def main():
    csv_files = ["data/delivery_center1.csv",
                 "data/delivery_center2.csv"]  # List of CSV files
    agents = []

    for filename in csv_files:
        if os.path.exists(filename):
            centers = read_csv(filename)
            agents.extend(centers)
        else:
            print(f"File {filename} not found.")

    async def run_agents():
        for agent in agents:
            await agent.start(auto_register=True)

    asyncio.run(run_agents())


if __name__ == "__main__":
    main()
