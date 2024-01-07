import pytest
import datetime
from reservation_system import Equipment, Reservation, ReservationSystem

def test_find_equipment_multi_phasic_radiation_scanner():
    rs = ReservationSystem()
    equipment = rs._find_equipment('multi-phasic radiation scanner')
    assert equipment.name == 'multi-phasic radiation scanner'

def test_find_equipment_ore_scooper():
    rs = ReservationSystem()
    equipment = rs._find_equipment('ore scooper')
    assert equipment.name == 'ore scooper'

def test_find_equipment_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    equipment = rs._find_equipment('1.21 gigawatt lightning harvester')
    assert equipment.name == '1.21 gigawatt lightning harvester'

def test_calculate_cost_multi_phasic_radiation_scanner():
    rs = ReservationSystem()
    equipment = Equipment('multi-phasic radiation scanner', 4, 990)
    start_time = datetime.datetime.now() + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(hours=2)
    cost = rs._calculate_cost(equipment, start_time, end_time)
    assert cost == 1980

def test_calculate_cost_ore_scooper():
    rs = ReservationSystem()
    equipment = Equipment('ore scooper', 8, 500)
    start_time = datetime.datetime.now() + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(hours=3)
    cost = rs._calculate_cost(equipment, start_time, end_time)
    assert cost == 1500

def test_calculate_cost_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    equipment = Equipment('1.21 gigawatt lightning harvester', 2, 3000)
    start_time = datetime.datetime.now() + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(hours=4)
    cost = rs._calculate_cost(equipment, start_time, end_time)
    assert cost == 18000

def test_check_availability_multi_phasic_radiation_scanner():
    rs = ReservationSystem()
    equipment = Equipment('multi-phasic radiation scanner', 4, 990)
    start_time = datetime.datetime.now() + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(hours=2)
    assert rs._check_availability(equipment, start_time, end_time) == True

def test_check_availability_ore_scooper():
    rs = ReservationSystem()
    equipment = Equipment('ore scooper', 8, 500)
    start_time = datetime.datetime.now() + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(hours=3)
    assert rs._check_availability(equipment, start_time, end_time) == True

def test_check_availability_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    equipment = Equipment('1.21 gigawatt lightning harvester', 2, 3000)
    start_time = datetime.datetime.now() + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(hours=4)
    assert rs._check_availability(equipment, start_time, end_time) == True

def test_make_reservation_ore_scooper():
    rs = ReservationSystem()
    reservation = rs.make_reservation(1, 'ore scooper', datetime.datetime.now() + datetime.timedelta(days=14), datetime.datetime.now() + datetime.timedelta(days=14, hours=5), 0, 0)
    assert isinstance(reservation, Reservation)

def test_cancel_reservation_ore_scooper():
    rs = ReservationSystem()
    reservation = rs.make_reservation(1, 'ore scooper', datetime.datetime.now() + datetime.timedelta(days=14), datetime.datetime.now() + datetime.timedelta(days=14, hours=5), 0, 0)
    refund = rs.cancel_reservation(reservation.reservation_id)
    assert refund == 125.0

def test_find_equipment_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    equipment = rs._find_equipment('1.21 gigawatt lightning harvester')
    assert equipment.name == '1.21 gigawatt lightning harvester'

def test_calculate_cost_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    equipment = Equipment('1.21 gigawatt lightning harvester', 1, 10000)
    start_time = datetime.datetime.now() + datetime.timedelta(days=30)
    end_time = start_time + datetime.timedelta(hours=12)
    cost = rs._calculate_cost(equipment, start_time, end_time)
    assert cost == 90000

def test_check_availability_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    equipment = Equipment('1.21 gigawatt lightning harvester', 1, 10000)
    start_time = datetime.datetime.now() + datetime.timedelta(days=30)
    end_time = start_time + datetime.timedelta(hours=12)
    assert rs._check_availability(equipment, start_time, end_time) == True

def test_make_reservation_1_21_gigawatt_lightning_harvester():
    rs = ReservationSystem()
    reservation = rs.make_reservation(1, '1.21 gigawatt lightning harvester', datetime.datetime.now() + datetime.timedelta(days=30), datetime.datetime.now() + datetime.timedelta(days=30, hours=12), 0, 0)
    assert isinstance(reservation, Reservation)

def test_cancel_reservation_ore_scooper():
    rs = ReservationSystem()
    reservation = rs.make_reservation(2, 'ore scooper', datetime.datetime.now() + datetime.timedelta(days=14), datetime.datetime.now() + datetime.timedelta(days=14, hours=5), 0, 0)
    refund = rs.cancel_reservation(reservation.reservation_id)
    assert refund == 1875