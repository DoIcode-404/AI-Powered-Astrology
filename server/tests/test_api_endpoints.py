"""
Automated API Testing Suite for Week 2 Deployment Verification

This script tests all critical API endpoints to ensure production readiness.
Supports both local (http://localhost:8005) and Railway deployments.

Usage:
    python test_api_endpoints.py --url "https://your-railway-url"
    python test_api_endpoints.py --local (for local testing on port 8005)
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import sys

class APITester:
    """Comprehensive API endpoint tester"""

    def __init__(self, base_url: str, verbose: bool = True):
        self.base_url = base_url.rstrip('/')
        self.verbose = verbose
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.kundali_id = None
        self.prediction_id = None
        self.test_results = []
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0

    def log(self, message: str, level: str = "INFO"):
        """Log test messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}] [{level}]"
        print(f"{prefix} {message}")

    def test(self, name: str, method: str, endpoint: str,
             expected_status: int, data: Optional[Dict] = None,
             require_auth: bool = False, timeout: int = 10) -> Tuple[bool, Dict]:
        """Execute a single API test"""

        self.test_count += 1
        url = f"{self.base_url}{endpoint}"

        try:
            headers = {"Content-Type": "application/json"}

            if require_auth:
                if not self.access_token:
                    self.log(f"⚠️  SKIP: {name} (No auth token available)", "WARN")
                    return False, {}
                headers["Authorization"] = f"Bearer {self.access_token}"

            start_time = time.time()

            if method == "GET":
                response = self.session.get(url, headers=headers, timeout=timeout)
            elif method == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=timeout)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=timeout)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms

            # Determine test result
            success = response.status_code == expected_status
            status_emoji = "✅" if success else "❌"

            result_msg = (
                f"{status_emoji} {name} | "
                f"Status: {response.status_code} (expected {expected_status}) | "
                f"Time: {elapsed_time:.2f}ms"
            )

            self.log(result_msg, "INFO" if success else "ERROR")

            if self.verbose and response.text:
                try:
                    response_json = response.json()
                    self.log(f"   Response: {json.dumps(response_json, indent=2)[:200]}...", "DEBUG")
                except:
                    self.log(f"   Response: {response.text[:200]}", "DEBUG")

            # Track results
            self.test_results.append({
                "test": name,
                "success": success,
                "status": response.status_code,
                "expected": expected_status,
                "time_ms": elapsed_time
            })

            if success:
                self.passed_count += 1
            else:
                self.failed_count += 1

            # Return parsed response for token extraction
            try:
                return success, response.json()
            except:
                return success, {}

        except requests.exceptions.Timeout:
            self.log(f"❌ {name} | TIMEOUT (>{timeout}s)", "ERROR")
            self.failed_count += 1
            self.test_results.append({
                "test": name,
                "success": False,
                "error": "Timeout"
            })
            return False, {}
        except requests.exceptions.ConnectionError:
            self.log(f"❌ {name} | CONNECTION ERROR", "ERROR")
            self.failed_count += 1
            self.test_results.append({
                "test": name,
                "success": False,
                "error": "Connection Error"
            })
            return False, {}
        except Exception as e:
            self.log(f"❌ {name} | EXCEPTION: {str(e)}", "ERROR")
            self.failed_count += 1
            self.test_results.append({
                "test": name,
                "success": False,
                "error": str(e)
            })
            return False, {}

    def run_health_check(self):
        """Test: Health check endpoint"""
        self.log("\n" + "="*60, "INFO")
        self.log("PHASE 1: HEALTH & CONNECTIVITY CHECKS", "INFO")
        self.log("="*60, "INFO")

        success, response = self.test(
            "Health Check",
            "GET",
            "/health",
            200
        )

        if not success:
            self.log("\n⚠️  CRITICAL: Health check failed. Server may not be running.", "WARN")
            return False

        return True

    def run_auth_tests(self):
        """Test: User registration and authentication"""
        self.log("\n" + "="*60, "INFO")
        self.log("PHASE 2: AUTHENTICATION TESTS", "INFO")
        self.log("="*60, "INFO")

        # Generate unique email for this test run
        timestamp = int(time.time())
        test_email = f"test.user.{timestamp}@astrology.test"
        test_password = "TestPassword123!@"

        # Test 1: Register new user
        register_data = {
            "email": test_email,
            "username": f"testuser_{timestamp}",
            "password": test_password
        }

        success, response = self.test(
            "User Registration (NEW USER)",
            "POST",
            "/auth/register",
            200,
            register_data
        )

        if success and "data" in response:
            self.access_token = response["data"].get("access_token")
            self.refresh_token = response["data"].get("refresh_token")
            self.user_id = response["data"].get("user_id")

            if not self.access_token:
                self.log("⚠️  No access token in registration response", "WARN")
                return False

            self.log(f"   Access token acquired: {self.access_token[:20]}...", "DEBUG")
        else:
            self.log("⚠️  Registration failed, skipping auth tests", "WARN")
            return False

        # Test 2: Login with same credentials
        login_data = {
            "email": test_email,
            "password": test_password
        }

        success, response = self.test(
            "User Login",
            "POST",
            "/auth/login",
            200,
            login_data
        )

        if success and "data" in response:
            # Update tokens from login
            self.access_token = response["data"].get("access_token")
            self.refresh_token = response["data"].get("refresh_token")

        # Test 3: Refresh token
        refresh_data = {"refresh_token": self.refresh_token}

        success, response = self.test(
            "Token Refresh",
            "POST",
            "/auth/refresh_token",
            200,
            refresh_data,
            require_auth=False
        )

        if success and "data" in response:
            self.access_token = response["data"].get("access_token")

        # Test 4: Invalid credentials
        invalid_login = {
            "email": test_email,
            "password": "WrongPassword123!"
        }

        self.test(
            "Invalid Login Credentials (Expected Error)",
            "POST",
            "/auth/login",
            401,
            invalid_login,
            require_auth=False
        )

        return True

    def run_kundali_tests(self):
        """Test: Kundali generation and CRUD operations"""
        self.log("\n" + "="*60, "INFO")
        self.log("PHASE 3: KUNDALI TESTS", "INFO")
        self.log("="*60, "INFO")

        # Sample birth data
        kundali_data = {
            "birthDate": "1990-05-15",
            "birthTime": "14:30",
            "latitude": 28.7041,
            "longitude": 77.1025,
            "timezone": "Asia/Kolkata"
        }

        # Test 1: Generate kundali
        success, response = self.test(
            "Generate Kundali",
            "POST",
            "/kundali/generate_kundali",
            200,
            kundali_data,
            require_auth=True
        )

        # Test 2: Save kundali
        save_data = {
            "name": "Test Kundali - Automated Test",
            **kundali_data
        }

        success, response = self.test(
            "Save Kundali",
            "POST",
            "/kundali/save_kundali",
            201,
            save_data,
            require_auth=True
        )

        if success and "data" in response:
            self.kundali_id = response["data"].get("id")
            if not self.kundali_id:
                self.log("⚠️  No kundali_id in save response", "WARN")
            else:
                self.log(f"   Kundali saved with ID: {self.kundali_id}", "DEBUG")

        if not self.kundali_id:
            self.log("⚠️  Skipping kundali CRUD tests (no saved kundali)", "WARN")
            return True

        # Test 3: List user kundalis
        self.test(
            "List Kundalis",
            "GET",
            "/kundali/list_kundalis",
            200,
            require_auth=True
        )

        # Test 4: Get specific kundali
        self.test(
            "Get Kundali Details",
            "GET",
            f"/kundali/get_kundali/{self.kundali_id}",
            200,
            require_auth=True
        )

        # Test 5: Update kundali
        update_data = {"name": "Updated Test Kundali - Modified"}

        self.test(
            "Update Kundali",
            "PUT",
            f"/kundali/update_kundali/{self.kundali_id}",
            200,
            update_data,
            require_auth=True
        )

        # Test 6: Delete kundali (do this last)
        self.test(
            "Delete Kundali",
            "DELETE",
            f"/kundali/delete_kundali/{self.kundali_id}",
            200,
            require_auth=True
        )

        return True

    def run_prediction_tests(self):
        """Test: Prediction endpoints"""
        self.log("\n" + "="*60, "INFO")
        self.log("PHASE 4: PREDICTION TESTS", "INFO")
        self.log("="*60, "INFO")

        if not self.kundali_id:
            self.log("⚠️  Skipping prediction tests (no kundali available)", "WARN")
            self.log("   Creating temporary kundali for testing...", "INFO")

            kundali_data = {
                "name": "Temp for Predictions",
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 28.7041,
                "longitude": 77.1025,
                "timezone": "Asia/Kolkata"
            }

            success, response = self.test(
                "Create Temp Kundali",
                "POST",
                "/kundali/save_kundali",
                201,
                kundali_data,
                require_auth=True
            )

            if success and "data" in response:
                self.kundali_id = response["data"].get("id")

        if not self.kundali_id:
            self.log("❌ Cannot test predictions without kundali", "ERROR")
            return False

        # Test 1: Create prediction
        prediction_data = {
            "kundali_id": self.kundali_id,
            "prediction_type": "career",
            "timeframe": "next_year"
        }

        success, response = self.test(
            "Create Prediction",
            "POST",
            "/predictions/create",
            201,
            prediction_data,
            require_auth=True
        )

        if success and "data" in response:
            self.prediction_id = response["data"].get("id")

        # Test 2: List predictions
        self.test(
            "List Predictions",
            "GET",
            "/predictions/list",
            200,
            require_auth=True
        )

        # Test 3: Get prediction details (if available)
        if self.prediction_id:
            self.test(
                "Get Prediction Details",
                "GET",
                f"/predictions/get/{self.prediction_id}",
                200,
                require_auth=True
            )

        return True

    def run_error_tests(self):
        """Test: Error handling"""
        self.log("\n" + "="*60, "INFO")
        self.log("PHASE 5: ERROR HANDLING TESTS", "INFO")
        self.log("="*60, "INFO")

        # Test 1: Invalid endpoint
        self.test(
            "Invalid Endpoint (Expected 404)",
            "GET",
            "/nonexistent/endpoint",
            404
        )

        # Test 2: Missing required field
        invalid_data = {
            "birthDate": "1990-05-15"
            # Missing other required fields
        }

        self.test(
            "Missing Required Fields (Expected 422)",
            "POST",
            "/kundali/generate_kundali",
            422,
            invalid_data,
            require_auth=True
        )

        # Test 3: Invalid date format
        invalid_date_data = {
            "birthDate": "invalid-date",
            "birthTime": "14:30",
            "latitude": 28.7041,
            "longitude": 77.1025,
            "timezone": "Asia/Kolkata"
        }

        self.test(
            "Invalid Date Format (Expected 422)",
            "POST",
            "/kundali/generate_kundali",
            422,
            invalid_date_data,
            require_auth=True
        )

        # Test 4: Unauthorized access
        self.test(
            "Unauthorized Access (Expected 401)",
            "GET",
            "/kundali/list_kundalis",
            401,
            require_auth=False  # Don't add token
        )

        return True

    def print_summary(self):
        """Print test summary"""
        self.log("\n" + "="*60, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("="*60, "INFO")

        self.log(f"Total Tests: {self.test_count}", "INFO")
        self.log(f"Passed: {self.passed_count} ✅", "INFO")
        self.log(f"Failed: {self.failed_count} ❌", "INFO")

        if self.failed_count == 0:
            self.log("\n🎉 ALL TESTS PASSED! API is ready for production.", "INFO")
            return True
        else:
            self.log(f"\n⚠️  {self.failed_count} tests failed. Please review errors above.", "WARN")
            return False

    def run_all_tests(self):
        """Run complete test suite"""
        self.log("Starting API Test Suite...", "INFO")
        self.log(f"Target URL: {self.base_url}", "INFO")

        # Check if server is reachable
        if not self.run_health_check():
            self.log("\n❌ CRITICAL: Cannot reach server. Aborting tests.", "ERROR")
            return False

        # Run all test phases
        self.run_auth_tests()
        self.run_kundali_tests()
        self.run_prediction_tests()
        self.run_error_tests()

        # Print summary
        return self.print_summary()


def main():
    parser = argparse.ArgumentParser(
        description="API Testing Suite for Kundali Astrology API"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="Base URL for API (e.g., https://your-railway-app.up.railway.app)"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Test local server on http://localhost:8005"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="Show detailed response output"
    )

    args = parser.parse_args()

    # Determine base URL
    if args.local:
        base_url = "http://localhost:8005"
    elif args.url:
        base_url = args.url
    else:
        print("Error: Specify --url or --local")
        parser.print_help()
        sys.exit(1)

    # Run tests
    tester = APITester(base_url, verbose=args.verbose)
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()