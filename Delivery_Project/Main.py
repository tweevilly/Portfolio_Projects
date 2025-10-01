# Author : Thuy-Vi Hatfield
# Student ID : 011650621
# Title : C950 WGUPS Routing Program 

import csv
import datetime
import Truck
from builtins import ValueError

from CreateHashTable import CreateHashMap
from Package import Package

# Read the file of address information
with open("CSV/Address_File.csv") as csvfile1:
    CSV_Address = csv.reader(csvfile1)
    CSV_Address = list(CSV_Address)

# Read the file of distance information
with open("CSV/Distance_File.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)


# Read the file of package information
with open("CSV/Package_File.csv") as csvfile2:
    CSV_Package = csv.reader(csvfile2)
    CSV_Package = list(CSV_Package)

# Load package objects into the hash table: package_hash_table___________________________________________________________________________________________________________________________
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pStatus = "At Hub"
    
            # Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus)

            # Insert data into hash table
            package_hash_table.insert(pID, p)


# Method for finding distance between two addresses___________________________________________________________________________________________________________________________________________
def distance_in_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]

    return float(distance)


# Method to get address number from string literal of address
def extract_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Constraints__________________________________________________________________________________________________________________________________________________________________________

package_constraints = {
    3:  {"truck": 2},
    6:  {"available_time": datetime.timedelta(hours=9, minutes=5)},
    9:  {"available_time": datetime.timedelta(hours=10, minutes=20),
          "corrected_address": {
                "address": "410 S State St",
                "city": "Salt Lake City",
                "state": "UT",
                "zipcode": "84111"
        }
    },
    14: {"deliver_with": [15, 19]},
    15: {"deliver_with": [14, 19]},   
    16: {"deliver_with": [13, 19, 20]},
    19: {"deliver_with": [13, 14, 16, 20]},
    20: {"deliver_with": [13, 16, 19]},
    18: {"truck": 2},
    25: {"available_time": datetime.timedelta(hours=9, minutes=5)},
    28: {"available_time": datetime.timedelta(hours=9, minutes=5)},
    32: {"available_time": datetime.timedelta(hours=9, minutes=5)},
    36: {"truck": 2},
    38: {"truck": 2},
}

package_deadlines = {
    1: "10:30",
    6: "10:30",
    13: "10:30",
    14: "10:30",
    16: "10:30",
    20: "10:30",
    25: "10:30",
    29: "10:30",
    30: "10:30",
    31: "10:30",
    34: "10:30",
    40: "10:30",
    15: "9:00"
}


# auto_load trucks__________________________________________________________________________________________________________________________
def auto_load_trucks(package_hash_table, trucks): # Assigns packages to trucks automatically based on constraints.

    for t in trucks:
        t.packages.clear()

    for package_id in range(1, 41):
        package = package_hash_table.lookup(package_id)

        if not package:
            continue

        constraint = package_constraints.get(package_id, {})
        
  
        # Truck-specific constraints
        if "truck" in constraint:
            trucks[constraint["truck"] - 1].packages.append(package_id)
            continue

        # Delayed packages, wait fro available time, most likely load on truck3
        if "available_time" in constraint:
            trucks[2].packages.append(package_id)  # load onto truck3
            continue

        # Deliver-with constraints
        if "deliver_with" in constraint:
            if package_id not in trucks[0].packages:
                trucks[0].packages.append(package_id)
            for companion in constraint["deliver_with"]:
                if companion not in trucks[0].packages:
                    trucks[0].packages.append(companion)
            continue

        # Deadline-sensitive packages, priority on truck1
        if package_id in package_deadlines:
            trucks[0].packages.append(package_id)
            continue

        # Distribute packages evenly 
        smallest_truck = min(trucks, key=lambda tr: len(tr.packages))
        smallest_truck.packages.append(package_id)

#truck delivery__________________________________________________________________________________________________________________

