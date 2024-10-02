from fastapi import APIRouter, Depends, status

from metric_benchmark.apis.auth import verify_api_key
from metric_benchmark.apis.benchmark_service import BenchmarkService

router = APIRouter()


@router.get("/rankings", status_code=status.HTTP_200_OK)
def get_simulation_and_rankings(
    benchmark_service: BenchmarkService = Depends(BenchmarkService),
    api_key: str = Depends(verify_api_key),
):
    response = benchmark_service.get_simulation_and_rankings()
    return response


@router.get("/rankings/{metric_name}", status_code=status.HTTP_200_OK)
def get_simulation_and_rankings_by_metric_name(
    metric_name: str,
    benchmark_service: BenchmarkService = Depends(BenchmarkService),
    api_key: str = Depends(verify_api_key),
):
    response = benchmark_service.get_simulation_and_rankings_by_metric_name(metric_name)
    return response
