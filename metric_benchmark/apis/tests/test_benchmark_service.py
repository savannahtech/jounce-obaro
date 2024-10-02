import json
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from metric_benchmark.apis.benchmark_service import BenchmarkService


@pytest.fixture
def mock_llm_repository():
    return Mock()


@pytest.fixture
def mock_metric_repository():
    return Mock()


@pytest.fixture
def mock_simulator_repository():
    return Mock()


@pytest.fixture
def benchmark_service(
    mock_llm_repository, mock_metric_repository, mock_simulator_repository
):
    return BenchmarkService(
        llm_repository=mock_llm_repository,
        metric_repository=mock_metric_repository,
        simulator_repository=mock_simulator_repository,
    )


@pytest.fixture
def mock_redis_client():
    with patch("metric_benchmark.apis.benchmark_service.RedisClient") as mock:
        yield mock.return_value


def test_get_simulation_and_rankings_from_cache(benchmark_service, mock_redis_client):
    cached_data = [{"metric1": [{"llm_name": "LLM1", "mean_value": 0.85}]}]
    mock_redis_client.redis.exists.return_value = True
    mock_redis_client.redis.get.return_value = json.dumps(cached_data)
    result = benchmark_service.get_simulation_and_rankings()

    assert result == {"data": cached_data}
    mock_redis_client.redis.exists.assert_called_once()
    mock_redis_client.redis.get.assert_called_once()


def test_get_simulation_and_rankings_from_repositories(
    benchmark_service,
    mock_redis_client,
    mock_metric_repository,
    mock_simulator_repository,
):
    mock_redis_client.redis.exists.return_value = False
    mock_metric = Mock()
    mock_metric.name = "metric1"
    mock_metric_repository.get_metrics.return_value = [mock_metric]
    mock_simulator_repository.get_metric_means_by_llm.return_value = [
        ("LLM1", 0.854321)
    ]

    result = benchmark_service.get_simulation_and_rankings()

    expected_data = [{"metric1": [{"llm_name": "LLM1", "mean_value": 0.85}]}]
    assert result == {"data": expected_data}
    mock_redis_client.redis.set.assert_called_once()


def test_get_simulation_and_rankings_by_metric_name_from_cache(
    benchmark_service, mock_redis_client
):
    metric_name = "metric1"
    cached_data = {"metric1": [{"llm_name": "LLM1", "mean_value": 0.85}]}
    mock_redis_client.redis.exists.return_value = True
    mock_redis_client.redis.get.return_value = json.dumps(cached_data)

    result = benchmark_service.get_simulation_and_rankings_by_metric_name(metric_name)

    assert result == {"data": cached_data}
    mock_redis_client.redis.exists.assert_called_once()
    mock_redis_client.redis.get.assert_called_once()


def test_get_simulation_and_rankings_by_metric_name_from_repositories(
    benchmark_service,
    mock_redis_client,
    mock_metric_repository,
    mock_simulator_repository,
):
    metric_name = "metric1"
    mock_redis_client.redis.exists.return_value = False
    mock_metric = Mock()
    mock_metric.name = metric_name
    mock_metric_repository.get_metric_by_name.return_value = mock_metric
    mock_simulator_repository.get_metric_means_by_llm.return_value = [
        ("LLM1", 0.854321)
    ]

    result = benchmark_service.get_simulation_and_rankings_by_metric_name(metric_name)

    expected_data = {"metric1": [{"llm_name": "LLM1", "mean_value": 0.85}]}
    assert result == {"data": expected_data}
    mock_redis_client.redis.set.assert_called_once()


def test_get_simulation_and_rankings_by_metric_name_not_found(
    mock_redis_client, benchmark_service, mock_metric_repository
):
    mock_redis_client.redis.exists.return_value = False
    metric_name = "non_existent_metric"
    mock_metric_repository.get_metric_by_name.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        benchmark_service.get_simulation_and_rankings_by_metric_name(metric_name)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Metric not found"
