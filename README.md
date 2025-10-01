# WGUPS Routing Program
**Scenario**:
    The Western Governors University Parcel Service (WGUPS) needs to determine an efficient route and delivery distribution for their daily local deliveries (DLD) because packages 
    are not currently being consistently delivered by their promised deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements that are listed in the attached “WGUPS Package File.”
    Your task is to determine an algorithm, write code, and present a solution where all 40 packages will be delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all trucks. The specific delivery locations are shown on the attached “Salt Lake City Downtown Map,” and distances to each location are given in the attached “WGUPS Distance Table.” The intent is to use the program for this specific location and also for many other cities in each state where WGU has a presence. As such, you will need to include detailed comments to make your code easy to follow and to justify the decisions you made while writing your scripts. 
   The supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the variables listed in the “WGUPS Package File,” including what has been delivered and at what time the delivery occurred.

**Assumptions** :
    Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
    The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
    There are no collisions.
    Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
    Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
    The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
    There is up to one special note associated with a package.
    The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
    The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
    The day ends when all 40 packages have been delivered.
  
**Course-provided files** :
    WGUPS Distance Table (.xlsx).
    WGUPS Package File (.xlsx).
    Salt Lake City Downtown Map (.docx).

# Project Objectives
    Implement a program that loads and delivers 40 packages using limited truck and driver resources
    
    Account for various delivery constraints including delays, deadlines, grouped deliveries, and incorrect addresses
    
    Use a custom-built hash table for efficient package management
    
    Simulate time and calculate accurate delivery timestamps for each package
    
    Ensure the total mileage does not exceed 140 miles
    
    Provide User Interface:    
        Delivery status of any package at any time
        Summary of total mileage
        Status of all trucks and their delivery progress
        
# Constraints and Assumptions
    Truck :
        Each truck can carry up to 16 packages.
        Each package has a unique ID number.
        Three trucks and two drivers are available:
        Only two trucks can be on the road at the same time.
        A driver stays with their assigned truck until all deliveries are completed.
        Trucks leave the hub no earlier than 8:00 AM, fully loaded.
        Trucks can return to the hub to pick up additional packages as needed.
        Delivery and loading are instantaneous.
        
    Time & Speed Assumptions :
        Trucks travel at an average speed of 18 miles per hour.
        No gas limitations — trucks do not need to refuel.
        No traffic or collisions are considered.
        The day ends when all 40 packages have been delivered.

    Package Constraints : 
        Delayed in transit, arrives at hub at 9:05 a.m.      (packages 6, 25, 28, 32)
        Packages that must be delivered together.            (packages 13, 14, 15, 16, 19, 20)
        Packages that must go on Truck 2.                    (packages 3, 18, 36, 38)
        Delivery deadline at 10:30 a.m.                      (packages 1, 6, 13, 14, 16, 20, 25, 29, 30, 31, 34, 40)
        Delivery deadline at 9:00 a.m.                       (package 15) 
        
    Package #9 :
        Has a known incorrect address at start time and can only be corrected at 10:20 AM:
            Before 10:20 AM, it cannot be delivered.
            After 10:20 AM, its correct address is:          (410 S. State St., Salt Lake City, UT 84111)

    Distance Table Assumptions :
        The “WGUPS Distance Table” provides distance in miles between each location.
        Distances are symmetric: the distance from A to B is the same as from B to A.
        Distances are rounded to nearest tenth of a mile and used to calculate travel times at 18 mph.

# Program Structure 
    Delivery_Project
    
    	|-Main.py                    (Entry point of the program and overall control flow)
    	|-CreateHashMap.py           (Implements the custom hash table used for efficient package lookup)          
    	|-Package.py                 (Handles package-related classes and methods)
    	|-Truck.py                   (Contains the data structures related to truck operations and delivery)
    	|-CSV
    	|	|-Address_File.csv
    	|	|-Distance_File.csv
    	|	|-Package_File.csv

# Data Sources and Extraction
    WGUPS Distance Table (.xlsx) :
        Converted to `CSV/Distance_File.csv`  
        Contains a symmetric matrix of distances between all delivery addresses  
        Used to calculate shortest paths between locations  
        Imported and parsed using the Python `csv` module
    
    WGUPS Package File (.xlsx) :
        Converted to `CSV/Package_File.csv`  
        Contains package IDs, addresses, deadlines, city/state/zip, weight, and special notes  
        Used to create package objects with proper constraints (e.g. delayed availability, truck assignment)  
        Loaded into a custom hash table for efficient lookup and status tracking
    
    Salt Lake City (.docx) :
        Downtown Map (used as visual reference, not directly parsed)









































    


