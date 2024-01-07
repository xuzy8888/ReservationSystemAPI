'api_service.py'

from fastapi import FastAPI, Request, Body
import datetime

from server.res_system import ReservationSystem as db_sys

app = FastAPI()
sys = db_sys()


@app.post("/reservation/post")
async def reserve_item(reservation: dict = Body(...)):
    """Given a machine type and datetime, calls the reservation method
    and returns a success message plus any errors
    
    Parameters
    ----------
    - reservation : json
        json containing start_time, end_time, user_name, equip_name, x_coor, y_coor
    
    Returns
    -------
    - json
        json containing success and message
    """

    details = reservation
    print(details)

    try:

        # convert start and end to datetime.datetime objects
        start = datetime.datetime.strptime(details["start_time"], "%Y-%m-%d %H:%M")
        end = datetime.datetime.strptime(details["end_time"], "%Y-%m-%d %H:%M")


        downpayment = sys.make_reservation(
            details["user_name"], 
            details["equipment_name"], 
            start, end,
            details["x_coor"], details["y_coor"])
        success = True
        message = f"Succesfully reserved the {details['equipment_name']} for {details['user_name']} from {start} to {end}. Downpayment is {downpayment}"

    except ValueError as e:
        success = False
        message = f"ERROR - {e}"
    return {"success": success, "message": message}


@app.get("/reservation/getall")
async def get_all_reservations():
    """Returns all reservations in the database

    Parameters
    ----------
    None

    Returns
    -------
    - json
        json containing success and message
    """
    try:
        reservations = sys.list_all_reservations()
        success = True
    except ValueError as e:
        success = False
        reservations = f"ERROR - {e}"
    return {"success": success, "message": reservations}


@app.delete("/reservation/cancel")
async def delete_reservation(id: int):
    """Given a reservation id, calls the cancel_reservation method
    
    Parameters
    ----------
    - id : int
        id of the reservation to be cancelled

    Returns
    -------
    - json
        json containing success, message and refund
    """
    try:
        refund = sys.cancel_reservation(id)
        success = True
        test_message = "Succesfully cancelled reservation"
    except ValueError as e:
        success = False
        test_message = f"ERROR - {e}"
        refund = 0
    return {"success": success, "message": test_message, "refund": refund}


@app.get("/reservation/getbytime")
async def get_reservations(start: str, end: str):
    """Given a start and end time, calls the list_reservations method
    
    start and end time must be in the format YYYY-MM-DD HH:MM
    
    Parameters
    ----------
    - start : str
        start time of the reservation
    - end : str
        end time of the reservation

    Returns
    -------
    - json
        json containing success and message
    """

    start = prep_datetime(start)
    end = prep_datetime(end)

    reservations = sys.list_reservations(start, end)
    return {"success": True, "message": reservations}


@app.get("/reservation/getbyuser")
async def get_customer_reservations(user_name, start, end):
    """Given a user name, start and end time, calls the list_customer_reservations method
    
    start and end time must be in the format YYYY-MM-DD HH:MM
    
    Parameters
    ----------
    - user_name : str
        name of the user
    - start : str
        start time of the reservation
    - end : str
        end time of the reservation

    Returns
    -------
    - json
        json containing success and message

    """

    start = prep_datetime(start)
    end = prep_datetime(end)

    reservations = sys.list_customer_reservations(user_name.strip("'"), start, end)

    return {"success": True, "message": reservations}


@app.get("/reservation/getbyequip")
async def get_machine_reservations(equipment_name, start, end):
    """Given a machine name, start and end time, calls the list_machine_reservations method

    start and end time must be in the format YYYY-MM-DD HH:MM
    
    Parameters
    ----------
    - equip_name : str
        name of the machine
    - start : str
        start time of the reservation
    - end : str
        end time of the reservation

    Returns
    -------
    - json
        json containing success and message

    """
    start = prep_datetime(start)
    end = prep_datetime(end)
    equipment_input = equipment_name.strip("'")
    equipment = sys._find_equipment(equipment_input)

    if equipment is None:
        return {"success": False, "message": f"Machine not found - user entered '{equipment_input}'"}

    reservations = sys.list_machine_reservations(equipment_name.strip("'"), start, end)

    return {"success": True, "message": reservations}

#TODO: @kanello to do this
@app.get("/reservation/user")
async def user_login(username):
    """Check that the user name exists and return the first_name and user_role"""
    username_input = username.strip("'")

    # return user roles with numbers 0, 1,2
    user = sys.login_user(username_input)
    if user :
        user=user[0]
        print(user)
        return {"success": True, "id": user[0], "role": user[4], "username": username, "first_name": user[2]}
    
    return {"success": False, "message": f"User not found - user entered '{username_input}'"}
    


#TODO: @kanello to do this
@app.get("/reservation/access")
async def confirm_access(reservation_id):
    """Check that this user is the reservation owner"""
    reservation_id_input = reservation_id.strip("'")

    username = sys.db.select("reservations_view", "username", f"reservation_id = {reservation_id_input}")

    if username is None:
        return {"success": False, "message": f"Reservation not found - user entered '{reservation_id_input}'"}


    return {"success": True, "username": username}


@app.post("/reservation/user/adduser")
async def add_user(username, first_name, role):
    """
    add new user with username = username , user_role = role
    """
    username_input = username.strip("'")
    first_name_input = first_name.strip("'")
    role_input = role.strip("'")

    sys.add_user(username_input, first_name_input, role_input)

    return {"success": True, "message": f"User {username_input} added"}


@app.put("/reservation/user/changeuser")
async def change_user_role(username, role):
    """
    change existed user with username = username to have user_role = role
    """
    username_input = username.strip("'")
    role_input = role.strip("'")

    # check if user exists
    if sys._find_user(username_input) is None:
        return {"success": False, "message": f"User not found - user entered '{username_input}'"}
    
    sys.change_user_role(username_input, role_input)

    return {"success": True, "message": f"User {username_input} changed to {role_input}"}


@app.delete("/reservation/user/deleteuser")
async def remove_user(username):
    """
    remove the user with username=username from the database
    """
    
    username_input = username.strip("'")

    # check if user exists
    if sys._find_user(username_input) is None:
        return {"success": False, "message": f"User not found - user entered '{username_input}'"}
    

    sys.remove_user(username_input)

    return {"success": True, "message": f"User {username_input} removed"}

@app.get("/reservation/user/getall")
async def get_all_users():
    """
    get all users from the database
    """
    users = sys.list_all_users()

    return {"success": True, "message": users}

def prep_datetime(date_time):
    return datetime.datetime.strptime(date_time.strip("'"), "%Y-%m-%d %H:%M")
