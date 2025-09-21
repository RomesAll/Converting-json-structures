from models import WorkersORM, ResumesORM, Workload
from service import ResumesCRUDService, WorkersCRUDService
from repository import *
from database import Base, engine, async_engine
from sqlalchemy import text
from config import settings
from httpx import AsyncClient, ASGITransport
from src.main import app
import pytest, pytest_asyncio, httpx

@pytest.fixture(scope="session", autouse=True)
async def async_fixture():
    assert settings.database.POSTGRES_MODE == 'TEST'
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope='session', autouse=True)
async def default_data_for_workers():
    async with async_session_factory() as session:
        user1 = WorkersORM(first_name='Марат', last_name='Янбарисов', phone='+790213423', email='mar@gmail.com')
        user2 = WorkersORM(first_name='Роман', last_name='Буба', phone='+790213423', email='asdf@gmail.com')
        user3 = WorkersORM(first_name='Роман', last_name='Тестовый', phone='+790213423', email='asdf@gmail.com')
        user4 = WorkersORM(first_name='Валентин', last_name='Вялый', phone='+790213423', email='rsdfv@gmail.com')
        session.add_all([user1, user2, user3, user4])
        await session.commit()
        resume1 = ResumesORM(title='Python', compensation=7000, workload=Workload.fulltime, worker_id=1)
        resume2 = ResumesORM(title='C++', compensation=7000, workload=Workload.fulltime, worker_id=2)
        session.add_all([resume1, resume2])
        await session.commit()

@pytest.mark.asyncio
async def test_service_select_workers():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.get("/api/v1/workers/")
        assert response.status_code == 200
        json_data = response.json()
        assert len(json_data) == 4

@pytest.mark.asyncio
async def test_service_select_workers_by_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.get("/api/v1/workers/detail/1")
        assert response.status_code == 200
        json = response.json()[0]
        assert json.get('id') == 1

@pytest.mark.asyncio
async def test_service_select_workers_and_resumes():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.get("/api/v1/workers/resumes")
        assert response.status_code == 200
        json = response.json()[0]
        assert len(json.get('resumes')) != 0

@pytest.mark.asyncio
async def test_service_select_workers_insert():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post("/api/v1/workers/create", json={
            "first_name": "test",
            "last_name": "test",
            "phone": "test",
            "email": "user@example.com"
        })
        assert response.status_code == 200
        assert response.json() == 5