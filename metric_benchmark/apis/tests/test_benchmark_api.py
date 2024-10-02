from unittest.mock import Mock

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient

from metric_benchmark.apis.auth import verify_api_key
from metric_benchmark.apis.benchmark_service import BenchmarkService
from metric_benchmark.apis.v1.route_benchmark import router

load_dotenv()

app = FastAPI()
app.include_router(router)

client = TestClient(app)

TEST_API_KEY = "1234"


@pytest.fixture
def mock_benchmark_service():
    return Mock(spec=BenchmarkService)


@pytest.fixture(autouse=True)
def mock_dependencies(mock_benchmark_service):
    def override_benchmark_service():
        return mock_benchmark_service

    app.dependency_overrides[BenchmarkService] = override_benchmark_service

    yield

    app.dependency_overrides.clear()


def test_get_simulation_and_rankings(mock_benchmark_service):
    app.dependency_overrides[verify_api_key] = lambda: TEST_API_KEY
    cached_data = [{"metric1": [{"llm_name": "LLM1", "mean_value": 0.85}]}]

    mock_response = {"data": cached_data}
    mock_benchmark_service.get_simulation_and_rankings.return_value = mock_response

    response = client.get("/rankings", headers={"X-API-Key": TEST_API_KEY})

    assert response.status_code == 200
    assert response.json() == mock_response
    mock_benchmark_service.get_simulation_and_rankings.assert_called_once()


def test_get_simulation_and_rankings_unauthorized():
    response = client.get("/rankings", headers={"X-API-Key": "wrong_key"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API key"}


def test_get_simulation_and_rankings_by_metric_name(mock_benchmark_service):
    app.dependency_overrides[verify_api_key] = lambda: TEST_API_KEY
    metric_name = "metric1"
    mock_response = {"data": {"metric1": [{"llm_name": "LLM1", "mean_value": 0.85}]}}
    mock_benchmark_service.get_simulation_and_rankings_by_metric_name.return_value = (
        mock_response
    )

    response = client.get(
        f"/rankings/{metric_name}", headers={"X-API-Key": TEST_API_KEY}
    )

    assert response.status_code == 200
    assert response.json() == mock_response
    mock_benchmark_service.get_simulation_and_rankings_by_metric_name.assert_called_once_with(
        metric_name
    )


def test_get_simulation_and_rankings_by_metric_name_unauthorized():
    response = client.get("/rankings/metric1", headers={"X-API-Key": "wrong_key"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API key"}
