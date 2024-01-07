## Team AlphaGo

## Code explanation

The code implements a reservation system that allows users to reserve equipment for a specified period. The reservation system has three types of equipment: multi-phasic radiation scanner, ore scooper, and 1.21 gigawatt lightning harvester. The code also calculates the total cost of the reservation based on the equipment's base cost and the duration of the reservation. The reservation system checks the availability of the equipment and takes into account specific constraints based on the equipment type. If the reservation is canceled, the system calculates the refund amount based on the number of days until the start of the reservation.

The system has three classes:

1. `Equipment`: represents the equipment that can be reserved. It has three attributes: `name` (str), `availability` (int), and `base_cost` (float).
2. `Reservation`: represents a reservation. It has eight attributes: `reservation_id` (int), `customer_id` (int), `equipment` (an instance of the `Equipment` class), `start_time` (a `datetime.datetime` object), `end_time` (a `datetime.datetime` object), `total_cost` (float), `down_payment` (float), and `location` (a tuple of two integers).
3. `ReservationSystem`: represents the reservation system. It has four attributes: `equipment_list` (a list of instances of the `Equipment` class), `reservations` (a list of instances of the `Reservation` class), `reservation_id_counter` (int), and `cancelled_reservations` (a list of instances of the `Reservation` class).

The `ReservationSystem` class has five methods:

1. `_find_equipment`: a helper method that finds an instance of the `Equipment` class by its name. If the equipment is not found, the method returns `None`.
2. `_calculate_cost`: a helper method that calculates the total cost of a reservation based on the equipment's base cost and the duration of the reservation. If the reservation is made less than 14 days in advance, the cost is not discounted. If the reservation is made 14 or more days in advance, the cost is discounted by 25%.
3. `_check_availability`: a helper method that checks if the equipment is available for the specified period and takes into account specific constraints based on the equipment type.
4. `make_reservation`: a method that allows users to make a reservation. The method takes a customer ID, equipment name, start time, end time, and location (x and y coordinates) as input. The method finds an instance of the `Equipment` class by its name and checks if it is available. If the equipment is available, the method creates a new instance of the `Reservation` class and adds it to the `reservations` list. The method returns the reservation and the down payment as a tuple.
5. `cancel_reservation`: a method that allows users to cancel a reservation. The method takes a reservation ID as input and calculates the refund amount based on the number of days until the start of the reservation. The method removes the reservation from the `reservations` list and adds it to the `cancelled_reservations` list. The method returns the refund amount.

### Source Code Management Strategy

- Developers pull from main branch, work on a feature branch, and push to main branch.
- Push directly

### Issues

- We tried to implement a persistence mechanism using sqlite. The file still exists in `server/assignment1.py` but it is not used in the system
- When testing locally within the file system, it all worked ok
- Introducing FastAPI introduced some issues with threading and sqlite. The threads couldn't properly communicate with the database
- We weren't able to find a solution for this and reverted to using a list of reservations in memory
