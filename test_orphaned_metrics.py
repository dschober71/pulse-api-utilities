#!/usr/bin/env python3
"""
Test script for orphaned metrics functionality.
This script tests the API endpoints without requiring real Tableau credentials.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:3000"

def test_api_connection():
    """Test basic API connectivity"""
    print("Testing API connection...")
    response = requests.get(f"{BASE_URL}/api/hello")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_orphaned_metrics_endpoint():
    """Test orphaned metrics detection endpoint structure"""
    print("Testing /orphaned-metrics endpoint structure...")

    # This will fail authentication, but we can verify the endpoint exists
    # and returns the expected error structure
    payload = {
        "server_url": "https://test.tableau.com",
        "api_version": "3.26",
        "site_content_url": "",
        "auth_method": "password",
        "username": "test",
        "password": "test"
    }

    response = requests.post(f"{BASE_URL}/orphaned-metrics", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()

    # Check response structure
    has_success_field = 'success' in result
    has_error_or_results = 'error' in result or 'orphaned_metrics' in result

    print(f"Response has 'success' field: {has_success_field}")
    print(f"Response has error or results: {has_error_or_results}")

    if not result.get('success'):
        print(f"Expected error: {result.get('error', 'Unknown')}")

    print()
    return has_success_field and has_error_or_results

def test_delete_endpoint():
    """Test delete orphaned metrics endpoint structure"""
    print("Testing /delete-orphaned-metrics endpoint structure...")

    # Test without confirmation - should fail
    payload = {
        "server_url": "https://test.tableau.com",
        "api_version": "3.26",
        "site_content_url": "",
        "auth_method": "password",
        "username": "test",
        "password": "test",
        "orphaned_metric_ids": ["test-id-1", "test-id-2"]
    }

    response = requests.post(f"{BASE_URL}/delete-orphaned-metrics", json=payload)
    result = response.json()

    print(f"Status: {response.status_code}")
    print(f"Response has 'success' field: {'success' in result}")

    # Should fail without confirmation
    if not result.get('success'):
        print(f"Expected error (no confirmation): {result.get('error', 'Unknown')}")
        assert "confirmation" in result.get('error', '').lower()

    # Test with confirmation but invalid auth
    payload['confirmation'] = 'CONFIRM CLEANUP'
    response = requests.post(f"{BASE_URL}/delete-orphaned-metrics", json=payload)
    result = response.json()
    print(f"\nWith confirmation - Status: {response.status_code}")
    print(f"Expected auth error: {result.get('error', 'Unknown')}")

    print()
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Orphaned Metrics Feature Test Suite")
    print("=" * 60)
    print()

    tests = [
        ("API Connection", test_api_connection),
        ("Orphaned Metrics Endpoint", test_orphaned_metrics_endpoint),
        ("Delete Orphaned Metrics Endpoint", test_delete_endpoint),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' raised exception: {e}\n")
            results.append((test_name, False))

    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    print()

    all_passed = all(result for _, result in results)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check output above for details.")
