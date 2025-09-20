from fastapi import APIRouter, Depends
from service import WorkersCRUDService
from schemas import WorkerDTO, WorkerRelDTO, PaginationParams, WorkerAddDTO
from typing import Annotated

router = APIRouter()

PaginationParamsDep = Annotated[PaginationParams, Depends(PaginationParams)]

@router.get('/{id_worker}', summary='Получить сотрудника по id')
async def get_worker(id_worker: int) -> WorkerRelDTO:
    dto_model = await WorkersCRUDService.service_select_worker_by_id(id=id_worker)
    return dto_model

@router.get('/', summary='Получить всех сотрудников')
async def get_workers(pagination_params: PaginationParamsDep) -> list[WorkerDTO]:
    list_dto_model = await WorkersCRUDService.service_select_workers(pagination_params)
    return list_dto_model

@router.get('/resumes', summary='Получить всех сотрудников и резюме этих сотрудников')
async def get_workers_and_resumes(pagination_params: PaginationParamsDep) -> list[WorkerRelDTO]:
    list_dto_model = await WorkersCRUDService.service_select_workers_rel(pagination_params)
    return list_dto_model

@router.post('/create', summary='Добавить сотрудника')
async def create_worker(worker_info: WorkerAddDTO):
    id = await WorkersCRUDService.service_insert_workers(worker_info)
    return id

@router.put('/{id_worker}/update', summary='Обновить информацию о сотруднике')
async def update_worker(id_worker: int, new_data: WorkerAddDTO):
    id = await WorkersCRUDService.service_update_workers(id_worker, new_data)
    return id

@router.delete('/{id_worker}/delete', summary='Удалить сотрудника по id')
async def delete_worker(id_worker: int):
    id = await WorkersCRUDService.service_delete_workers(id=id_worker)
    return id