from fastapi import FastAPI
from service import *
from schemas import WorkerDTO, WorkerRelDTO, ResumesAddDTO, ResumesDTO, ResumesRelDTO
import uvicorn

app = FastAPI()

@app.get('/workers')
async def get_workers() -> list[WorkerDTO]:
    list_dto_model = await DefaultCRUDService.service_select_workers()
    return list_dto_model

@app.get('/workers/resumes')
async def get_workers_and_resumes() -> list[WorkerRelDTO]:
    list_dto_model = await DefaultCRUDService.service_select_workers_rel()
    return list_dto_model

# @app.get('/worker/{id_worker}')
# async def get_worker_by_id(id_worker) -> WorkerRelDTO:
#     dto_model = await DefaultCRUDService.s


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=8000)