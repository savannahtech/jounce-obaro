from fastapi import APIRouter

from metric_benchmark.apis.v1 import route_benchmark

api_router = APIRouter()
api_router.include_router(
    route_benchmark.router, prefix="/api/v1/benchmarks", tags=["benchmarks"]
)