def delivering_packages(truck):
    not_delivered = [package_hash_table.lookup(pid) for pid in truck.packages]
    truck.packages.clear()

    while not_delivered:
        next_address = float("inf")
        next_package = None
        for package in not_delivered:
            dist = distance_in_between(extract_address(truck.address), extract_address(package.address))
            if dist <= next_address:
                next_address = dist
                next_package = package

        truck.packages.append(next_package.ID)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

package_hash_table = CreateHashMap()
load_package_data("CSV/Package_File.csv", package_hash_table)

truck1 = Truck.Truck(16, 18, None, [], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck.Truck(16, 18, None, [], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
truck3 = Truck.Truck(16, 18, None, [], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

trucks = [truck1, truck2, truck3]
auto_load_trucks(package_hash_table, trucks)

delivering_packages(truck1)
delivering_packages(truck2)
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3)

# User Interface_________________________________________________________________________________________________________________________
class Main:
    def __init__(self, trucks, package_hash_table):
        self.trucks = trucks
        self.package_hash_table = package_hash_table

    def run(self):
        print("\nWestern Governors University Parcel Service (WGUPS)\n")

        while True:
            total_mileage = sum(truck.mileage for truck in self.trucks)
            last_delivery_time = max(
                (pkg.delivery_time for truck in self.trucks for pkg_id in truck.packages
                 if (pkg := self.package_hash_table.lookup(pkg_id)) and pkg.delivery_time),
                default=None
            )
            total_time_hours = (last_delivery_time - min(truck.depart_time for truck in self.trucks)).total_seconds() / 3600 \
                if last_delivery_time else 0

            print(f"Total mileage for all trucks: {total_mileage:.2f} miles")
            if last_delivery_time:
                #self check on times to query package info
                print(f"Time of last delivery: {str(last_delivery_time)}")
                print(f"Total delivery time: {total_time_hours:.2f} hours\n")
            else:
                print("No deliveries completed yet.\n")

            # Menu
            print("Options:")
            print("1 - View delivery status of packages")
            # for self check on constraints
            print("2 - See which packages are on which truck")
            print("Esc - Quit program")

            choice = input("Select an option: ").strip().lower()

            if choice == "1":
                convert_timedelta = self.get_user_time()
                self.view_packages(convert_timedelta)
            elif choice == "2":
                self.show_truck_packages()
            elif choice == "esc":
                print("\nProgram closed.")
                break
            else:
                print("Invalid option. Please try again.\n")

    def get_user_time(self):
        while True:
            try:
                user_time = input("\nEnter time to check package status (HH:MM:SS): ").strip()
                h, m, s = map(int, user_time.split(":"))
                return datetime.timedelta(hours=h, minutes=m, seconds=s)
            except ValueError:
                print("Invalid format. Please enter time as HH:MM:SS.\n")

    def view_packages(self, convert_timedelta):
        while True:
            choice = input("\nView an individual package ('solo') or all packages ('all'): ").strip().lower()
            if choice in ["solo", "all"]:
                break
            print("Invalid choice. Please type 'solo' or 'all'.\n")

        if choice == "solo":
            self.show_single_package(convert_timedelta)
        elif choice == "all":
            self.show_all_packages(convert_timedelta)

    def show_single_package(self, convert_timedelta):
        while True:
            try:
                package_id = int(input("\nEnter numeric package ID: ").strip())
                package = self.package_hash_table.lookup(package_id)
                if package is None:
                    raise ValueError
                package.update_status(convert_timedelta)
                print(f"\n{package}\n")
                break
            except ValueError:
                print("Invalid package ID. Please enter a valid number.\n")

    def show_all_packages(self, convert_timedelta):
        print()

        for package_id in range(1, 41):
            package = self.package_hash_table.lookup(package_id)
            package.update_status(convert_timedelta)
            print(package)
        print()

    def show_truck_packages(self):
        print("\nPackages assigned to each truck:")
        for i, truck in enumerate(self.trucks, start=1):
            print(f"Truck {i}: {truck.packages}")
        print()



# Run Program_________________________________________________________________________________________________________________________________________________________________
trucks = [truck1, truck2, truck3]
main_program = Main(trucks, package_hash_table)
main_program.run()