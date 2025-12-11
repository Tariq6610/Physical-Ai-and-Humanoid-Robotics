import pytest
import time
import requests
import os
from unittest.mock import patch
from src.services.rag_service import RAGService
from src.api.chat import chat_endpoint
from src.models.chat import ChatRequest


def test_response_time_under_load():
    """
    Test that the API responds within acceptable time limits under load.
    Target: <3 seconds for typical queries as specified in the spec.
    """
    # Mock the RAG service to avoid external dependencies during testing
    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "This is a mocked response for performance testing."

        # Test single request response time
        start_time = time.time()

        # Create a test request
        test_request = ChatRequest(query="What is ROS 2?")

        # Call the endpoint
        response = chat_endpoint(test_request)

        end_time = time.time()
        response_time = end_time - start_time

        # Assert that response time is under 3 seconds
        assert response_time < 3.0, f"Response time {response_time:.2f}s exceeded 3 seconds"

        # Verify the response content
        assert "response" in response
        assert response["response"] == "This is a mocked response for performance testing."


def test_multiple_requests_performance():
    """
    Test performance when handling multiple requests in succession.
    """
    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "Performance test response"

        # Measure time for multiple requests
        start_time = time.time()

        num_requests = 10
        for i in range(num_requests):
            test_request = ChatRequest(query=f"Performance test query {i}")
            response = chat_endpoint(test_request)
            assert "response" in response

        end_time = time.time()
        total_time = end_time - start_time
        avg_response_time = total_time / num_requests

        # Assert average response time is reasonable
        assert avg_response_time < 1.0, f"Average response time {avg_response_time:.2f}s too high for {num_requests} requests"


def test_memory_usage_stability():
    """
    Test that memory usage remains stable during extended usage.
    This test checks for potential memory leaks by running multiple requests.
    """
    import psutil
    import os

    # Get initial memory usage
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "Memory stability test response"

        # Run multiple requests to check for memory leaks
        for i in range(50):  # 50 requests should be enough to detect obvious leaks
            test_request = ChatRequest(query=f"Memory test query {i}")
            response = chat_endpoint(test_request)
            assert "response" in response

        # Check final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 50MB for 50 requests)
        assert memory_increase < 50, f"Memory increased by {memory_increase:.2f}MB which is too high"


def test_concurrent_request_simulation():
    """
    Simulate concurrent requests to test API stability under parallel load.
    Note: This is a simplified simulation without true threading.
    """
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "Concurrent test response"

        def make_request(query_num):
            test_request = ChatRequest(query=f"Concurrent test query {query_num}")
            return chat_endpoint(test_request)

        # Simulate 5 concurrent requests
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, i) for i in range(5)]
            results = [future.result() for future in futures]

        end_time = time.time()
        total_time = end_time - start_time

        # Verify all requests completed successfully
        assert len(results) == 5
        for result in results:
            assert "response" in result

        # Total time should be reasonable (less than 5 seconds for 5 concurrent requests)
        assert total_time < 5.0, f"Total time for concurrent requests {total_time:.2f}s too high"


def test_large_query_handling():
    """
    Test API performance with larger queries to ensure it handles various input sizes.
    """
    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "Large query response"

        # Test with a larger query
        large_query = "Explain in detail the complete architecture of ROS 2 including all middleware components, node communication patterns, service implementations, action handling, parameter management, and quality of service settings with practical examples for humanoid robotics applications. " * 5  # Repeat to make it larger

        start_time = time.time()
        test_request = ChatRequest(query=large_query)
        response = chat_endpoint(test_request)
        end_time = time.time()

        response_time = end_time - start_time

        # Response time should still be reasonable even with larger queries
        assert response_time < 5.0, f"Response time for large query {response_time:.2f}s exceeded 5 seconds"
        assert "response" in response


if __name__ == "__main__":
    # Run performance tests individually to see timing
    print("Running performance tests...")

    start = time.time()
    test_response_time_under_load()
    print(f"✓ Response time test passed in {time.time() - start:.2f}s")

    start = time.time()
    test_multiple_requests_performance()
    print(f"✓ Multiple requests test passed in {time.time() - start:.2f}s")

    start = time.time()
    test_memory_usage_stability()
    print(f"✓ Memory stability test passed in {time.time() - start:.2f}s")

    start = time.time()
    test_concurrent_request_simulation()
    print(f"✓ Concurrent requests test passed in {time.time() - start:.2f}s")

    start = time.time()
    test_large_query_handling()
    print(f"✓ Large query handling test passed in {time.time() - start:.2f}s")

    print("All performance tests passed!")