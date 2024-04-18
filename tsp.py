import networkx as nx
import math

def haversine_distance(coord1, coord2):
    # Calculate the distance between two coordinates using the haversine distance formula
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

def tsp_algorithm(locations):
    # Create a graph
    G = nx.Graph()

    # Add nodes with latitude and longitude as attributes
    for i, (name, coord) in enumerate(locations.items()):
        G.add_node(i, name=name, coord=coord)

    # Add edges with weights representing real distances
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            distance = haversine_distance(locations[i], locations[j])
            G.add_edge(i, j, weight=distance)

    # Solve the TSP using an approximation algorithm
    tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)

    # Adjust node indices in tsp_path to match the graph
    tsp_path = [node_idx for node_idx in tsp_path if isinstance(node_idx, int)]

    # Calculate the total distance
    total_distance = sum(G[tsp_path[i - 1]][tsp_path[i]]['weight'] for i in range(1,len(tsp_path)))

    return tsp_path, total_distance


# Example usage
if __name__ == "__main__":
    # Example locations with latitude and longitude
    locations = {
        0: (40.7128, -74.0060),  # New York
        1: (34.0522, -118.2437),  # Los Angeles
        2: (41.8781, -87.6298),   # Chicago
        3: (29.7604, -95.3698)    # Houston
    }

    # Find the shortest path
    tsp_path, total_distance = tsp_algorithm(locations)

    # Print the result
    print("Shortest path:", tsp_path)
    print("Shortest distance:", total_distance)
