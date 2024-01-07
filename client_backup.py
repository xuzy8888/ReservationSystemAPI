import datetime
import requests

"""
role         id    responsibility
scheduler    0     all function in system
customer     1     all function in system, for themselves only
admin        2     add or remove user, change their role
"""

# global variable for the url prefix, default to be local host
url = " http://127.0.0.1:8000/reservation/"

"""
Given a string of date and time, check if it follows the format
    
Parameters
----------
- date_string : string
string of date and time
    
Returns
-------
flag ValueError if the format of string is incorrect
"""


def check_input_date(date_string):
    try:
        date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD HH:MM format.")


"""
given a json object containing reservations, print it cleanly
    
Parameters
----------
- r_json : json
the json object parsed from the http response
    
Returns
-------
print the reservations to the terminal
"""


def print_reservations_from_json(r_json):
    print("id/customer/equipment/start_time/end_time/total_cost/down_payment/location")
    res_list = r_json["message"]
    for res in res_list:
        res_id = res["reservation_id"]
        customer_name = res["customer_id"]
        equip = res["equipment"]["name"]
        start_time = res["start_time"]
        end_time = res["end_time"]
        total_cost = res["total_cost"]
        down_payment = res["down_payment"]
        location = res["location"]
        print(res_id, "/", customer_name, "/", equip, "/", start_time, "/", end_time, "/", total_cost, "/",
              down_payment, "/", location)


def check_username(username):
    r = requests.get(url + "user?username=" + username)
    r_json = r.json()
    if r_json["success"]:
        return True
    else:
        return False


def check_reservation_id(reservation_id, user_name):
    r = requests.get(url + "?reservation_id=" + reservation_id)
    r_json = r.json()
    if r_json["success"]:
        if r_json["user_name"] == user_name:
            return True
    return False


