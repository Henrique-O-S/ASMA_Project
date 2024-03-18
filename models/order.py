class Order:
    def __init__(self, order_id, latitude, longitude, weight):
        self.order_id = order_id
        self.latitude = float(latitude.replace(',', '.'))  # Convert to float, replacing comma with dot if necessary
        self.longitude = float(longitude.replace(',', '.'))  # Convert to float, replacing comma with dot if necessary
        self.weight = int(weight)  # Convert to integer

    def get_order_id(self):
        return self.order_id

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_weight(self):
        return self.weight
    
    def __str__(self):
        return f"Order ID: {self.order_id}, Latitude: {self.latitude}, Longitude: {self.longitude}, Weight: {self.weight}"