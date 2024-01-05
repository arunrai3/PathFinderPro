# Path Finder Pro

Welcome to PathFinderPro, a command-line Python application designed to optimize delivery routes using the nearest neighbor algorithm. This program is tailored for delivery services, providing an efficient and time-sensitive solution for managing package deliveries. PathFinderPro simulates the operation of three delivery trucks, each tasked with distributing packages according to specific criteria outlined in the `packageCSV.csv` file. Users can interact with the program via the command line to track deliveries, view package details, and analyze the efficiency of delivery routes.

## Features

- **Nearest Neighbor Algorithm:** Utilizes this algorithm to determine the most efficient delivery route, minimizing travel time and distance.
- **Command-Line Interface:** Easy-to-use command-line interface for running the program and interacting with the delivery data.
- **Multiple Truck Simulation:** Manages three trucks simultaneously to optimize delivery schedules and routes.
- **Time-Sensitive Deliveries:** Considers specific delivery time requirements as per package instructions to prioritize and schedule accordingly.
- **Custom Package Filtering:** Offers the flexibility to view all packages or filter packages by specific criteria such as weight, time delivered, or assigned truck.
- **Detailed Delivery Tracking:** Tracks each package’s delivery status in real-time, including the exact time of delivery.
- **Comprehensive Reporting:** Generates reports on the fly, providing insights into route efficiency, package status, and overall delivery performance.
- **CSV Package Data Integration:** Seamlessly imports package data from `packageCSV.csv`, allowing for easy data management and updates.

## Data

The PathFinderPro program extensively utilizes data stored in the `/data` folder to optimize delivery routes and manage package information. This data is fundamental to the program's operation, as it includes key details such as distances between locations and address information. 

### Current Data Structure:

- **Distances Data:** Contains the distances between various delivery points, essential for calculating the most efficient routes.
- **Address Data:** Provides detailed address information for each delivery location, ensuring accurate and reliable package delivery.

### Future Enhancements:

- **Google Maps API Integration:** In future updates, PathFinderPro aims to incorporate the Google Maps API. This enhancement will allow for greater flexibility and scalability, enabling users to input a broader range of locations and addresses. With this integration, the program will be able to handle dynamic routing based on real-time data and user-specific requirements, significantly expanding its capabilities and applicability in various logistical scenarios.


## Dependencies
All imports in this program are a part of Python's standard library and don't require any external packages.


## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/arunrai3/PathFinderPro.git

2. **Navigate to the Repository Directory:**
   ```bash
   cd PathFinderPro

3. **Run the Bot:**
   Execute the main script from root directory:
   ```bash
   python main.py


## Disclosure
This program is not to be distrubuted in anyway.
