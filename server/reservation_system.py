import datetime
from typing import List, Dict
import os


from db_utils import DBUtils

class Equipment:
    def __init__(self, name, availability, base_cost):
        self.name = name
        self.availability = availability
        self.base_cost = base_cost


class Reservation:
    def __init__(self, reservation_id: int, customer_id: int, equipment: Equipment, start_time: datetime.datetime,
                 end_time: datetime.datetime, total_cost: float, down_payment: float, x: int, y: int):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.equipment = equipment
        self.start_time = start_time
        self.end_time = end_time
        self.total_cost = total_cost
        self.down_payment = down_payment
        self.location = (x, y)

    def __str__(self) -> str:
        return f'{self.reservation_id}, {self.customer_id}, {self.equipment.name}, {self.total_cost}, {self.down_payment} {self.start_time}, {self.end_time}, {self.location}'


class ReservationSystem:

    def __init__(self):
        self.equipment_list = [
            Equipment('multi-phasic radiation scanner', 4, 990),
            Equipment('ore scooper', 4, 1000),
            Equipment('1.21 gigawatt lightning harvester', 1, 88000)
        ]
        self.reservations: List[Reservation] = []
        self.reservation_id_counter = 1
        self.cancelled_reservations: List[Reservation] = []
        self.db_setup()
    
    def db_setup(self):
        """Stand up database, set up tables and seed data"""

        self.db = DBUtils('reservation_system.db')

        create_db = os.path.join(os.path.dirname(__file__), 'create_db.sql')
        self.db.execute_script(create_db)

        seed_data = os.path.join(os.path.dirname(__file__), 'seed_db.sql')
        self.db.execute_script(seed_data)


    # Can be removed
    def _find_equipment(self, equipment_name):
        for equipment in self.equipment_list:
            if equipment.name == equipment_name:
                return equipment
        return None

    def _calculate_cost(self, equipment, start_time, end_time):
        # if (start_time - datetime.datetime.now()).days < 14:
        #     reservation_duration = (end_time - start_time).seconds / 3600
        #     return reservation_duration * equipment.base_cost
        # else:
        #     reservation_duration = (end_time - start_time).seconds / 3600
        #     return reservation_duration * equipment.base_cost * 0.75
        
        discount = 1
        if (start_time - datetime.datetime.now()).days >= 14:
            discount = 0.75
        
        reservation_duration = (end_time - start_time).seconds / 3600

        
        equipment_cost = self.db.select('machines', 'cost', f"""machine = '{equipment}' """)[0][0]
        
        return reservation_duration*equipment_cost*discount        
        
        

    # TODO: get from db
    def _check_availability(self, equipment, start_time, end_time):
        # overlapping_reservations = [
        #     r for r in self.reservations if r.equipment.name == equipment.name and
        #                                     not (r.end_time <= start_time or r.start_time >= end_time)
        # ]


        # get number of machines with given equipment name in use during the specified time range
        overlapping_reservations = self.db.select('reservations', 'count(*)', f"""machine= '{equipment}'
        AND start_date >='{start_time}' 
        AND end_date <= '{end_time}'""")[0][0]
        
        print(overlapping_reservations)

        max_machines_available = self.db.select('machines', 'available', f"""machine = '{equipment}'""")[0][0]


        if overlapping_reservations >= max_machines_available:
            return False
        
        return True




        # if equipment.name == "multi-phasic radiation scanner":
        #     if len(self.reservations) == 0:
        #         return True

        #     # Check if harvester is in use during the specified time range
        #     harvester_in_use = False
        #     for reservation in self.reservations:
        #         if reservation.start_time <= end_time and reservation.end_time >= start_time:
        #             if reservation.equipment.name == '1.21 gigawatt lightning harvester':
        #                 harvester_in_use = True
        #                 break

        #     # Check if more than 3 scanners are in use at any given time
        #     scanner_count = 0
        #     for reservation in self.reservations:
        #         if reservation.start_time <= end_time and reservation.end_time >= start_time:
        #             if reservation.equipment.name == "multi-phasic radiation scanner":
        #                 scanner_count += 1
        #                 # print(scanner_count)
        #                 if scanner_count >= 3 or harvester_in_use:
        #                     return False

        #     return True

        # if equipment.name == 'ore scooper':
        #     if len(overlapping_reservations) > 4:
        #         return False
        #     else:
        #         return True

        # scanners_in_use = [
        #     r for r in self.reservations if r.equipment.name == "multi-phasic radiation scanner" and
        #                                     not (r.end_time <= start_time or r.start_time >= end_time)
        # ]

        # if scanners_in_use:
        #     return False
        # else:
        #     return True

    def make_reservation(self, customer_id, equipment_name, start_time, end_time, x, y):
        """Finds equipment by name, checks availability and constraints, creates a new reservation and adds it to the database, calculates total cost and down payment cost"""
        

        # Can be removed
        equipment = self._find_equipment(equipment_name)
        """
        if not equipment:
            raise ValueError("Invalid equipment name")

        if not self._check_availability(equipment, start_time, end_time):
            raise ValueError("Reservation not available")

        reservation_id = self.reservation_id_counter
        self.reservation_id_counter += 1"""

        # changed to equipment name b/c before it was an object
        total_cost = self._calculate_cost(equipment_name, start_time, end_time)
        down_payment = total_cost * 0.5
        
        """## REMOVE
        reservation = Reservation(reservation_id, customer_id, equipment, start_time, end_time, total_cost,
                                  down_payment, x, y)
        self.reservations.append(reservation)
        ## STOP REMOVE"""

        self.db.add_reservation(
            customer_id= customer_id, equipment= equipment_name, 
            start_date= start_time, end_date= end_time, cost=total_cost, 
            downpayment= down_payment, location=f'{x, y}')

        # Return the reservation and the down_payment as a tuple
        return down_payment

    def cancel_reservation(self, reservation_id: int) -> float:
        # Find reservation by reservation_id
        # Calculate refund amount based on cancel_time
        # Remove reservation from self.reservations
        """
        reservation = None
        for r in self.reservations:
            if r.reservation_id == reservation_id:
                reservation = r
                break

        if not reservation:
            raise ValueError("Reservation not found")

        days_difference = (reservation.start_time - datetime.datetime.now()).days
        if days_difference >= 7:
            refund = 0.75 * reservation.down_payment
        elif days_difference >= 2:
            refund = 0.50 * reservation.down_payment
        else:
            refund = 0

        self.reservations.remove(reservation)
        self.cancelled_reservations.append(reservation)
        """

        """DB STUFF"""

        # check if it exists
        if len(self.db.check_reservation(reservation_id)) == 0:
            # TODO: perhaps we shouldn't raise an error here
            raise ValueError("Reservation not found")

        # cancel & get refund
        downpayment, reservation_date = self.db.cancel_reservation(reservation_id)
        refund = self.calculate_refund(downpayment, reservation_date)

        return refund
    
    def calculate_refund(self, downpayment: int, reservation_date: datetime.datetime) -> float:
        days_difference = (reservation_date - datetime.datetime.now()).days
        if days_difference >= 7:
            refund = 0.75 * downpayment
        elif days_difference >= 2:
            refund = 0.50 * downpayment
        else:
            refund = 0
        return refund

    def list_reservations(self, start_date : datetime.datetime, end_date : datetime.datetime):
        
        res  = self.db.select("reservations", "*", f"start_date >= '{start_date}' AND end_date <= '{end_date}'")

        # TODO: make it print nicely

        for i in res:
            print(i)

        return res
        

    def list_customer_reservations(self, customer_id, start_date, end_date):
        
        res = self.db.select("reservations", "*", f"customer = '{customer_id}' AND start_date >= '{start_date}' AND end_date <= '{end_date}'")

        for i in res:
            print(i)

        # return [r for r in self.reservations if
        #         r.customer_id == customer_id and r.start_time >= start_date and r.end_time <= end_date]

    def list_machine_reservations(self, equipment_name: str, start_date: datetime.datetime,
                                  end_date: datetime.datetime):
        """Prints all reservations for a given machine within a given time period
        
        Parameters
        ----------
        equipment_name: str
            The name of the machine
        start_date: datetime.datetime
            The start date of the time period
        end_date: datetime.datetime
            The end date of the time period

        """
        
        res = self.db.select("reservations", "*", f"machine = '{equipment_name}' AND start_date >= '{start_date}' AND end_date <= '{end_date}'")

        for i in res:
            print(i)

        # return [r for r in self.reservations if
        #         r.equipment.name == equipment_name and r.start_time >= start_date and r.end_time <= end_date]

    def list_all_transactions(self, ):
        pass

    def list_financial_transactions(self, start_date: datetime.datetime, end_date: datetime.datetime) -> Dict[
        str, List]:
        transactions = {
            'reservations': [],
            'cancellations': [],
        }

        for r in self.reservations:
            if r.start_time >= start_date and r.end_time <= end_date:
                transactions['reservations'].append({
                    'reservation_id': r.reservation_id,
                    'customer_id': r.customer_id,
                    'equipment_name': r.equipment.name,
                    'start_time': r.start_time,
                    'end_time': r.end_time,
                    'cost': self._calculate_cost(r.equipment, r.start_time, r.end_time)
                })
        for r in self.cancelled_reservations:
            transactions["cancellations"].append({
                'reservation_id': r.reservation_id,
                'customer_id': r.customer_id,
                'equipment_name': r.equipment.name,
                'start_time': r.start_time,
                'end_time': r.end_time,
                'cost': self._calculate_cost(r.equipment, r.start_time, r.end_time)
            })

        return transactions

    # Additional utility functions for checking constraints and calculating costs



if __name__ == '__main__':
    R = ReservationSystem()

    R.make_reservation(1, '1.21 gigawatt lightning harvester', datetime.datetime(2023, 5, 1), datetime.datetime(2023, 5, 2), 0, 0)

    for result in R.db.show_reservations():
        print(result)

    av = R._check_availability('ore scooper', datetime.datetime(2023, 5, 1), datetime.datetime(2023, 5, 2))
    print(av)

    
    # print(R.cancel_reservation(64))

    # R.list_reservations(datetime.datetime(2018, 1, 1), datetime.datetime(2022, 1, 1))

    # R.list_customer_reservations('John Doe', datetime.datetime(2018, 1, 1), datetime.datetime(2022, 1, 1))

    # R.list_machine_reservations('1.21 gigawatt lightning harvester', datetime.datetime(2018, 1, 1), datetime.datetime(2022, 1, 1))