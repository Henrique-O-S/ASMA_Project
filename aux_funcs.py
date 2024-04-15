from math import radians, sin, cos, sqrt, atan2


def extract_numeric_value(value_str):
    """
    Extracts the numeric value from a string containing numeric value followed by units.
    Example: "20km/h" -> 20
    """
    numeric_part = ""
    for char in value_str:
        if char.isdigit() or char == ".":
            numeric_part += char
        else:
            break
    return float(numeric_part) if numeric_part else None


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface
    using the Haversine formula.

    Parameters:
    lat1 (float): Latitude of the first point in degrees.
    lon1 (float): Longitude of the first point in degrees.
    lat2 (float): Latitude of the second point in degrees.
    lon2 (float): Longitude of the second point in degrees.

    Returns:
    float: Distance between the two points in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_earth = 6371  # Radius of the Earth in kilometers
    distance = radius_earth * c

    return distance


def assign_orders_to_drone(orders, drone_capacity, center_location):
    orders_sorted_by_weight = sorted(
        orders, key=lambda x: x.weight, reverse=True)
    orders_with_ratios = []

    for order in orders_sorted_by_weight:
        distance_to_center = haversine_distance(
            center_location[0], center_location[1], order.latitude, order.longitude)
        weight_to_distance_ratio = order.weight * \
            distance_to_center if distance_to_center != 0 else float('inf')
        orders_with_ratios.append((order, weight_to_distance_ratio))

    # Sort orders by weight-to-distance ratio in ascending order
    orders_with_ratios.sort(key=lambda x: (x[0].weight, x[1]))

    assigned_orders = []
    current_capacity = 0

    for order, _ in orders_with_ratios:
        if current_capacity + order.weight <= drone_capacity:
            assigned_orders.append(order)
            current_capacity += order.weight
        else:
            break  # Stop assigning orders if drone's capacity is reached

    return assigned_orders


def calculate_savings(orders, center_location):
    savings = {}
    n = len(orders)
    for i in range(n):
        for j in range(i+1, n):
            savings[(i, j)] = haversine_distance(center_location[0], center_location[1], orders[i].latitude, orders[i].longitude) + haversine_distance(center_location[0],
                                                                                                                                                       center_location[1], orders[j].latitude, orders[j].longitude) - haversine_distance(orders[i].latitude, orders[i].longitude, orders[j].latitude, orders[j].longitude)
    return savings


def clarke_wright_savings(orders, drone_capacity, center_location):
    savings = calculate_savings(orders, center_location)
    sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)
    route = []
    route_capacity = 0

    for (i, j), s in sorted_savings:
        if i not in route and j not in route:
            if route_capacity + orders[i].weight <= drone_capacity:
                route.append(i)
                route_capacity += orders[i].weight
            if route_capacity + orders[j].weight <= drone_capacity:
                route.append(j)
                route_capacity += orders[j].weight
            if route_capacity >= drone_capacity:
                break

    # Convert indices to Order objects
    best_route_orders = [orders[idx] for idx in route]

    return best_route_orders


def evaluate_proposals(proposals):
    best_proposal = None
    max_orders = 0
    max_weight = 0

    for proposal in proposals:
        center_id, orders = proposal
        num_orders = len(orders)
        total_weight = 0
        for order in orders:
            total_weight += order["weight"]

        if num_orders > max_orders or (num_orders == max_orders and total_weight > max_weight):
            max_orders = num_orders
            max_weight = total_weight
            best_proposal = (center_id, orders)

    return best_proposal
