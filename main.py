#-----------------------------------------
#Developer: Arun Rai
#Project Name: Path Finder Pro        
#-----------------------------------------

import csv
import math
import datetime as othertime
import sys
import re
import os
from datetime import datetime

#self adjusting hash table data structure that stores the packages without using any external libraries
class packageHashTable:
    #initializes the hash table with 10 slots
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
    
    #Method to search for a package based on a key
    def search(self,key):
    
        #Calculate the bucket index for the given key
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        #Iterate through the key-value pairs in the bucket
        for kv in bucket_list:
          if kv[0] == key:
            return kv[1] 
        return None
        
    #Method to insert a new key-value pair or update an existing pair
    def insert(self, key, package):    
    
        #Calculate the bucket index for the given key
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        #Iterate through the key-value pairs in the bucket
        for kv in bucket_list:
          if kv[0] == key:
            kv[1] = package #Update the package value if the key exists
            return True
        
        #If the key does not exist in the bucket, create a new key-value pair
        key_value = [key, package]
        bucket_list.append(key_value)
        return True    
    
    


class Truck:
    #Constructor to initialize truck class
    def __init__(self, ID, current_address,time_left_hub,latest_time_stamp):
        self.ID = ID
        self.packages = []
        self.current_address = current_address
        self.time_left_hub = time_left_hub
        self.latest_time_stamp = latest_time_stamp
        self.distance_traveled = 0
    #Method used to load packages on truck at the beginning of program
    def loadPackage(self, package):
        self.packages.append(package)
     
        
    



class Package:
    #Constructor to initialize package class
    def __init__(self, ID, deliveryAddress, deliveryDeadLine, deliveryCity, deliveryZipcode, packageWeight, status):
        self.ID = ID
        self.deliveryAddress = deliveryAddress
        self.deliveryDeadLine = deliveryDeadLine
        self.deliveryCity = deliveryCity
        self.deliveryZipcode = deliveryZipcode
        self.packageWeight = packageWeight
        self.status = status
    #Returns a string representation of the package information
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.ID, self.deliveryAddress, self.deliveryDeadLine, self.deliveryCity, self.deliveryZipcode, self.packageWeight, self.status)  
        
        



#This method is used to extract the package information from the package.csv file that is provided with this project   
def importPackageFromCSV(nameofcsv):
    global packageTable
    #opens csv
    with open(nameofcsv) as theCsv:
        packages = csv.reader(theCsv, delimiter=',')
        #iterates through each line of the csv and collects data from specific columns
        for package in packages:
            packageID = int(package[0])
            deliveryAddress = package[1]
            deliveryDeadLine= package[5]
            deliveryCity = package[2]
            deliveryZipcode = package[4]
            packageWeight = package[6]
            status = "at the hub"
           
            #data from each row is turned into a package class and passed in the hash table data structure for storage
            newPackage = Package(packageID, deliveryAddress, deliveryDeadLine, deliveryCity, deliveryZipcode, packageWeight, status)

            packageTable.insert(packageID, newPackage)
            
#This method is used to extract the address information from the address.csv file that is provided with this project   
def importAddressFromCSV(nameofcsv):
    global addressData
    #opens csv
    with open(nameofcsv) as theCsv:
        locations = csv.reader(theCsv, delimiter=',')
        #iterates through each line of the csv and collects data from specific column
        for location in locations:
            #passes data from each row into global array that stores all addresses
            addressData.append(location[2])
            

#This method is used to extract the distance information between each address from the distance.csv file that is provided with this project               
def importDistanceFromCSV(nameofcsv):
    global distance_list
    #opens csv
    with open(nameofcsv) as theCsv:
        counter = 0
        location_distances = csv.reader(theCsv, delimiter=',')
        #Iterates through each line in csv and collects data from specifc column
        for location_distance in location_distances:
            temp_list = []
            length = counter + 1
            #Iterates through each column for current row and adds all populated columns to an array. This gets all the distances from each address that correspond to the address for that row.
            for i in range(length):
              temp_list.append(float(location_distance[i]))
            distance_list.append(temp_list)      
            counter = counter + 1

#This method is called when nearest neighbor algorithm is being run and is calculating the distance between the current address and each other possible address to go next. Accepts current address, and potentail next address.
def distanceFrom(address1, address2):
    global addressData
    global distance_list
    #since it is a 2d array and distance between two addresses is not duplicated will have to check which array the distance is stored in. For example the distance between "300 State St" and "410 State St" might be stored in the "300 State St" array or the "410 State St" array. But not both.
    try:
      d = distance_list[addressData.index(address1)][addressData.index(address2)]
    except:
      d = distance_list[addressData.index(address2)][addressData.index(address1)]
    return d 