def main():
    login = False
    user_id = -1
    user_role = -1
    user_name = ""
    while True:
        if not login:
            print("Thank you for using the reservation system, what would you like to do?")
            print("1. log in to the system")
            print("2. exit the program")
            choice = input("Enter your choice: ")

            if choice == "1":
                input_username = input("Please enter your username:")
                r = requests.get(url + "user?username=" + input_username)
                r_json = r.json()
                if r_json["success"]:
                    login = True
                    user_id = r_json["id"]
                    user_role = r_json["role"]
                    user_name = r_json["username"]
                else:
                    print("The username is not registered, please try again")

            elif choice == "2":
                print("Exiting program")
                break
        else:
            if user_role is 1 or 2:
                print("What would you like to do?")
                print("1. Make a reservation")
                print("2. Cancel a reservation")
                print("3. Reservations for given date range")
                print("4. For a given customer for a given date range, including the cost of the reservation.")
                print("5. List the current reservations for a given machine for a given date range.")
                print("6. List all reservations.")
                print("7. Log out")
                print("8. Exit")
                choice = input("Enter your choice: ")

                # make a reservation
                if choice == "1":
                    # get user input and do basic validation
                    name = user_name
                    if user_role is 0:
                        name = input("Enter your username: ")
                        if not check_username(name):
                            print("The username does not exist")
                            continue
                    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
                    check_input_date(start_time)
                    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
                    check_input_date(end_time)
                    x_coordinate = input("Enter x coordinate in the 20*20 grid:")
                    y_coordinate = input("Enter y coordinate in the 20*20 grid:")
                    equipment_name = input(
                        "Enter equipment name: \n 1.21 gigawatt lightning harvester\n multi-phasic radiation scanner\n ore "
                        "scooper\n")

                    # send http post request
                    r = requests.post(url + "post",
                                      json={"user_name": name, "equip_name": equipment_name, "start_time": start_time,
                                            "end_time": end_time, "x_coor": x_coordinate, "y_coor": y_coordinate})

                    # parse and print the response
                    r_json = r.json()
                    if r_json["success"]:
                        print(r_json["message"])
                    else:
                        print("reservation failed")
                        print(r_json["message"])

                # cancel a request
                elif choice == "2":

                    # get user input
                    reservation_id = input("Enter reservation ID to cancel: ")

                    if user_role is 1:
                        if not check_reservation_id(reservation_id, user_name):
                            print("access denied")
                            continue
                    # send http delete request
                    r = requests.delete(url + "cancel?id=" + reservation_id)

                    # parse and print the response
                    r_json = r.json()
                    if r_json["success"]:
                        print(r_json["message"])
                        print("Your refund is: ", r_json["refund"])
                    else:
                        print("Unable to cancel your appointment.")
                        print(r_json["message"])

                # list all reservation between a start date and end date
                elif choice == "3":

                    # get user input and validate
                    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
                    check_input_date(start_time)
                    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
                    check_input_date(end_time)

                    # make the http get request with query parameters
                    params = f"?start='{start_time}'&end='{end_time}'"
                    r = requests.get(url + "getbytime" + params)

                    # parse and print the results
                    r_json = r.json()
                    if r_json["success"]:
                        print_reservations_from_json(r_json)
                    else:
                        print("Can not find reservations")
                        print(r_json["message"])

                # list all reservation between a start date and end date, for specific customer
                elif choice == "4":

                    # get and check user input
                    customer_name = input("Enter customer name:")
                    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
                    check_input_date(start_time)
                    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
                    check_input_date(end_time)

                    # make http get request
                    payload = f"?start='{start_time}'&end='{end_time}'&user_name='{customer_name}'"
                    r = requests.get(url + "getbyuser" + payload)

                    # parse and print the results
                    r_json = r.json()
                    if r_json["success"]:
                        print_reservations_from_json(r_json)
                    else:
                        print("Can not find reservations")
                        print(r_json["message"])

                # list all reservation between a start date and end date, for specific machine
                elif choice == "5":

                    # get and check user input
                    machine_code = input(
                        "enter machine's name \n 1 for ore scooper \n 2 for multi-phasic radiation scanner \n 3 for 1.21 "
                        "gigawatt lightning harvester")
                    if machine_code == "3":
                        machine_name = "1.21 gigawatt lightning harvester"
                    elif machine_code == "2":
                        machine_name = "multi-phasic radiation scanner"
                    elif machine_code == "1":
                        machine_name = "ore scooper"
                    else:
                        print("Invalid choice. Please try again")
                    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
                    check_input_date(start_time)
                    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
                    check_input_date(end_time)

                    # make http get request
                    payload = f"?start='{start_time}'&end='{end_time}'&equip_name='{machine_name}'"
                    r = requests.get(url + "getbyequip" + payload)

                    # parse and print the results
                    r_json = r.json()
                    if r_json["success"]:
                        print_reservations_from_json(r_json)
                    else:
                        print("Can not find reservations")
                        print(r_json["message"])

                # printing all reservations, for testing purpose
                elif choice == "6":
                    print("printing the reservations...")
                    r = requests.get(url + "getall")
                    if r.status_code == 200:
                        print("id/customer/equipment/start_time/end_time/total_cost/down_payment/location")
                        r_json = r.json()
                        res_list = r_json["message"]
                        for res in res_list:
                            res_id = res["reservation_id"]
                            customer_name = res["customer_id"]
                            equip = res["equipment"]["name"]
                            start_time = res["start_time"]
                            end_time = res["end_time"]
                            total_cost = res["total_cost"]
                            down_payment = res["down_payment"]
                            location = res["location"]
                            print(res_id, "/", customer_name, "/", equip, "/", start_time, "/", end_time, "/",
                                  total_cost,
                                  "/",
                                  down_payment, "/", location)
                    else:
                        print("Can not print reservations, please try again later")

                # exit the system
                elif choice == "7":
                    login = False
                    user_id = -1
                    user_role = -1
                    user_name = ""
                    print("You are logged out")

                # exit the system
                elif choice == "8":
                    print("Exiting program")
                    break

                else:
                    print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
