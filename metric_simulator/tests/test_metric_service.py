from unittest.mock import AsyncMock, Mock, patch

import pytest

from metric_simulator.metric_service import MAX_RETRIES, RETRY_DELAY, MetricService


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
def metric_service(
    mock_llm_repository, mock_metric_repository, mock_simulator_repository
):
    return MetricService(
        llm_repository=mock_llm_repository,
        metric_repository=mock_metric_repository,
        simulator_repository=mock_simulator_repository,
    )


@pytest.fixture
def mock_redis_client():
    with patch("metric_simulator.metric_service.RedisClient") as mock:
        yield mock.return_value


@pytest.mark.asyncio
async def test_generate_metric_data(metric_service):
    mock_metric_generator = Mock()
    mock_metric_generator.generate_data_points.return_value = [1, 2, 3]
    metric_name = "test_metric"
    llm_name = "test_llm"

    result = await metric_service.generate_metric_data(
        mock_metric_generator, metric_name, llm_name
    )

    assert result == [1, 2, 3]
    mock_metric_generator.generate_data_points.assert_called_once_with(metric_name)


@pytest.mark.asyncio
async def test_simulate_data_points_with_retry_success(
    metric_service, mock_redis_client
):
    mock_lock = AsyncMock()
    mock_redis_client.redis.lock.return_value.__enter__.return_value = mock_lock

    with patch.object(
        metric_service, "simulate_data_points", new_callable=AsyncMock
    ) as mock_simulate:
        await metric_service.simulate_data_points_with_retry()
        mock_redis_client.redis.lock.assert_called_once_with(
            "retry_benchmarks_lock",
            timeout=MAX_RETRIES * RETRY_DELAY,
            blocking=True,
            blocking_timeout=10,
        )
        mock_simulate.assert_called_once()


@pytest.mark.asyncio
async def test_simulate_data_points(
    metric_service,
    mock_llm_repository,
    mock_metric_repository,
    mock_simulator_repository,
    mock_redis_client,
):
    mock_llm = Mock()
    mock_llm.id = 1
    mock_llm.name = "TestLLM"
    mock_llm.company_name = "TestCompany"
    mock_llm_repository.get_llms.return_value = [mock_llm]

    mock_metric = Mock()
    mock_metric.id = 1
    mock_metric.name = "TestMetric"
    mock_metric_repository.get_metrics.return_value = [mock_metric]

    with patch(
        "metric_simulator.metric_service.MetricGenerator"
    ) as mock_generator_class:
        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator
        mock_generator.generate_data_points.return_value = [1, 2, 3]

        await metric_service.simulate_data_points()

        mock_simulator_repository.remove_all_metrics.assert_called_once()
        mock_generator_class.assert_called_once_with("TestCompany", "TestLLM")
        mock_generator.generate_data_points.assert_called_once_with("TestMetric")
        mock_simulator_repository.bulk_add_metrics.assert_called_once_with(
            1, 1, [1, 2, 3]
        )
        mock_redis_client.redis.delete.assert_called()
        mock_redis_client.delete_key.assert_called()


def test_remove_metrics(metric_service, mock_simulator_repository):
    metric_service.remove_metrics()
    mock_simulator_repository.remove_all_metrics.assert_called_once()
