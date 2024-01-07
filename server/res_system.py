import datetime
import os
import logging
from server.db_utils import DBUtils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReservationSystem:

    def __init__(self):
        self.db_setup()

    def db_setup(self) -> None:
        """Stand up database, set up tables and seed data"""

        self.db = DBUtils('reservation_system.db')
        # create tables
        self.db.execute_script(os.path.join(os.path.dirname(__file__), 'create_db.sql'))
        # seed_data
        self.db.execute_script(os.path.join(os.path.dirname(__file__), 'seed_db.sql'))

    def _find_equipment(self, equipment_name: str) -> str:
        """Returns the equipment object if it exists, otherwise returns None
        
        Parameters
        ----------
        equipment_name: str
            - The name of the equipment
            
        Returns
        -------
        equipment: Equipment
            - The equipment object if it exists, otherwise None"""

        if self.db.select('machines', '*', f"""equipment = '{equipment_name}' """):
            return equipment_name
        return None

    def _calculate_cost(self, equipment: str, start_time: datetime.datetime, end_time: datetime.datetime) -> float:
        """Calculates the cost of a reservation
        
        Parameters
        ----------
        equipment: str
            - The equipment object
        start_time: datetime.datetime
            - The start time of the reservation
        end_time: datetime.datetime
            - The end time of the reservation
            
        Returns
        -------
        cost: float
            - The cost of the reservation"""

        discount = 1
        if (start_time - datetime.datetime.now()).days >= 14:
            discount = 0.75

        reservation_duration = (end_time - start_time).seconds / 3600

        equipment_cost = self.db.select('machines', 'cost', f"""equipment = '{equipment}' """)[0][0]

        return reservation_duration * equipment_cost * discount

    def _check_availability(self, equipment: str, start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
        """Checks if a equipment is available during a given time range
        
        Parameters
        ----------
        equipment: str
            - The equipment object
        start_time: datetime.datetime
            - The start time of the reservation
        end_time: datetime.datetime
            - The end time of the reservation
        
        Returns
        -------
        available: bool
            - True if the equipment is available, False otherwise"""

        query_parameters = f"""equipment= '{equipment}'
        AND start_date >='{start_time}' 
        AND end_date <= '{end_time}'"""
        overlapping_res = self.db.select('reservations', 'count(*)', query_parameters)
        overlapping_res = overlapping_res[0][0]

        max_machines_available = self.db.select('machines', 'available', f"""equipment = '{equipment}'""")[0][0]

        if overlapping_res >= max_machines_available:
            return False

        return True

    def make_reservation(self, customer_id: str, equipment_name: str, start_time: datetime.datetime,
                         end_time: datetime.datetime, x: str, y: str) -> float:
        """Makes a reservation for a given customer and returns the downpayment amount (50% of the total cost)
        
        Parameters
        ----------
        customer_id: int
            - The customer's id
        equipment_name: str
            - The name of the equipment
        start_time: datetime.datetime
            - The start time of the reservation
        end_time: datetime.datetime
            - The end time of the reservation
        x: str
            - The x coordinate of the location
        y: str
            - The y coordinate of the location
        
        Returns
        -------
        down_payment: float
            - The down payment for the reservation"""

        equipment = self._find_equipment(equipment_name)
        if not equipment:
            raise ValueError("Equipment not found")

        total_cost = self._calculate_cost(equipment_name, start_time, end_time)
        down_payment = total_cost * 0.5

        location_string = x + " " + y
        self.db.add_reservation(
            customer_id= customer_id, equipment= equipment_name, 
            start_date= start_time, end_date= end_time, cost=total_cost, 
            downpayment= down_payment, location=location_string)
        """
        location_string = "{" + x + "," + y + "}" 
        self.db.add_reservation(
            customer_id=customer_id, equipment=equipment_name,
            start_date=start_time, end_date=end_time, cost=total_cost,
            downpayment=down_payment, location=location_string)
        """
        return down_payment

    def cancel_reservation(self, reservation_id: int) -> float:
        """Cancels a reservation and returns the refund amount.
        
        Refund amount is calculated as follows:
        - 75% refund if cancelled 7 or more days before reservation
        - 50% refund if cancelled 2-6 days before reservation
        - No refund if cancelled less than 2 days before reservation
        
        Parameters
        ----------
        reservation_id: int
            - The id of the reservation to cancel
            
        Returns
        -------
        refund: float
            - The refund amount"""

        # check if it exists
        if len(self.db.check_reservation(reservation_id)) == 0:
            raise ValueError("Reservation not found")

        # cancel & get refund
        downpayment, reservation_date = self.db.cancel_reservation(reservation_id)
        refund = self._calculate_refund(downpayment, reservation_date)

        return refund

    def _calculate_refund(self, downpayment: int, reservation_date: datetime.datetime) -> float:
        """Calculates the refund amount for a given downpayment and reservation date
        
        Refund amount is calculated as follows:
        - 75% refund if cancelled 7 or more days before reservation
        - 50% refund if cancelled 2-6 days before reservation
        - No refund if cancelled less than 2 days before reservation
        
        Parameters
        ----------
        downpayment: int
            - The downpayment amount
        reservation_date: datetime.datetime
            - The date of the reservation
        
        Returns
        -------
        refund: float
            - The refund amount"""

        days_difference = (reservation_date - datetime.datetime.now()).days
        if days_difference >= 7:
            refund = 0.75 * downpayment
        elif days_difference >= 2:
            refund = 0.50 * downpayment
        else:
            refund = 0
        return refund

    def list_nicely(self, res: list) -> dict:
        """Returns a dictionary of reservations to help parse and show the user

        Dictory format:
        { "reservations": [ {
                    "reservation_id": 1,
                    "customer": 1,
                    "equipment": "Excavator",
                    "start_date": "2021-03-01 00:00:00",
                    "end_date": "2021-03-02 00:00:00",
                    "active": 1,
                    "cost": 1000.0,
                    "downpayment": 500.0,
                    "location": "(1, 1)"
                }, 
                ] }
                
        
        Parameters
        ----------
        res: list
            - The list of reservations to parse
        
        Returns
        -------
        reservations: dict
            - The dictionary of reservations"""

        reservations = {}
        rezos = []

        for i in res:
            reservation = {"reservation_id": i[0], "username": i[1], "firstname": i[2], "equipment": i[3],
                           "start_date": i[4], "end_date": i[5], "active": i[6], "cost": i[7], "downpayment": i[8],"location":i[9]}

            rezos.append(reservation)

        reservations["reservations"] = rezos

        return reservations

    def list_all_reservations(self) -> dict:
        """Queries the reservation database and returns a dictionary of all reservations

        Returns
        -------
        reservations: dict
            - The dictionary of reservations
        
        """

        logger.debug("list_all_reservations")

        res = self.db.select("reservations_view", "*")

        return self.list_nicely(res)

    def list_reservations(self, start_date: datetime.datetime, end_date: datetime.datetime) -> dict:
        """Queries the reservation database and returns a dictionary of reservations within a given time period
        
        Parameters
        ----------
        start_date: datetime.datetime
            - The start date of the time period
        end_date: datetime.datetime
            - The end date of the time period
        
        Returns
        -------
        reservations: dict
            - The dictionary of reservations"""

        res = self.db.select("reservations_view", "*", f"start_date >= '{start_date}' AND end_date <= '{end_date}'")

        return self.list_nicely(res)

    def list_customer_reservations(self, username: str, start_date: datetime.datetime,
                                   end_date: datetime.datetime) -> dict:
        """Queries the reservation database and returns a dictionary of reservations for a given customer within a given time period
        
        Parameters
        ----------
        username: str
            - The username of the customer
        start_date: datetime.datetime
            - The start date of the time period
        end_date: datetime.datetime
            - The end date of the time period
        
        Returns
        -------
        reservations: dict
            - The dictionary of reservations"""
        columns = "reservation_id, username, first_name, equipment, start_date, end_date, active, cost, downpayment, location"
        res = self.db.select("reservations_view", columns,
                             f"username = '{username}' AND start_date >= '{start_date}' AND end_date <= '{end_date}'")

        return self.list_nicely(res)

    def list_machine_reservations(self, equipment_name: str, start_date: datetime.datetime,
                                  end_date: datetime.datetime):
        """Queries the reservation database and returns a dictionary of reservations for a given equipment within a given time period
        
        Parameters
        ----------
        equipment_name: str
            - The name of the equipment
        start_date: datetime.datetime
            - The start date of the time period
        end_date: datetime.datetime
            - The end date of the time period
        
        Returns
        -------
        reservations: dict
            - The dictionary of reservations
        """

        if self._find_equipment(equipment_name) is None:
            return None

        logger.debug(" - list_machine_reservations")

        res = self.db.select("reservations_view", "*",
                             f"equipment = '{equipment_name}' AND start_date >= '{start_date}' AND end_date <= '{end_date}'")

        logger.debug(" - results:")
        for i in res:
            logger.debug(f" - {i}")

        return self.list_nicely(res)

    def remove_user(self, username: str) -> None:
        """Removes a user from the database
        
        Parameters
        ----------
        username: str
            - The username of the customer
        """
        print("to remove ", username)
        self.db.remove_user(username)

    def add_user(self, username: str, first_name: str, role: str) -> None:
        """Adds a user to the database
        
        Parameters
        ----------
        username: str
            - The username of the customer
        """
        self.db.add_user(username, first_name, role)

    def change_user_role(self, username: str, role: str) -> None:
        """Updates a user in the database
        
        Parameters
        ----------
        username: str
            - The username of the customer
        role: str
            - The new role of the user

        """
        self.db.change_user_role(username, role)

    def login_user(self, username: str) -> str:
        """Returns the user object if it exists, otherwise returns None
        
        Parameters
        ----------
        username: str
            - The username of the customer
            
        Returns
        -------
        user: User
            - The user object if it exists, otherwise None"""
        user_details = self.db.select('user_roles_view', '*', f"""username = '{username}' and active = 'TRUE' """)
        print(user_details)
        return user_details

    def _find_user(self, username: str) -> str:
        """Returns the user object if it exists, otherwise returns None
        
        Parameters
        ----------
        username: str
            - The username of the customer
            
        Returns
        -------
        user: User
            - The user object if it exists, otherwise None"""
        print(f"""username = '{username}' """)
        if self.db.select('users', '*', f"""username = '{username}' """):
            return username
        return None

    def list_all_users(self) -> dict:
        """Queries the user database and returns a dictionary of all users

        Returns
        -------
        users: dict
            - The dictionary of users
        
        """
        logger.debug("list_all_users")

        res = self.db.select("users", "*")
        users = {"users": []}
        for i in res:
            users["users"].append({"user_id": i[0], "username": i[1], "first_name": i[2], "active": i[3]})

            # users[i[0]] = users

        return users


if __name__ == '__main__':
    pass
