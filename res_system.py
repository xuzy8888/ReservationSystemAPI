import datetime
from typing import List, Dict


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
        self._seed_reservations()

    def _seed_reservations(self):
        start_time1 = datetime.datetime(2023, 4, 14, 9, 0)
        end_time1 = datetime.datetime(2023, 4, 14, 12, 0)
        self.make_reservation('John', '1.21 gigawatt lightning harvester', start_time1, end_time1, 1, 4)

        start_time2 = datetime.datetime(2023, 4, 7, 10, 0)
        end_time2 = datetime.datetime(2023, 4, 7, 11, 0)
        self.make_reservation('Jane', 'multi-phasic radiation scanner', start_time2, end_time2, 2, 3)

        start_time2 = datetime.datetime(2023, 4, 7, 10, 0)
        end_time2 = datetime.datetime(2023, 4, 7, 11, 0)
        self.make_reservation('Abhi', 'multi-phasic radiation scanner', start_time2, end_time2, 7, 7)

        start_time2 = datetime.datetime(2023, 4, 7, 10, 0)
        end_time2 = datetime.datetime(2023, 4, 7, 11, 0)
        self.make_reservation('Pinky', 'multi-phasic radiation scanner', start_time2, end_time2, 8, 8)

    
        start_time2 = datetime.datetime(2023, 4, 8, 10, 0)
        end_time2 = datetime.datetime(2023, 4, 8, 11, 0)
        self.make_reservation('krishna', 'multi-phasic radiation scanner', start_time2, end_time2, 9, 9)

        start_time3 = datetime.datetime(2023, 4, 1, 11, 0)
        end_time3 = datetime.datetime(2023, 4, 1, 12, 0)
        self.make_reservation('Bob', 'ore scooper', start_time3, end_time3, 17, 18)

        start_time4 = datetime.datetime(2023, 4, 2, 10, 0)
        end_time4 = datetime.datetime(2023, 4, 2, 11, 0)
        self.make_reservation('Jane', 'ore scooper', start_time4, end_time4, 15, 15)

        start_time5 = datetime.datetime(2023, 4, 3, 9, 0)
        end_time5 = datetime.datetime(2023, 4, 3, 10, 0)
        self.make_reservation('Jane', '1.21 gigawatt lightning harvester', start_time5, end_time5, 10, 11)
    

    def _find_equipment(self, equipment_name):
        for equipment in self.equipment_list:
            if equipment.name == equipment_name:
                return equipment
        return None

    def _calculate_cost(self, equipment, start_time, end_time):
        if (start_time - datetime.datetime.now()).days < 14:
            reservation_duration = (end_time - start_time).seconds / 3600
            return reservation_duration * equipment.base_cost
        else:
            reservation_duration = (end_time - start_time).seconds / 3600
            return reservation_duration * equipment.base_cost * 0.75

    def _check_availability(self, equipment, start_time, end_time):
        overlapping_reservations = [
            r for r in self.reservations if r.equipment.name == equipment.name and
                                            not (r.end_time <= start_time or r.start_time >= end_time)
        ]

        if equipment.name == "multi-phasic radiation scanner":
            if len(self.reservations) == 0:
                return True

            # Check if harvester is in use during the specified time range
            harvester_in_use = False
            for reservation in self.reservations:
                if reservation.start_time <= end_time and reservation.end_time >= start_time:
                    if reservation.equipment.name == '1.21 gigawatt lightning harvester':
                        harvester_in_use = True
                        break

            # Check if more than 3 scanners are in use at any given time
            scanner_count = 0
            for reservation in self.reservations:
                if reservation.start_time <= end_time and reservation.end_time >= start_time:
                    if reservation.equipment.name == "multi-phasic radiation scanner":
                        scanner_count += 1
                        # print(scanner_count)
                        if scanner_count >= 3 or harvester_in_use:
                            return False

            return True

        if equipment.name == 'ore scooper':
            if len(overlapping_reservations) > 4:
                return False
            else:
                return True

        scanners_in_use = [
            r for r in self.reservations if r.equipment.name == "multi-phasic radiation scanner" and
                                            not (r.end_time <= start_time or r.start_time >= end_time)
        ]

        if scanners_in_use:
            return False
        else:
            return True

    def make_reservation(self, customer_id, equipment_name, start_time, end_time, x, y):
        # Find equipment by name
        # Check availability and constraints
        # Create a new reservation and add it to self.reservations
        # Calculate total cost and down payment cost
        equipment = self._find_equipment(equipment_name)
        if not equipment:
            raise ValueError("Invalid equipment name")

        if not self._check_availability(equipment, start_time, end_time):
            raise ValueError("Reservation not available")

        reservation_id = self.reservation_id_counter
        self.reservation_id_counter += 1

        total_cost = self._calculate_cost(equipment, start_time, end_time)
        down_payment = total_cost * 0.5
        reservation = Reservation(reservation_id, customer_id, equipment, start_time, end_time, total_cost,
                                  down_payment, x, y)
        self.reservations.append(reservation)

        # Return the reservation and the down_payment as a tuple
        return reservation

    def cancel_reservation(self, reservation_id: int) -> float:
        # Find reservation by reservation_id
        # Calculate refund amount based on cancel_time
        # Remove reservation from self.reservations
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
        return refund

    def list_reservations(self, start_date, end_date):
        return [r for r in self.reservations if r.start_time >= start_date and r.end_time <= end_date]

    def list_customer_reservations(self, customer_id, start_date, end_date):
        return [r for r in self.reservations if
                r.customer_id == customer_id and r.start_time >= start_date and r.end_time <= end_date]

    """
    def list_machine_reservations(self, equipment_name: str, start_date: datetime.datetime,
                                  end_date: datetime.datetime, user_name: str) -> List[Reservation]:
        if user_name == "":
            return [r for r in self.reservations if
                    r.equipment.name == equipment_name and r.start_time >= start_date and r.end_time <= end_date]
        else:
            return [r for r in self.reservations if
                    r.equipment.name == equipment_name and r.start_time >= start_date and r.end_time <= end_date and r.customer_id]
    """

    def list_machine_reservations(self, equipment_name: str, start_date: datetime.datetime,
                                  end_date: datetime.datetime) -> List[Reservation]:
        return [r for r in self.reservations if
                r.equipment.name == equipment_name and r.start_time >= start_date and r.end_time <= end_date]


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
    
    def list_all_reservations(self):
        return [r for r in self.reservations]
    # Additional utility functions for checking constraints and calculating costs



