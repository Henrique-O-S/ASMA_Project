# ASMA Drone Delivery System

A multi-agent system simulation for drone delivery operations using SPADE (Smart Python Agent Development Environment). This project demonstrates autonomous drone coordination for package delivery from distribution centers to customers.

## 🎯 Project Overview

This project implements a **Multi-Agent System (MAS)** that simulates a drone delivery network with intelligent coordination between delivery centers and autonomous drones. The system features real-time visualization and optimized path planning for efficient package delivery operations.

### Key Features
- **Multi-Agent Coordination**: Centers and drones communicate to optimize delivery assignments
- **Real-time Visualization**: Web-based map interface showing live drone movements
- **Intelligent Path Planning**: Drones optimize routes based on capacity, autonomy, and location
- **Resource Management**: Dynamic consideration of drone capabilities and battery life
- **Scalable Architecture**: Support for multiple delivery centers and drone fleets

## 🏗️ System Architecture

### Agent Types

#### 🏢 CenterAgent (`agents/center.py`)
- Manages delivery orders for specific geographic areas
- Coordinates with available drones for optimal order assignment
- Tracks inventory and delivery status
- Broadcasts order availability to drone fleet

#### 🚁 DroneAgent (`agents/drone.py`)
- Autonomous delivery vehicles with configurable parameters:
  - **Capacity**: Maximum payload weight
  - **Autonomy**: Battery life/range limitations
  - **Velocity**: Speed of movement
- Implements intelligent bidding for orders based on efficiency
- Executes delivery missions with real-time position updates

#### 🌍 WorldAgent (`agents/world.py`)
- Central system coordinator and monitoring hub
- Provides real-time updates to the web interface
- Handles system-wide logging and status tracking
- Manages communication between all agents

### Data Models

#### 📦 Order (`models/order.py`)
```python
class Order:
    - id: Unique order identifier
    - latitude/longitude: Delivery coordinates
    - weight: Package weight for capacity planning
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Local XMPP server (ejabberd, prosody, or similar)
- Modern web browser for visualization

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ASMA_Project-main
   ```

2. **Install dependencies**:
   ```bash
   pip install spade flask flask-socketio flask-cors asyncio networkx
   ```

3. **Setup XMPP server**:
   - Install a local XMPP server (required for SPADE agent communication)
   - Ensure the server is running on `localhost` with default settings

### Running the Simulation

1. **Start the application**:
   ```bash
   python create_agents.py
   ```

2. **Access the web interface**:
   - Open your browser and navigate to `http://localhost:8000`
   - View real-time drone movements and delivery progress

## 📊 Configuration

### Delivery Centers Configuration
Edit `data/delivery_center1.csv` and `data/delivery_center2.csv`:
```csv
id;latitude;longitude;weight
center1;18,994237;72,825553;0
order1_1;19,017584;72,922585;20
order1_2;19,007584;72,912585;5
```
- First row: Center location (weight = 0)
- Subsequent rows: Orders with delivery coordinates and weights

### Drone Fleet Configuration
Configure drone specifications in `data/delivery_drones.csv`:
```csv
id;capacity;autonomy;velocity;initialPos
drone1;50kg;100km;60km/h;center1
drone2;30kg;80km;45km/h;center2
```

## 🔧 System Components

### Core Application Files
- **`create_agents.py`**: Main application entry point and agent orchestration
- **`aux_funcs.py`**: Utility functions for distance calculations and path optimization
- **`templates/map.html`**: Web interface for real-time visualization

### Agent Communication Protocol
The system uses SPADE's XMPP-based messaging for agent coordination:
- **Order Announcements**: Centers broadcast available orders
- **Proposal Submissions**: Drones bid for orders based on efficiency metrics
- **Assignment Confirmations**: Centers assign orders to optimal drones
- **Status Updates**: Real-time position and delivery status reports

## 📈 Simulation Workflow

1. **System Initialization**
   - Delivery centers load orders from CSV files
   - Drones register with centers and receive initial positioning

2. **Order Management Cycle**
   - Centers announce available orders to drone fleet
   - Drones evaluate orders and submit proposals
   - Centers assign orders based on optimization criteria

3. **Delivery Execution**
   - Assigned drones navigate to pickup locations
   - Path optimization for multiple order deliveries
   - Real-time position updates to world agent

4. **Monitoring and Visualization**
   - Web interface displays live drone movements
   - System status and delivery progress tracking

## �️ Customization Options

### Adding New Scenarios
- **Expand Order Sets**: Add more orders to center CSV files
- **Scale Drone Fleet**: Configure additional drones with varying capabilities
- **Geographic Areas**: Modify coordinates for different regions

### Extending Functionality
- **Custom Behaviors**: Implement additional agent behaviors
- **Enhanced Algorithms**: Improve path optimization and assignment logic
- **Advanced Visualization**: Add new features to the web interface

## 🧪 Technical Implementation

### Multi-Agent Behaviors
- **Finite State Machines**: Drone agents use FSM for delivery workflow
- **Periodic Behaviors**: Regular status updates and order checking
- **Message Templates**: Structured communication protocols

### Optimization Algorithms
- **Haversine Distance**: Accurate geographic distance calculations
- **Shortest Path**: Route optimization for multiple deliveries
- **Proposal Evaluation**: Multi-criteria decision making for order assignment

## 🎓 Educational Context

This project serves as a practical implementation for **ASMA (Agent Systems and Multi-Agent Systems)** coursework, demonstrating:
- Agent-based modeling and simulation
- Distributed coordination algorithms
- Real-time system visualization
- Multi-criteria optimization in autonomous systems

## � License

This project is developed for educational purposes as part of ASMA coursework. Feel free to use and modify for learning and research activities.

## 🔗 Technologies & Frameworks

- **[SPADE](https://spade-mas.readthedocs.io/)**: Smart Python Agent Development Environment
- **[Flask](https://flask.palletsprojects.com/)**: Web application framework
- **[Socket.IO](https://socket.io/)**: Real-time bidirectional communication
- **[NetworkX](https://networkx.org/)**: Graph algorithms for path optimization
- **HTML/CSS/JavaScript**: Frontend visualization and interactivity

---

*Developed as part of Agent Systems and Multi-Agent Systems (ASMA) coursework*
