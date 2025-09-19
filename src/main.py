from fastapi import FastAPI, Depends
from service import *
from schemas import WorkerDTO, WorkerRelDTO, ResumesAddDTO, ResumesDTO, ResumesRelDTO
import uvicorn

app = FastAPI()

PaginationParamsDep = Annotated[PaginationParams, Depends(PaginationParams)]

@app.get('/workers')
async def get_workers(pagination_params: Annotated[PaginationParams, Depends(PaginationParams)]) -> list[WorkerDTO]:
    list_dto_model = await DefaultCRUDService.service_select_workers(pagination_params)
    return list_dto_model

@app.get('/workers/resumes')
async def get_workers_and_resumes(pagination_params: PaginationParamsDep) -> list[WorkerRelDTO]:
    list_dto_model = await DefaultCRUDService.service_select_workers_rel(pagination_params)
    return list_dto_model

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=8000)