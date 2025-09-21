from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.workers import router as router_workers
from routers.resumes import router as router_resumes
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.include_router(router=router_workers, prefix='/api/v1/workers', tags=['Сотрудники'])
app.include_router(router=router_resumes, prefix='/api/v1/resumes', tags=['Резюме'])

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=8000)