#After nearest neighbor algorithm complete and closest address is found. This method is ran and the package is delivered. 
def deliver_package(address,truck,distance):
    count = 0
    #Iterates all packages and selects all packages associated with that address, since may be more than one
    for package in truck.packages:
      if package.deliveryAddress == address:
        time_in_hours = distance / 18
        time_obj = othertime.timedelta(hours=time_in_hours)        
        if count < 1:
            #Update time stamp on truck
            truck.latest_time_stamp = truck.latest_time_stamp + time_obj
        count = count + 1
        #Update status of package
        package.status = "Delivered (" + truck.latest_time_stamp.strftime("%I:%M:%S %p") +  ")"
        print("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), str(package.status), package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))
        
        

#Method used to load packages on truck at the beginning of program
def loadTruck(truck,ListOfpackages):
    for package in ListOfpackages:
        truck.loadPackage(packageTable.search(package))



#Core logic where nearest neighbor algorithm is run
def deliverpackagesforTruck(truck):
    truck_drop_offs = []
    already_dropped_off = []
    
    #Iterates through all packages on selected truck and removes duplicate address. 
    for package in truck.packages:
        if package.deliveryAddress not in truck_drop_offs:
            truck_drop_offs.append(package.deliveryAddress)

    #Iterates through all addresses truck has to visit.
    for i in truck_drop_offs:

        lowest_distance = 9999999
        #iterates through all possible address locations to travel to next from current address
        for address in truck_drop_offs:
        
            #Stores minimum distance, excluding current address and places already visited
            if address != truck.current_address and address not in already_dropped_off:
              distance = distanceFrom(truck.current_address,address)
              if distance < lowest_distance:
                lowest_distance = distance
                lowest_distance_address = address
        
        #After finding minimum distance from current address values are updated and truck deliver package to that address
        truck.distance_traveled = truck.distance_traveled + lowest_distance
        already_dropped_off.append(lowest_distance_address)
        deliver_package(lowest_distance_address,truck,lowest_distance)
        truck.current_address = lowest_distance_address
    #After all locations have been iterated through that means all packages have been delivered. Now  the truck will drive back to the hub
    driveBackToHub(truck)


#Method used when all packages are delivered for truck and time to drive back to hub.
def driveBackToHub(truck):
    global hub_address
    #Updates values like distance traveled and trucks timestamp
    distance_back_to_hub = distanceFrom(truck.current_address, hub_address)
    truck.distance_traveled = truck.distance_traveled + distance_back_to_hub
    time_in_hours = distance_back_to_hub / 18
    time_obj = othertime.timedelta(hours=time_in_hours)        
    truck.latest_time_stamp = truck.latest_time_stamp + time_obj
            

  
#This method is ran when simulation begins
def startProgram():

    print("\n------------------Running simulation------------------\n")

    #intialize all varaibles
    global packageTable
    global distance_list
    global addressData
    global trucklist
    global hub_address
    global error_address_corrected_timestamp
    hub_address = "4001 South 700 East"
    start_time1 = datetime.strptime("08:00:00 AM", "%I:%M:%S %p")
    start_time2 = datetime.strptime("09:05:00 AM", "%I:%M:%S %p")
    error_address_corrected_timestamp = datetime.strptime("10:20:00 AM", "%I:%M:%S %p")
    distance_list = []
    addressData = []
    packageTable = packageHashTable()

    #create three truck objects
    truck1 = Truck(1,"4001 South 700 East",start_time1,start_time1)
    truck2 = Truck(2,"4001 South 700 East",start_time2,start_time2)
    truck3 = Truck(3,"4001 South 700 East",start_time1,start_time1)


    trucklist = [truck1,truck2,truck3]

    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file paths relative to the script directory using os.path.join
    package_csv_path = os.path.join(script_directory, "data", "packageCSV.csv")
    address_csv_path = os.path.join(script_directory, "data", "addressCSV.csv")
    distance_csv_path = os.path.join(script_directory, "data", "distanceCSV.csv")
    
    # Use the constructed file paths in your functions
    importPackageFromCSV(package_csv_path)
    importAddressFromCSV(address_csv_path)
    importDistanceFromCSV(distance_csv_path)
    
    #create lists of which truck each package will be assigned to
    truck1packagelist = [1, 15, 13, 14, 16, 19, 29, 20, 31, 34, 37]
    truck2packagelist = [3, 6, 25, 28, 32, 36, 38, 18, 30, 35, 40]
    truck3packagelist = [9, 2, 4, 5, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33, 39]

    #Load the assigned packages on the truck
    loadTruck(truck1,truck1packagelist)
    loadTruck(truck2,truck2packagelist)
    loadTruck(truck3,truck3packagelist)


    #deliver packages for each truck
    print("\n--------------\nTruck 1\n--------------\n")
    deliverpackagesforTruck(truck1)
    print("\n--------------\nTruck 2\n--------------\n")
    deliverpackagesforTruck(truck2)

    #These conditional statements check what time truck 3 should leave. Since one of the drivers from truck 1 and 2 have to be back at the hub as well as the GPS has to be corrected with the correct address for package 9.
    if truck1.latest_time_stamp <= truck2.latest_time_stamp and truck1.latest_time_stamp > error_address_corrected_timestamp:
        truck3.latest_time_stamp = truck1.latest_time_stamp
        truck3.time_left_hub = truck1.latest_time_stamp
        correctAddressPackage9(truck3)
        print("\n--------------\nTruck 3\n--------------\n")
        deliverpackagesforTruck(truck3)
    elif truck2.latest_time_stamp < truck1.latest_time_stamp and truck2.latest_time_stamp > error_address_corrected_timestamp:
        truck3.latest_time_stamp = truck2.latest_time_stamp
        truck3.time_left_hub = truck2.latest_time_stamp
        correctAddressPackage9(truck3)
        print("\n--------------\nTruck 3\n--------------\n")
        deliverpackagesforTruck(truck3)
    else:
        truck3.latest_time_stamp = error_address_corrected_timestamp
        truck3.time_left_hub = error_address_corrected_timestamp
        correctAddressPackage9(truck3)        
        print("\n--------------\nTruck 3\n--------------\n")
        deliverpackagesforTruck(truck3)        
        
        
    #Prints the results for distance traveled for each truck, and all trucks combined    
    print("\n\n------------------Distance Traveled------------------\n")    
    print("All Trucks: " + str(truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled) + "\n")
    print("Truck 1: " + str(truck1.distance_traveled))
    print("Truck 2: " + str(truck2.distance_traveled))
    print("Truck 3: " + str(truck3.distance_traveled) + "\n\n\n")
    
    #Displays options to user when simulation is complete
    runQuestion2()
        
#This method is ran before truck 3 goes out for delivery and needs to update package ID 9 with correct address
def correctAddressPackage9(truck):
    for package in truck.packages:
        if package.ID == 9:
            package.deliveryAddress = "410 S State St"        
     
#First thing that is displayed to user. Easy to use user interface from command line
def runQuestion1():
    #Displays options and accpets user input
    answer = input("\n\nWelocome to the PathFinderPro delivery simulation! Please choose one of the options below by typing the letter next to that option.\n\nr - run simulation\nq - quit\n\n>")
    if answer == "r":
        startProgram()
    elif answer == "q":
        print("Program ended.")
        sys.exit()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again")
        runQuestion1()
        
#This question acts as the main menu, and is run after simulation or other options are selected. Contains all the functions the program can do.      
def runQuestion2():
    answer = input("\n\nWhat would like to  do next? Please choose one of the options below by typing the letter next to that option.\n\na - Status of all packages at a specifc time\nb - Status of a specifc package at a specifc time\nc - Run simulation again\nq - Quit\n\n>")
    if answer == "a":
        allPackagesSpecifcTime()
    elif answer == "b":
        specifcPackageSpecificTime()
    elif answer == "c":
        startProgram()
    elif answer == "q":
        print("Program ended.")
        sys.exit()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again")
        runQuestion2()

#This method is ran after a user selects to view status of all packages at a specifc time. They will input a time and program will return status for all packages at that time.        
def allPackagesSpecifcTime():
    global trucklist
    global error_address_corrected_timestamp
    display_list = []
    time_pattern = r"\d{2}:\d{2}:\d{2} [AP]M"
    #allow user to input time
    answer = input("\n\nEnter a time. Program will display status for all packages at that given time.(Or type \"r\" to return to menu)\n\nFormat examples:\n\"07:00:00 AM\"\n\"01:00:00 PM\"\n\n>")
    #check if time inputted matches desired format
    if re.match(time_pattern, answer):
        #Iterate through all packages for all trucks
        for truck in trucklist:
            for package in truck.packages:
            
                time = datetime.strptime(answer, "%I:%M:%S %p")                
                match = re.search(r'\((.*?)\)', package.status)
                time_delivered_t = match.group(1)       
                time_delivered = datetime.strptime(time_delivered_t, "%I:%M:%S %p")
                
                #special operations have to take place for package 9 since address is different depending on what time the user inputs.
                if package.ID == 9:
                    if time < error_address_corrected_timestamp:
                        package.deliveryAddress = "300 State St"
                    else:
                        package.deliveryAddress = "410 S State St"        
                
                #Core logic that determines what the status of current package was at inputted time. If time delivered is less than time inputted, than package was
                #delivered. If time delivered is after time inputted but time truck for that package left hub was before time inputted than that mean its "En Route". Else it is "At the Hub" Since truck hasent left yet
                if time_delivered <= time:
                    display_list.append("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), str(package.status), package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))
                elif truck.time_left_hub <= time and time_delivered > time:
                    display_list.append("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), "En Route", package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))
                else:
                    display_list.append("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), "At the hub", package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))
                    
        #orgainze the prints in order by package ID
        display_list.sort(key=lambda x: int(re.search(r'ID:\s*(\d+)', x).group(1)))
        for item in display_list:
            print(item)
        #return to main menu
        runQuestion2()        
    
    #exceptions if user inputted something other than time
    elif answer == "r":
        runQuestion2()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again")
        allPackagesSpecifcTime()

#Method is ran after user wants to view status for specific packages at a specific time. First step is this method which collects time first than sends to "selectpackage" method which will determine what specific package.
def specifcPackageSpecificTime():
    time_pattern = r"\d{2}:\d{2}:\d{2} [AP]M"
    answer = input("\n\nEnter a time. Program will display status for a specifc package at that given time.(Or type \"r\" to return to menu)\n\nFormat examples:\n\"07:00:00 AM\"\n\"01:00:00 PM\"\n\n>")
    if re.match(time_pattern, answer):
        selectpackage(answer)

    elif answer == "r":
        runQuestion2()
    else:
        print("\n\nIm sorry I dont think I understood that. Please try and answer again")
        specifcPackageSpecificTime()

#This method is ran after user selects what time they would like to view the status for their specific package. This method will now let the user select what type of specific package they would like to view, then with all information gathered "logicForPrinting" method is called to execute the logic.
def selectpackage(time):
    global check_condition
    answer = input("\n\nSelect parameter to search package by(Or type \"r\" to return to menu). \n\na - package ID number\nb - delivery address\nc - delivery deadline\nd - delivery city\ne - delivery zip code\nf - package weight \ng - delivery status \n\n>")
    if answer == "a":
        check_condition = lambda package, answer: package.ID == int(answer)
        question_string = "\n\nPlease enter the Package ID number you would like to view the status of. (Or type \"r\" to return to menu)\n\n>"
        exception_string = "\n\nIm sorry I could not find any Packages with an ID that match your input. Please try and answer again. (This question only accepts integers as an answer)"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "b":
        check_condition = lambda package, answer: package.deliveryAddress == answer
        question_string = "\n\nPlease enter the Delivery Address for the package you would like to view the status of. (Or type \"r\" to return to menu)\n\n>" 
        exception_string = "\n\nIm sorry, I could not find any Packages with a Delivery Addresses that match your input. Please try again using these examples to help format (\"4001 South 700 East\",\"1060 Dalton Ave S\")"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "c":
        check_condition = lambda package, answer: package.deliveryDeadLine == answer
        question_string = "\n\nPlease enter the Delivery Dealine for the package you would like to view the status of. (Or type \"r\" to return to menu)\n\n>"
        exception_string = "\n\nIm sorry, I could not find any Packages with a Delivery Deadline that match your input. Note not to include seconds for this input. Please try again using these examples to help format (\"10:30 AM\",\"9:00 AM\", \"EOD\")"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "d":
        check_condition = lambda package, answer: package.deliveryCity == answer
        question_string = "\n\nPlease enter the City for the Package you would like to view the status of. (Or type \"r\" to return to menu)\n\n>"
        exception_string = "\n\nIm sorry, I could not find any Packages with a City that match your input. Please try again using these examples to help format (\"Salt Lake City\",\"Murray\", \"Holladay\")"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "e":
        check_condition = lambda package, answer: package.deliveryZipcode == answer
        question_string =  "\n\nPlease enter the Zip Code for the Package you would like to view the status of. (Or type \"r\" to return to menu)\n\n>"
        exception_string = "\n\nIm sorry, I could not find any Packages with a Zip Code that match your input. Please try again using these examples to help format (\"84119\",\"84117\", \"84104\")"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "f":
        check_condition = lambda package, answer: package.packageWeight == answer
        question_string = "\n\nPlease enter the Weight (Mass Kilo) for the Package you would like to view the status of. (Or type \"r\" to return to menu)\n\n>"
        exception_string = "\n\nIm sorry, I could not find any Packages with a Weight that match your input. Please try again using these examples to help format (\"22\",\"44\", \"1\")"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "g":
        check_condition = lambda package, answer: answer in ["Delivered", "En Route", "At the hub"]
        question_string = "\n\nPlease enter the Status for the Package you would like to view. (Or type \"r\" to return to menu)\n\n>"
        exception_string = "\n\nIm sorry, I could not find any Packages with a Status that match your input. Please try again using these examples to help format (\"Delivered\",\"En Route\", \"At the hub\")"
        logicForPrinting(question_string,exception_string,time)
    elif answer == "r":
      runQuestion2()
    else:
      print("\n\nIm sorry I dont think I understood that. Please try and answer again")
      selectpackage(time)
      




#This method is ran after user selects to view status of a specifc package at a specific time and all information has been gathered. Which are accepted as parameters for this method. Core logic happens here.
def logicForPrinting(question,exception,time):
    display_list = []
    found_match = "N"
    global error_address_corrected_timestamp
    global trucklist
    global check_condition
    
    #Displays appropiate questions for which question type user wanted. Such as "Input package ID number" or "Input package delivery address"
    answer = input(question)    
    
    #Iterate through all packages for all trucks
    for truck in trucklist:
        for package in truck.packages:
            
            condition_time = datetime.strptime(time, "%I:%M:%S %p")

            #special operations have to take place for package 9 since address is different depending on what time the user inputs.
            if package.ID == 9:
                if condition_time < error_address_corrected_timestamp:
                    package.deliveryAddress = "300 State St"
                else:
                    package.deliveryAddress = "410 S State St"            
            
            #This logic checks if current package matches the criteria user inputted for specifc package. Such as which package ID number or what package delivery address
            try:
                condition = check_condition(package, answer)
            except:
                condition = False
            
            #If packages matches criteria continue
            if condition:            
                found_match = "Y"
                object_time = datetime.strptime(time, "%I:%M:%S %p")                
                match = re.search(r'\((.*?)\)', package.status)
                time_delivered_t = match.group(1)       
                time_delivered = datetime.strptime(time_delivered_t, "%I:%M:%S %p")                
                
                #Core logic that determines what the status of current package was at inputted time. If time delivered is less than time inputted, than package was
                #delivered. If time delivered is after time inputted but time truck for that package left hub was before time inputted than that mean its "En Route". Else it is "At the Hub" Since truck hasent left yet                
                if time_delivered <= object_time:
                    #If user only wants to print packages with delivered status this logic handles that
                    if answer not in ["En Route", "At the hub"]:
                        display_list.append("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), str(package.status), package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))

                elif truck.time_left_hub <= object_time and time_delivered > object_time:
                    #If user only wants to print packages with "En Route" status this logic handles that
                    if answer not in ["Delivered", "At the hub"]:                    
                        display_list.append("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), "En Route", package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))

                else:
                    #If user only wants to print packages with "At the hub" status this logic handles that
                    if answer not in ["Delivered", "En Route"]:
                        display_list.append("ID: {:<3} Status: {:<30} Delivery Address: {:<40} Delivery Deadline: {:<10} Package City: {:<20} Delivery Zip Code: {:<10} Weight: {:<3}".format(str(package.ID), "At the hub", package.deliveryAddress, package.deliveryDeadLine, package.deliveryCity, str(package.deliveryZipcode), str(package.packageWeight)))

    #orgainze the prints in order by package ID
    display_list.sort(key=lambda x: int(re.search(r'ID:\s*(\d+)', x).group(1)))
    for item in display_list:
        print(item)
    #exception handling for bad inputs and returning to main menu     
    if found_match == "N" and answer != "r":
        print(exception)
        logicForPrinting(question,exception,time)
    elif found_match == "N" and answer == "r":
        runQuestion2()
    else:
        runQuestion2()




#--------------------
#start of the program
#--------------------

runQuestion1()



  























