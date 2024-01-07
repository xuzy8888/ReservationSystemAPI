Hey team, I figured this would be easier to just put all my 
comments in one readme file rather than commenting on specific commits

1) ```python
   @app.get("/reservation/getall")
    def get_all_reservations():
    """Returns all reservations in the database

    Parameters
    ----------
    None

    Returns
    -------
    - json
        json containing success and message
    """
    reservations = sys.list_all_reservations()
    return {"success": True, "message": reservations}
Most of your other api routes have try/except blocks in them for api errors,
should probably have that here too. What if the response
that gets assigned to `reservations` is some error message from the system,
then you'd get a response like `{"success": True, "message": "internal server error"}`
which would be confusing.

2) ```def check_input_date(date_string):
    try:
        date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD HH:MM format.")
If you just want to check that the date_string is convertable to a date object, leave the variable out.
date_object isn't actually used or returned in this function, so no need to assign it. You can just do
```python
def check_input_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD HH:MM format.")
```

3) `server/reservation_system.py` is missing docstrings and has a lot of commented out code, please remove big blocks like that before submitting.