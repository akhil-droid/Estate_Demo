"""
UK Estate Agency AI - Test Scenarios
====================================
Run all test scenarios from simple to complex.

Usage:
    python test_scenarios.py              # Run all tests
    python test_scenarios.py --simple     # Run simple tests only
    python test_scenarios.py --medium     # Run medium tests only
    python test_scenarios.py --complex    # Run complex tests only
    python test_scenarios.py --no-approval # Skip human approval
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
BASE_URL = "http://localhost:8000"
RESULTS_FILE = "test_results.json"

# Test results storage
test_results = []


def log(message: str, level: str = "INFO"):
    """Print formatted log message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "TEST": "🧪"}
    print(f"[{timestamp}] {icons.get(level, 'ℹ️')} {message}")


def make_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """Make HTTP request to API."""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=60)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=60)
        else:
            return {"error": f"Unknown method: {method}"}
        
        # Check for HTTP errors
        if response.status_code >= 400:
            try:
                error_detail = response.json()
                return {"error": f"HTTP {response.status_code}: {error_detail.get('detail', 'Unknown error')}"}
            except:
                return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
        
        # Try to parse JSON
        if not response.text:
            return {"error": "Empty response from server"}
        
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed. Is the server running?"}
    except requests.exceptions.JSONDecodeError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}


def run_test(test_id: str, name: str, method: str, endpoint: str, 
             data: Dict = None, expected_keys: List[str] = None,
             expected_values: Dict = None) -> bool:
    """Run a single test and record result."""
    log(f"[{test_id}] {name}", "TEST")
    
    start_time = time.time()
    result = make_request(method, endpoint, data)
    elapsed = round((time.time() - start_time) * 1000)
    
    # Check for errors
    if "error" in result:
        log(f"  Error: {result['error']}", "FAIL")
        test_results.append({
            "test_id": test_id,
            "name": name,
            "status": "FAIL",
            "error": result["error"],
            "elapsed_ms": elapsed
        })
        return False
    
    # Check expected keys
    passed = True
    if expected_keys:
        for key in expected_keys:
            if key not in result:
                log(f"  Missing key: {key}", "FAIL")
                passed = False
    
    # Check expected values
    if expected_values:
        for key, expected in expected_values.items():
            actual = result.get(key)
            if actual != expected:
                log(f"  {key}: expected '{expected}', got '{actual}'", "FAIL")
                passed = False
    
    if passed:
        log(f"  Passed ({elapsed}ms)", "PASS")
    
    test_results.append({
        "test_id": test_id,
        "name": name,
        "status": "PASS" if passed else "FAIL",
        "input": {"method": method, "endpoint": endpoint, "data": data},
        "output": result,
        "elapsed_ms": elapsed
    })
    
    return passed


# ============================================================================
# SIMPLE TESTS - Data Lookups (No LLM)
# ============================================================================

def run_simple_tests():
    """Run simple data lookup tests."""
    print("\n" + "=" * 70)
    print("📋 SIMPLE TESTS - Data Lookups (No LLM)")
    print("=" * 70 + "\n")
    
    tests = [
        # Health check
        ("S001", "Health Check", "GET", "/", None, ["status"], {"status": "running"}),
        ("S002", "Health Endpoint", "GET", "/health", None, ["status"], {"status": "healthy"}),
        ("S003", "List Agents", "GET", "/agents", None, ["agents"], None),
        
        # Property lookups
        ("S004", "Get All Properties", "GET", "/data/properties", None, ["data"], None),
        ("S005", "Get Property by ID", "GET", "/data/properties/PROP-2024-5678", None, ["data"], None),
        ("S006", "Get Invalid Property", "GET", "/data/properties/INVALID-ID", None, None, None),
        
        # Buyer lookups
        ("S007", "Get All Buyers", "GET", "/data/buyers", None, ["data"], None),
        ("S008", "Get Buyer by ID", "GET", "/data/buyers/BUY-2024-3001", None, ["data"], None),
        ("S009", "Get Hot Buyers", "GET", "/data/buyers/hot", None, ["data"], None),
        
        # Vendor lookups
        ("S010", "Get All Vendors", "GET", "/data/vendors", None, ["data"], None),
        ("S011", "Get Vendor by ID", "GET", "/data/vendors/VEN-001", None, ["data"], None),
        
        # Employee lookups
        ("S012", "Get All Employees", "GET", "/data/employees", None, ["data"], None),
        ("S013", "Get Employee by ID", "GET", "/data/employees/EMP-001", None, ["data"], None),
        
        # Execution plans
        ("S014", "Get All Plans", "GET", "/plans", None, ["data"], None),
        ("S015", "Get Plan by ID", "GET", "/plans/PLAN-007", None, ["data"], None),
        ("S016", "Get Plan Steps", "GET", "/plans/PLAN-007/steps", None, ["steps"], None),
        
        # Search operations
        ("S017", "Search Properties by Price", "POST", "/data/properties/search", 
         {"criteria": {"min_price": 300000, "max_price": 400000}}, ["count", "data"], None),
        ("S018", "Search Buyers by Budget", "POST", "/data/buyers/search",
         {"criteria": {"min_budget": 250000, "max_budget": 350000}}, ["count", "data"], None),
        
        # History
        ("S019", "Get History", "GET", "/history", None, ["history"], None),
        
        # Metrics
        ("S020", "Get Metrics", "GET", "/metrics", None, ["data"], None),
    ]
    
    passed = 0
    for test in tests:
        if run_test(*test):
            passed += 1
    
    log(f"Simple Tests: {passed}/{len(tests)} passed", "INFO")
    return passed, len(tests)


