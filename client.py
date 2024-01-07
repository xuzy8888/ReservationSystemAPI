import datetime
import requests

"""
role         id    responsibility
scheduler    0     all function in system
customer     1     all function in system, for themselves only
admin        2     add or remove user, change their role
"""

VALID_ROLE = ["scheduler","customer","admin"]
class ReservationSystem:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/reservation/"
        self.login = False
        self.user_id = -1
        self.user_role = ""
        self.user_name = ""

    def check_input_date(self, date_string):
        try:
            date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD HH:MM format.")

    def print_reservations_from_json(self, r_json):
        print(r_json)
        print("id/username/firstname/equipment/start_time/end_time/total_cost/down_payment/location")
        res_list = r_json["message"]["reservations"]
        for res in res_list:
            if res["active"]:
                res_id = res["reservation_id"]
                user_name = res["username"]
                first_name = res["firstname"]
                equip = res["equipment"]
                active = res["active"]
                start_time = res["start_date"]
                end_time = res["end_date"]
                total_cost = res["cost"]
                down_payment = res["downpayment"]
                location = res["location"]
                print(res_id, "/", user_name, "/", first_name,"/",equip, "/", start_time, "/", end_time, "/", total_cost, "/",
                      down_payment, "/", location)

    def check_username(self, username):
        r = requests.get(self.url + "user?username=" + username)
        r_json = r.json()
        #print(r_json)
        if r_json["success"]:
            return True
        else:
            return False

    def check_reservation_id(self, reservation_id, user_name):
        r = requests.get(self.url + "access?reservation_id=" + reservation_id)
        r_json = r.json()
        if r_json["success"]:
            creator = r_json["username"][0][0]
            if creator == user_name:
                return True
        return False

    def main(self):
        while True:
            if not self.login:
                print("Thank you for using the reservation system, what would you like to do?")
                print("1. log in to the system")
                print("2. exit the program")
                choice = input("Enter your choice: ")

                if choice == "1":
                    self.user_login()
                elif choice == "2":
                    print("Exiting program")
                    break

            else:
                if self.user_role == "customer" or self.user_role == "scheduler":
                    print(f"Welcome {self.first_name}\n")
                    print("What would you like to do?")
                    print("1. Make a reservation")
                    print("2. Cancel a reservation")
                    print("3. List reservations within a date range")
                    print("4. List reservations within a date range, for specific customer")
                    print("5. List reservations within a given date range, for specific machine.")
                    print("6. List all reservations (Testing purpose, not part of the requirement):")
                    print("7. Log out")
                    print("8. Exit")
                    choice = input("Enter your choice: ")

                    # make a reservation
                    if choice == "1":
                        try:
                            self.make_reservation()
                        except KeyError:
                            print("access denied,you can not cancel this reservation")
                            continue
                        except ValueError:
                            print("Invalid Input")
                            continue

                    # cancel a request
                    elif choice == "2":
                        try:
                            self.cancel_reservation()
                        except PermissionError:
                            print("access denied,you can not cancel this reservation")
                            continue
                        except ValueError:
                            print("invalid input")
                            continue

                    # list all reservation between a start date and end date
                    elif choice == "3":
                        self.list_reservations_by_date()

                    # list all reservation between a start date and end date, for specific customer
                    elif choice == "4":
                        self.list_reservations_by_customer()

                    # list all reservation between a start date and end date, for specific machine
                    elif choice == "5":
                        self.list_reservations_by_machine()

                    # printing all reservations, for testing purpose
                    elif choice == "6":
                        self.print_all_reservations()

                    # log out
                    elif choice == "7":
                        self.user_logout()

                    # exit the system
                    elif choice == "8":
                        print("Exiting program")
                        break

                    else:
                        print("Invalid choice. Please try again.")

                elif self.user_role == "admin":
                    print(f"Welcome {self.first_name}\n")
                    print("What would you like to do?")
                    print("1. Add a user")
                    print("2. Remove a user")
                    print("3. Change users' role")
                    print("4. Log out")
                    print("5. Exit")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        try:
                            self.add_user()
                        except ValueError:
                            print("invalid input")
                            continue
                    elif choice == "2":
                        self.remove_user()
                    elif choice == "3":
                        try:
                            self.change_user()
                        except ValueError:
                            print("invalid input")
                            continue
                    elif choice == "4":
                        self.user_logout()
                    elif choice == "5":
                        print("Exiting program")
                        break
                    else:
                        print("Invalid choice. Please try again.")
                else:
                    print("user role does not exist")
                    break

    def user_login(self):
        input_username = input("Please enter your username:")
        r = requests.get(self.url + "user?username=" + input_username)
        r_json = r.json()
        print(r_json)
        if r_json["success"]:
            self.login = True
            self.user_id = int(r_json["id"])
            self.user_role = r_json["role"]
            self.user_name = r_json["username"]
            self.first_name = r_json["first_name"]
        else:
            print("The username is not registered, please try again")

    def make_reservation(self):
        # get user input and do basic validation
        name = self.user_name
        if self.user_role == "scheduler":
            name = input("Enter your username: ")
            if not self.check_username(name):
                print("The username does not exist")
                raise KeyError("The user is not registered")

        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(start_time)
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(end_time)
        x_coordinate = input("Enter x coordinate in the 20*20 grid:")
        if not x_coordinate.isnumeric() or int(x_coordinate) > 20 or int(x_coordinate) < 1:
            print("Please input a integer from 1 to 20")
            raise ValueError("Invalid location input")
        y_coordinate = input("Enter y coordinate in the 20*20 grid:")
        if not y_coordinate.isnumeric() or int(y_coordinate) > 20 or int(x_coordinate) < 1:
            print("Please input a integer from 1 to 20")
            raise ValueError("Invalid location input")

        equipment_name = ""
        machine_code = input(
            "enter machine's name \n 1 for ore scooper \n 2 for multi-phasic radiation scanner \n 3 for 1.21 "
            "gigawatt lightning harvester \n")
        if machine_code == "3":
            equipment_name = "1.21 gigawatt lightning harvester"
        elif machine_code == "2":
            equipment_name = "multi-phasic radiation scanner"
        elif machine_code == "1":
            equipment_name = "ore scooper"
        else:
            print("Invalid choice. Please try again")
            raise ValueError("Invalid machine code")
        r = requests.post(self.url + "post",
                          json={"user_name": name, "equipment_name": equipment_name, "start_time": start_time,
                                "end_time": end_time, "x_coor": x_coordinate, "y_coor": y_coordinate})

        # parse and print the response
        r_json = r.json()
        if r_json["success"]:
            print(r_json["message"])
        else:
            print("reservation failed")
            print(r_json["message"])

    def cancel_reservation(self):
        # get user input
        reservation_id = input("Enter reservation ID to cancel: ")

        if not reservation_id.isnumeric():
            print("Invalid reservation id")
            raise ValueError

        if self.user_role == "customer":
            if not self.check_reservation_id(reservation_id, self.user_name):
                raise PermissionError("You do not have access to the reservation")

        # send http delete request
        r = requests.delete(self.url + "cancel?id=" + reservation_id)

        # parse and print the response
        r_json = r.json()
        if r_json["success"]:
            print(r_json["message"])
            print("Your refund is: ", r_json["refund"])
        else:
            print("Unable to cancel your appointment.")
            print(r_json["message"])

    def list_reservations_by_date(self):
        """
        if scheduler(0) calls it, input start,end, then call api /reservation/getbytime
        if customer(1) calls it, input start,end, username is autofilled, then call api /reservation/getbyuser
        """
        # get user input and validate
        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(start_time)
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(end_time)

        if self.user_role == "customer":
            # make http get request
            payload = f"?start='{start_time}'&end='{end_time}'&user_name='{self.user_name}'"
            r = requests.get(self.url + "getbyuser" + payload)
        else:
            # make the http get request with query parameters
            params = f"?start='{start_time}'&end='{end_time}'"
            r = requests.get(self.url + "getbytime" + params)

        # parse and print the results
        r_json = r.json()
        if r_json["success"]:
            self.print_reservations_from_json(r_json)
        else:
            print("Can not find reservations")
            print(r_json["message"])

    def list_reservations_by_customer(self):
        """
        if scheduler(0) calls it, input username,start,end, then call api /reservation/getbyuser
        if customer(1) calls it, input start,end, username autofilled, then call api /reservation/getbyuser
        """

        name = self.user_name
        if self.user_role == "scheduler":
            name = input("Enter the username: ")

        # get and check user input
        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(start_time)
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(end_time)

        # make http get request
        payload = f"?start='{start_time}'&end='{end_time}'&user_name='{name}'"
        r = requests.get(self.url + "getbyuser" + payload)

        # parse and print the results
        r_json = r.json()
        if r_json["success"]:
            self.print_reservations_from_json(r_json)
        else:
            print("Can not find reservations")
            print(r_json["message"])

    def list_reservations_by_machine(self):
        """
        if scheduler(0) calls it, input start,end and machine name, username is blank, then call api /reservation/getbyequip
        if customer(1) calls it, input start,end and machine name, username is autofilled, then call api /reservation/getbyequip
        """
        # get and check user input
        machine_code = input(
            "enter machine's name \n 1 for ore scooper \n 2 for multi-phasic radiation scanner \n 3 for 1.21 "
            "gigawatt lightning harvester \n")
        if machine_code == "3":
            machine_name = "1.21 gigawatt lightning harvester"
        elif machine_code == "2":
            machine_name = "multi-phasic radiation scanner"
        elif machine_code == "1":
            machine_name = "ore scooper"
        else:
            print("Invalid choice. Please try again")
        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(start_time)
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
        self.check_input_date(end_time)

        name = ""
        if self.user_role == "customer":
            name = self.user_name

        # make http get request
        payload = f"?start='{start_time}'&end='{end_time}'&equipment_name='{machine_name}'&user_name='{name}'"
        r = requests.get(self.url + "getbyequip" + payload)

        # parse and print the results
        r_json = r.json()
        if r_json["success"]:
            self.print_reservations_from_json(r_json)
        else:
            print("Can not find reservations")
            print(r_json["message"])

    def print_all_reservations(self):
        print("Printing the reservations...")
        r = requests.get(self.url + "getall")
        if r.status_code == 200:
            self.print_reservations_from_json(r.json())
        else:
            print("Can not print reservations, please try again later")

    def add_user(self):
        user_name = input("Enter the username:")
        first_name = input("Input the user's firstname:")
        user_role = input("Enter the user's role:")
        if user_role not in VALID_ROLE:
            print("Invalid role to add")
            raise ValueError
        payload = f"?username='{user_name}'&role='{user_role}'&first_name='{first_name}'"
        r = requests.post(self.url + "user/adduser" + payload)

        # parse and print the results
        r_json = r.json()
        if r_json["success"]:
            print("sucessfully add the user")
        else:
            print("Can not add user")
            print(r_json["message"])

    def change_user(self):
        user_name = input("Enter the username:")
        user_role = input("Enter the user's role:")
        if user_role not in VALID_ROLE:
            print("Invalid role to add")
            raise ValueError
        payload = f"?username='{user_name}'&role='{user_role}'"
        r = requests.put(self.url + "user/changeuser" + payload)

        # parse and print the results
        r_json = r.json()
        if r_json["success"]:
            print("sucessfully change the role")
        else:
            print("Can not change role")
            print(r_json["message"])

    def remove_user(self):
        user_name = input("Enter the username:")
        payload = f"?username='{user_name}'"
        r = requests.delete(self.url + "user/deleteuser" + payload)

        # parse and print the results
        r_json = r.json()
        if r_json["success"]:
            print("sucessfully remove the user")
        else:
            print("Can not remove the user")
            print(r_json["message"])

    def user_logout(self):
        self.login = False
        self.user_id = -1
        self.user_role = ""
        self.user_name = ""
        print("You are logged out")


if __name__ == '__main__':
    reservation_system = ReservationSystem()
    reservation_system.main()
