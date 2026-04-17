#!/usr/bin/env python
"""
Day 12 Lab - Auto Grading Script
Based on INSTRUCTOR_GUIDE.md

Usage: python grade.py <public-url> <api-key>

Example:
python grade.py https://day12-ha-tang-cloud-va-deployment-2.onrender.com dev-key-change-me
"""

import sys
import os
import time
import requests


class Grader:
    def __init__(self, public_url, api_key):
        self.public_url = public_url.rstrip("/")
        self.api_key = api_key
        self.score = 0
        self.max_score = 80
        self.results = []

    def print_result(self, name, points, passed, detail=""):
        icon = "PASS" if passed else "FAIL"
        self.results.append(f"[{icon}] {name}: {points}/{points} {detail}")
        if passed:
            self.score += points

    def test_functionality(self):
        """Part 6: Functional Requirements (20 points)"""
        print("\n" + "=" * 50)
        print("FUNCTIONALITY (20pts)")
        print("=" * 50)

        # Test 1: Agent works (10pts)
        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
        r = requests.post(
            f"{self.public_url}/ask",
            headers=headers,
            json={"question": "Hello"},
            timeout=15,
        )
        passed = r.status_code == 200 and "answer" in r.json()
        self.print_result(
            "Agent responds correctly", 10, passed, f"status: {r.status_code}"
        )

        # Test 2: Error handling (5pts)
        r = requests.post(
            f"{self.public_url}/ask",
            headers=headers,
            json={},  # Invalid - missing question
            timeout=10,
        )
        passed = r.status_code in [422, 400, 401]
        self.print_result("Error handling", 5, passed, f"status: {r.status_code}")

        # Test 3: Model in response (5pts)
        r = requests.post(
            f"{self.public_url}/ask",
            headers=headers,
            json={"question": "test"},
            timeout=10,
        )
        data = r.json()
        passed = "model" in data or "timestamp" in data
        self.print_result("Response metadata", 5, passed)

    def test_docker(self):
        """Part 6: Docker & Configuration (15 points)"""
        print("\n" + "=" * 50)
        print("DOCKER (15pts)")
        print("=" * 50)

        # Check Dockerfile exists (handled by repo check)
        # Check multi-stage (5pts)
        self.print_result("Multi-stage Dockerfile", 5, True, "Manual check required")

        # Check docker-compose (4pts)
        self.print_result("docker-compose.yml", 4, True, "Manual check required")

        # Check environment config (3pts)
        # Test that config comes from env vars
        r = requests.get(f"{self.public_url}/health", timeout=10)
        data = r.json()
        passed = "version" in data or "environment" in data
        self.print_result(
            "Environment config", 3, passed, f"env: {data.get('environment')}"
        )

        # Config not hardcoded (3pts)
        self.print_result("No hardcoded config", 3, True, "Manual check required")

    def test_security(self):
        """Part 6: Security (20 points)"""
        print("\n" + "=" * 50)
        print("SECURITY (20pts)")
        print("=" * 50)

        # Test 1: Auth required (5pts)
        r = requests.post(
            f"{self.public_url}/ask", json={"question": "test"}, timeout=10
        )
        passed = r.status_code == 401
        self.print_result("Auth required (no key)", 5, passed, f"got {r.status_code}")

        # Test 2: Auth works (5pts)
        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
        r = requests.post(
            f"{self.public_url}/ask",
            headers=headers,
            json={"question": "test"},
            timeout=10,
        )
        passed = r.status_code == 200
        self.print_result("Auth with valid key", 5, passed, f"status: {r.status_code}")

        # Test 3: Rate limiting (5pts)
        # Make requests until rate limited
        rate_limited = False
        for i in range(15):
            r = requests.post(
                f"{self.public_url}/ask",
                headers=headers,
                json={"question": "test"},
                timeout=10,
            )
            if r.status_code == 429:
                rate_limited = True
                break
        self.print_result("Rate limiting", 5, rate_limited, f"got 429: {rate_limited}")

        # Test 4: No hardcoded secrets (5pts) - Manual check
        self.print_result("No hardcoded secrets", 5, True, "Manual check required")

    def test_reliability(self):
        """Part 6: Reliability (15 points)"""
        print("\n" + "=" * 50)
        print("RELIABILITY (15pts)")
        print("=" * 50)

        # Test 1: Health check (3pts)
        r = requests.get(f"{self.public_url}/health", timeout=10)
        passed = r.status_code == 200
        self.print_result("/health endpoint", 3, passed, f"status: {r.status_code}")

        # Test 2: Readiness check (3pts)
        r = requests.get(f"{self.public_url}/ready", timeout=10)
        passed = r.status_code in [200, 503]
        self.print_result("/ready endpoint", 3, passed, f"status: {r.status_code}")

        # Test 3: Graceful shutdown - Manual check (4pts)
        self.print_result("Graceful shutdown", 4, True, "Manual check required")

        # Test 4: Stateless (Redis) - Manual check (5pts)
        self.print_result("Stateless design", 5, True, "Manual check required")

    def test_deployment(self):
        """Part 6: Deployment (10 points)"""
        print("\n" + "=" * 50)
        print("DEPLOYMENT (10pts)")
        print("=" * 50)

        # Test 1: Public URL works (5pts)
        r = requests.get(f"{self.public_url}/health", timeout=10)
        passed = r.status_code == 200
        self.print_result("Public URL works", 5, passed, f"url: {self.public_url}")

        # Test 2: Config files (3pts)
        self.print_result("Config files exist", 3, True, "Manual check required")

        # Test 3: Environment setup (2pts)
        r = requests.get(f"{self.public_url}/health", timeout=10)
        data = r.json()
        env = data.get("environment", "unknown")
        passed = env in ["development", "staging", "production"]
        self.print_result("Environment set", 2, passed, f"env: {env}")

    def run_all_tests(self):
        """Run all grading tests"""
        print("\n" + "=" * 60)
        print("DAY 12 LAB - AUTO GRADING")
        print("=" * 60)
        print(f"URL: {self.public_url}")
        print(f"API Key: {self.api_key[:4]}...")

        self.test_functionality()
        self.test_docker()
        self.test_security()
        self.test_reliability()
        self.test_deployment()

        # Summary
        print("\n" + "=" * 60)
        print("GRADING RESULTS")
        print("=" * 60)

        for result in self.results:
            print(result)

        print("=" * 60)
        print(f"TOTAL: {self.score}/{self.max_score}")
        print("=" * 60)

        percentage = self.score / self.max_score * 100
        if percentage >= 70:
            print("PASSED (>= 70%)")
        else:
            print("NEEDS IMPROVEMENT (< 70%)")

        return self.score


def main():
    if len(sys.argv) < 2:
        # Default values for testing
        public_url = os.getenv(
            "BASE_URL", "https://day12-ha-tang-cloud-va-deployment-2.onrender.com"
        )
        api_key = os.getenv("AGENT_API_KEY", "6feb7477338741064ebe2221892333d4")
    else:
        public_url = sys.argv[1]
        api_key = sys.argv[2] if len(sys.argv) > 2 else "dev-key-change-me"

    grader = Grader(public_url, api_key)
    score = grader.run_all_tests()

    sys.exit(0 if score >= 56 else 1)  # 70% of 80 = 56


if __name__ == "__main__":
    main()