# ============================================================================
# MEDIUM TESTS - Direct Agent Calls (Uses LLM)
# ============================================================================

def run_medium_tests():
    """Run medium complexity tests - direct agent calls."""
    print("\n" + "=" * 70)
    print("📋 MEDIUM TESTS - Direct Agent Calls (Uses LLM)")
    print("=" * 70 + "\n")
    
    tests = [
        # Scout Agent
        ("M001", "Scout: Get Property", "POST", "/agents/scout",
         {"action": "Get property details", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M002", "Scout: Get Vendor", "POST", "/agents/scout",
         {"action": "Get vendor information", "context": {"vendor_id": "VEN-001"}},
         ["status"], None),
        
        ("M003", "Scout: Get Buyer", "POST", "/agents/scout",
         {"action": "Get buyer details", "context": {"buyer_id": "BUY-2024-3001"}},
         ["status"], None),
        
        ("M004", "Scout: Verify EPC", "POST", "/agents/scout",
         {"action": "Verify EPC certificate", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M005", "Scout: Create CRM Record", "POST", "/agents/scout",
         {"action": "Create CRM record", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M006", "Scout: Update Portals", "POST", "/agents/scout",
         {"action": "Update portal listings", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        # Intelligence Agent
        ("M007", "Intelligence: Match Buyers", "POST", "/agents/intelligence",
         {"action": "Match buyers for property", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M008", "Intelligence: Assess Risk", "POST", "/agents/intelligence",
         {"action": "Assess transaction risk", "context": {"buyer_id": "BUY-2024-3001", "vendor_id": "VEN-001"}},
         ["status"], None),
        
        ("M009", "Intelligence: Analyze Price", "POST", "/agents/intelligence",
         {"action": "Analyze property price", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M010", "Intelligence: Score Buyer", "POST", "/agents/intelligence",
         {"action": "Score buyer strength", "context": {"buyer_id": "BUY-2024-3001"}},
         ["status"], None),
        
        # Content Agent
        ("M011", "Content: Property Description", "POST", "/agents/content",
         {"action": "Generate property description", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M012", "Content: Email Response", "POST", "/agents/content",
         {"action": "Generate email response", "context": {"buyer_name": "Michael Brown", "property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M013", "Content: Vendor Report", "POST", "/agents/content",
         {"action": "Generate vendor report", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        # Compliance Agent
        ("M014", "Compliance: AML Check", "POST", "/agents/compliance",
         {"action": "Perform AML check", "context": {"vendor_id": "VEN-001"}},
         ["status"], None),
        
        ("M015", "Compliance: Validate EPC", "POST", "/agents/compliance",
         {"action": "Validate EPC", "context": {"property_id": "PROP-2024-5678"}},
         ["status"], None),
        
        ("M016", "Compliance: Validate Content", "POST", "/agents/compliance",
         {"action": "Validate content", "context": {"content": "Beautiful 3-bed family home with garden."}},
         ["status"], None),
    ]
    
    passed = 0
    for test in tests:
        if run_test(*test):
            passed += 1
        time.sleep(1)  # Rate limiting
    
    log(f"Medium Tests: {passed}/{len(tests)} passed", "INFO")
    return passed, len(tests)


# ============================================================================
# COMPLEX TESTS - Full Orchestrator Workflows (Uses LLM + Approval)
# ============================================================================

def run_complex_tests(require_approval: bool = False):
    """Run complex orchestrator workflow tests."""
    print("\n" + "=" * 70)
    print("📋 COMPLEX TESTS - Full Orchestrator Workflows")
    print("=" * 70)
    if require_approval:
        print("⚠️  Human approval required - check terminal!")
    else:
        print("ℹ️  Running without human approval")
    print()
    
    tests = [
        # Stage 1: Lead Generation
        ("C001", "Lead Capture - Website Form", 
         {"query": "New valuation request from Sarah Anderson for 47 Oak Road, M20 2QR",
          "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001"},
          "require_approval": require_approval}),
        
        ("C002", "Portal Enquiry Response",
         {"query": "Rightmove enquiry from Michael Brown about 47 Oak Road - cash buyer, wants viewing",
          "context": {"property_id": "PROP-2024-5678", "buyer_id": "BUY-2024-3001"},
          "require_approval": require_approval}),
        
        # Stage 3: Instruction
        ("C003", "New Instruction - Full Onboarding",
         {"query": "Instruction signed for 47 Oak Road, M20 2QR - begin full onboarding",
          "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001"},
          "require_approval": require_approval}),
        
        ("C004", "Generate Property Description",
         {"query": "Write property description for 47 Oak Road targeting family buyers",
          "context": {"property_id": "PROP-2024-5678"},
          "require_approval": require_approval}),
        
        # Stage 4: Launch
        ("C005", "Property Launch",
         {"query": "Launch 47 Oak Road on all portals",
          "context": {"property_id": "PROP-2024-5678"},
          "require_approval": require_approval}),
        
        # Stage 5: Marketing
        ("C006", "Daily Buyer Matching",
         {"query": "Find matching buyers for 47 Oak Road",
          "context": {"property_id": "PROP-2024-5678"},
          "require_approval": require_approval}),
        
        # Stage 6: Enquiries
        ("C007", "Immediate Enquiry Response",
         {"query": "URGENT: New Rightmove enquiry for 47 Oak Road - respond within 5 minutes",
          "context": {"property_id": "PROP-2024-5678", "buyer_name": "Sophie Turner"},
          "require_approval": require_approval}),
        
        # Stage 7: Feedback
        ("C008", "Weekly Vendor Report",
         {"query": "Generate weekly vendor report for 47 Oak Road",
          "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001"},
          "require_approval": require_approval}),
        
        # Stage 8: Offer
        ("C009", "Offer Qualification",
         {"query": "New offer received: £275,000 from Michael Brown for 47 Oak Road - verify buyer",
          "context": {"property_id": "PROP-2024-5678", "buyer_id": "BUY-2024-3001", "offer_amount": 275000},
          "require_approval": require_approval}),
        
        # Stage 9: Sale Agreed
        ("C010", "Sale Agreed Workflow",
         {"query": "Sale agreed on 47 Oak Road to Michael Brown for £280,000",
          "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001", "buyer_id": "BUY-2024-3001"},
          "require_approval": require_approval}),
        
        # Stage 10: MoS
        ("C011", "Generate Memorandum of Sale",
         {"query": "Generate and distribute MoS for 47 Oak Road",
          "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001", "buyer_id": "BUY-2024-3001"},
          "require_approval": require_approval}),
        
        # Compliance scenarios
        ("C012", "AML Compliance Check",
         {"query": "Run AML check for vendor Sarah Anderson",
          "context": {"vendor_id": "VEN-001"},
          "require_approval": require_approval}),
        
        ("C013", "EPC Verification",
         {"query": "Verify EPC for 47 Oak Road before marketing",
          "context": {"property_id": "PROP-2024-5678"},
          "require_approval": require_approval}),
        
        # Analysis scenarios
        ("C014", "Price Analysis",
         {"query": "Analyze pricing for 47 Oak Road against market comparables",
          "context": {"property_id": "PROP-2024-5678"},
          "require_approval": require_approval}),
        
        ("C015", "Chain Risk Assessment",
         {"query": "Assess chain risk for sale of 31 Park Road",
          "context": {"property_id": "PROP-2024-5682", "buyer_id": "BUY-2024-3023"},
          "require_approval": require_approval}),
    ]
    
    passed = 0
    for test_id, name, data in tests:
        log(f"[{test_id}] {name}", "TEST")
        
        start_time = time.time()
        result = make_request("POST", "/query", data)
        elapsed = round((time.time() - start_time) * 1000)
        
        if "error" in result:
            log(f"  Error: {result['error']}", "FAIL")
            test_results.append({
                "test_id": test_id,
                "name": name,
                "status": "FAIL",
                "error": result["error"],
                "elapsed_ms": elapsed
            })
        elif result.get("status") == "completed":
            log(f"  Passed ({elapsed}ms)", "PASS")
            passed += 1
            test_results.append({
                "test_id": test_id,
                "name": name,
                "status": "PASS",
                "input": data,
                "output": result,
                "elapsed_ms": elapsed
            })
        elif result.get("status") == "rejected":
            log(f"  Rejected by human ({elapsed}ms)", "WARN")
            test_results.append({
                "test_id": test_id,
                "name": name,
                "status": "REJECTED",
                "input": data,
                "output": result,
                "elapsed_ms": elapsed
            })
        else:
            log(f"  Unknown status: {result.get('status')}", "FAIL")
            test_results.append({
                "test_id": test_id,
                "name": name,
                "status": "FAIL",
                "input": data,
                "output": result,
                "elapsed_ms": elapsed
            })
        
        time.sleep(2)  # Rate limiting between complex tests
    
    log(f"Complex Tests: {passed}/{len(tests)} passed", "INFO")
    return passed, len(tests)


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

def run_edge_case_tests():
    """Run edge case tests."""
    print("\n" + "=" * 70)
    print("📋 EDGE CASE TESTS")
    print("=" * 70 + "\n")
    
    tests = [
        # Invalid IDs
        ("E001", "Invalid Property ID", "POST", "/agents/scout",
         {"action": "Get property", "context": {"property_id": "INVALID-999"}},
         ["status"], None),
        
        ("E002", "Invalid Buyer ID", "POST", "/agents/scout",
         {"action": "Get buyer", "context": {"buyer_id": "INVALID-999"}},
         ["status"], None),
        
        ("E003", "Invalid Vendor ID", "POST", "/agents/compliance",
         {"action": "AML check", "context": {"vendor_id": "INVALID-999"}},
         ["status"], None),
        
        # Missing context
        ("E004", "Missing Property ID", "POST", "/agents/content",
         {"action": "Generate description", "context": {}},
         ["status"], None),
        
        ("E005", "Missing Vendor ID for AML", "POST", "/agents/compliance",
         {"action": "AML check", "context": {}},
         ["status"], None),
        
        # Empty inputs
        ("E006", "Empty Action", "POST", "/agents/scout",
         {"action": "", "context": {}},
         ["status"], None),
        
        ("E007", "Empty Query", "POST", "/query",
         {"query": "", "require_approval": False},
         ["status"], None),
        
        # Special characters
        ("E008", "Special Characters in Query", "POST", "/query",
         {"query": "Property at 47 Oak Road (£285,000) - 3-bed & garden!", "require_approval": False},
         ["status"], None),
        
        # Large context
        ("E009", "Large Context", "POST", "/agents/intelligence",
         {"action": "Analyze", "context": {"data": "x" * 1000}},
         ["status"], None),
        
        # Boundary prices
        ("E010", "Search Zero Price", "POST", "/data/properties/search",
         {"criteria": {"min_price": 0, "max_price": 0}},
         ["count"], None),
        
        ("E011", "Search Very High Price", "POST", "/data/properties/search",
         {"criteria": {"min_price": 10000000}},
         ["count"], None),
    ]
    
    passed = 0
    for test in tests:
        if run_test(*test):
            passed += 1
        time.sleep(0.5)
    
    log(f"Edge Case Tests: {passed}/{len(tests)} passed", "INFO")
    return passed, len(tests)


# ============================================================================
# MAIN
# ============================================================================

def save_results():
    """Save test results to file."""
    with open(RESULTS_FILE, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(test_results),
            "passed": sum(1 for t in test_results if t["status"] == "PASS"),
            "failed": sum(1 for t in test_results if t["status"] == "FAIL"),
            "results": test_results
        }, f, indent=2)
    log(f"Results saved to {RESULTS_FILE}", "INFO")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🧪 UK ESTATE AGENCY AI - TEST SUITE")
    print("=" * 70)
    print(f"Server: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Parse arguments
    args = sys.argv[1:]
    run_all = len(args) == 0
    no_approval = "--no-approval" in args
    
    total_passed = 0
    total_tests = 0
    
    # Run simple tests
    if run_all or "--simple" in args:
        p, t = run_simple_tests()
        total_passed += p
        total_tests += t
    
    # Run medium tests
    if run_all or "--medium" in args:
        p, t = run_medium_tests()
        total_passed += p
        total_tests += t
    
    # Run edge case tests
    if run_all or "--edge" in args:
        p, t = run_edge_case_tests()
        total_passed += p
        total_tests += t
    
    # Run complex tests
    if run_all or "--complex" in args:
        p, t = run_complex_tests(require_approval=not no_approval)
        total_passed += p
        total_tests += t
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
    print("=" * 70 + "\n")
    
    # Save results
    save_results()
    
    return 0 if total_passed == total_tests else 1


if __name__ == "__main__":
    sys.exit(main())