from aux_funcs import sort_orders_by_shortest_path
from models.order import Order

# Define a simple test function
def test_sort_orders_by_shortest_path():
    # Define some sample data
    orders = [
        Order(1, str(52.52), str(13.405), 0),
        Order(2, str(48.85), str(2.35), 0),
        Order(3, str(51.51), str(-0.13), 0)
    ]

    orders1 = [
        Order(1, str(34.0522), str(-118.2437), 0),  # Los Angeles
        Order(2, str(41.8781), str(-87.6298), 0),   # Chicago
        Order(3, str(29.7604), str(-95.3698), 0)    # Houston
    ]
    center_location = (40.7128, -74.0060)  # Example center location (New York)
    center_location1 = (40.7128, -74.0060)  # Example center location (New York)

    # Call the function
    sorted_orders, total_distance = sort_orders_by_shortest_path(orders1, center_location1)
    
    # Assert that the sorted_orders are indeed sorted by shortest path
    # Add your assertions here based on the expected output
    
    print("sorted_orders", sorted_orders)
    print("total_distance", total_distance)

    # Assert that total_distance is a non-negative number
    assert total_distance >= 0, "Total distance should be non-negative"

# Run the test function
test_sort_orders_by_shortest_path()

