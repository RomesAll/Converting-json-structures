from fastapi import APIRouter, Depends
from service import ResumesCRUDService
from schemas import ResumesAddDTO, ResumesDTO, ResumesRelDTO, PaginationParams
from typing import Annotated

router = APIRouter()

PaginationParamsDep = Annotated[PaginationParams, Depends(PaginationParams)]

@router.get('/detail/{id_resume}', summary='Получить резюме по id')
async def get_resume(id_resume: int,) -> list[ResumesRelDTO]:
    dto_model = await ResumesCRUDService.service_select_resumes_by_id(id=id_resume)
    return dto_model

@router.get('/', summary='Получить все резюме')
async def get_resumes(pagination_params: PaginationParamsDep) -> list[ResumesDTO]:
    list_dto_model = await ResumesCRUDService.service_select_resumes(pagination_params)
    return list_dto_model

@router.get('/worker', summary='Получить все резюме и сотрудников, с которыми они связаны')
async def get_resumes_and_worker(pagination_params: PaginationParamsDep) -> list[ResumesRelDTO]:
    list_dto_model = await ResumesCRUDService.service_select_resumes_rel(pagination_params)
    return list_dto_model

@router.post('/create', summary='Добавить резюме')
async def create_resume(resume_info: ResumesAddDTO):
    id = await ResumesCRUDService.service_insert_resumes(resume_info)
    return id

@router.put('/{id_resume}/update', summary='Обновить информацию о резюме')
async def update_resume(id_resume: int, new_data: ResumesAddDTO):
    id = await ResumesCRUDService.service_update_resumes(id_resume, new_data)
    return id

@router.delete('/{id_resume}/delete', summary='Удалить резюме по id')
async def delete_resume(id_resume: int):
    id = await ResumesCRUDService.service_delete_resumes(id=id_resume)
    return id