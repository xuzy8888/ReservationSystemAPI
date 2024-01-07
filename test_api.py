import pytest
from httpx import AsyncClient
from api_service import app

base_url = "http://127.0.0.1:8000/reservation"

@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get('/getall')
    assert response.status_code == 200

    # we've seeded the system with reservations
    assert len(response.json()['message']) > 0 


@pytest.mark.asyncio
async def test_add_reservation_post():
    data = {
	"user_name": "anthony",
	"equipment_name": "1.21 gigawatt lightning harvester",
	"start_time": "2023-05-01 00:00:00",
	"end_time": "2023-05-02 00:00:00",
	"x_coor": 0,
	"y_coor": 0}

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/post", json=data)
    assert response.status_code == 200

    # it should return false because there is no machine named "ore"
    assert response.json()["success"] == False

@pytest.mark.asyncio
async def test_add_reservation_wrong_machine_name_post():
    data = {
	"user_name": "foo",
	"equipment_name": "ore",
	"start_time": "2023-05-01 00:00:00",
	"end_time": "2023-05-02 00:00:00",
	"x_coor": 0,
	"y_coor": 0}

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/post", json=data)
    assert response.status_code == 200

    # it should return false because there is no machine named "ore"
    assert response.json()["success"] == False

@pytest.mark.asyncio
async def test_get_by_equip():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("getbyequip?start='2020-01-01 00:00'&end='2024-01-01 00:00'&equipment_name='ore scooper'")
    assert response.status_code == 200

    # we've seeded the system with reservations
    assert len(response.json()['message']['reservations']) > 0 

@pytest.mark.asyncio
async def test_get_by_user():
    '''Tests the getbyuser endpoint
    We pass a name that doesn't exist in the system
    '''
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("getbyuser?start='2020-01-01 00:00'&end='2024-01-01 00:00'&user_name='foo'")
    assert response.status_code == 200

    # we've seeded the system with reservations
    assert len(response.json()['message']['reservations']) == 0

@pytest.mark.asyncio
async def test_get_by_time():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("getbytime?start='2020-01-01 00:00'&end='2024-01-01 00:00'")
    assert response.status_code == 200

    # we've seeded the system with reservations
    assert len(response.json()['message']['reservations']) > 0

@pytest.mark.asyncio
async def test_delete_reservation():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("cancel?id=1")
    assert response.status_code == 200

    # we've seeded the system with reservations
    assert response.json()['refund'] == 0

@pytest.mark.asyncio
async def test_add_and_delete_user():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("user/adduser?username=foo&first_name=Fineas&role=user")
    assert response.status_code == 200

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put("user/changeuser?username=foo&role=scheduler")
    assert response.status_code == 200

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("deleteuser?username=foo")
    assert response.status_code == 200

    

