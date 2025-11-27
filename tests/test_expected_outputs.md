# Test Expected Inputs & Outputs
## UK Estate Agency AI - Multi-Agent System

---

## SIMPLE TESTS (S001-S020) - No LLM, Data Lookups Only

### S001: Health Check
**Input:**
```
GET /
```
**Expected Output:**
```json
{
    "status": "running",
    "service": "UK Estate Agency AI - Multi-Agent System",
    "version": "1.0.0",
    "agents": ["Orchestrator", "Scout", "Intelligence", "Content", "Compliance"]
}
```

---

### S005: Get Property by ID
**Input:**
```
GET /data/properties/PROP-2024-5678
```
**Expected Output:**
```json
{
    "data": {
        "property_id": "PROP-2024-5678",
        "address_line1": "47 Oak Road",
        "postcode": "M20 2QR",
        "property_type": "semi_detached",
        "bedrooms": 3,
        "bathrooms": 2,
        "asking_price": 285000,
        "status": "active",
        "epc_rating": "C",
        "epc_expiry": "2033-05-15",
        "vendor_id": "VEN-001",
        ...
    }
}
```

---

### S008: Get Buyer by ID
**Input:**
```
GET /data/buyers/BUY-2024-3001
```
**Expected Output:**
```json
{
    "data": {
        "buyer_id": "BUY-2024-3001",
        "first_name": "Michael",
        "last_name": "Brown",
        "buyer_type": "chain_free_cash",
        "max_budget": 320000,
        "priority_level": "hot",
        "financial_status": "verified",
        ...
    }
}
```

---

### S011: Get Vendor by ID
**Input:**
```
GET /data/vendors/VEN-001
```
**Expected Output:**
```json
{
    "data": {
        "vendor_id": "VEN-001",
        "first_name": "Sarah",
        "last_name": "Anderson",
        "property_id": "PROP-2024-5678",
        "aml_status": "verified",
        "aml_certificate_id": "AML-2024-9001",
        "pep_check": "clear",
        "sanctions_check": "clear",
        ...
    }
}
```

---

### S017: Search Properties by Price
**Input:**
```
POST /data/properties/search
{
    "criteria": {
        "min_price": 300000,
        "max_price": 400000
    }
}
```
**Expected Output:**
```json
{
    "count": 8,  // Number varies based on data
    "data": [
        {"property_id": "...", "asking_price": 350000, ...},
        {"property_id": "...", "asking_price": 365000, ...},
        ...
    ]
}
```

---

## MEDIUM TESTS (M001-M016) - Direct Agent Calls

### M001: Scout - Get Property
**Input:**
```
POST /agents/scout
{
    "action": "Get property details",
    "context": {"property_id": "PROP-2024-5678"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "type": "property",
    "data": {
        "property_id": "PROP-2024-5678",
        "address_line1": "47 Oak Road",
        "asking_price": 285000,
        ...
    }
}
```

---

### M004: Scout - Verify EPC
**Input:**
```
POST /agents/scout
{
    "action": "Verify EPC certificate",
    "context": {"property_id": "PROP-2024-5678"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "type": "epc_verification",
    "epc_rating": "C",
    "epc_expiry": "2033-05-15",
    "valid": true
}
```

---

### M007: Intelligence - Match Buyers
**Input:**
```
POST /agents/intelligence
{
    "action": "Match buyers for property",
    "context": {"property_id": "PROP-2024-5678"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "type": "buyer_matching",
    "matches_found": 12,
    "top_matches": [
        {"buyer_id": "BUY-2024-3001", "name": "Michael Brown", "score": 94, "buyer_type": "chain_free_cash", "priority": "hot"},
        {"buyer_id": "BUY-2024-3002", "name": "James Wilson", "score": 85, "buyer_type": "first_time_buyer", "priority": "warm"},
        ...
    ]
}
```

---

### M008: Intelligence - Assess Risk
**Input:**
```
POST /agents/intelligence
{
    "action": "Assess transaction risk",
    "context": {"buyer_id": "BUY-2024-3001", "vendor_id": "VEN-001"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "risk_level": "LOW",
    "risk_score": 20,
    "factors": [
        "✅ Chain-free cash buyer",
        "✅ Finances verified"
    ]
}
```

---

### M011: Content - Property Description
**Input:**
```
POST /agents/content
{
    "action": "Generate property description",
    "context": {"property_id": "PROP-2024-5678"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "type": "property_description",
    "word_count": 165,
    "content": "Welcome to this charming three-bedroom semi-detached family home, ideally situated on Oak Road in the sought-after M20 area of Manchester. This well-presented property offers spacious accommodation throughout, featuring a welcoming entrance hall, a bright living room with bay window, and a modern fitted kitchen with dining area..."
}
```

---

### M014: Compliance - AML Check
**Input:**
```
POST /agents/compliance
{
    "action": "Perform AML check",
    "context": {"vendor_id": "VEN-001"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "aml_passed": true,
    "aml_status": "verified",
    "certificate_id": "AML-2024-9001"
}
```

---

### M015: Compliance - Validate EPC
**Input:**
```
POST /agents/compliance
{
    "action": "Validate EPC",
    "context": {"property_id": "PROP-2024-5678"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "epc_valid": true,
    "epc_rating": "C",
    "epc_expiry": "2033-05-15"
}
```

---

## COMPLEX TESTS (C001-C015) - Full Orchestrator Workflows

### C001: Lead Capture - Website Form
**Input:**
```
POST /query
{
    "query": "New valuation request from Sarah Anderson for 47 Oak Road, M20 2QR",
    "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001"},
    "require_approval": true
}
```
**Terminal Shows (awaiting approval):**
```
======================================================================
🎯 ORCHESTRATOR EXECUTION PLAN - AWAITING APPROVAL
======================================================================

📋 Plan ID: PLAN-001
📝 Plan Name: Inbound Lead Capture
📄 Description: Process new valuation request from website

⏱️  Estimated Time: 3500ms
💰 Estimated Cost: $0.45
🤖 Agents Required: orchestrator, scout, content
📊 Total Steps: 3
⚡ Parallel Groups: 1

📋 Execution Steps:
--------------------------------------------------
  Step 1: [scout] Create CRM lead record
  Step 2: [scout] Verify property details
  Step 3: [content] Send acknowledgment email

----------------------------------------------------------------------
👤 Do you approve this plan? (yes/no/modify):
```
**Expected Output (after typing 'yes'):**
```json
{
    "status": "completed",
    "plan": {
        "plan_id": "PLAN-001",
        "plan_name": "Inbound Lead Capture",
        "agents_required": ["orchestrator", "scout", "content"],
        "steps": [...]
    },
    "results": {
        "status": "completed",
        "steps_completed": [
            {"step": 1, "agent": "scout", "action": "Create CRM lead record", "result": {"status": "success", "record_id": "REC-20241127..."}},
            {"step": 2, "agent": "scout", "action": "Verify property details", "result": {"status": "success", "data": {...}}},
            {"step": 3, "agent": "content", "action": "Send acknowledgment email", "result": {"status": "success", "content": "..."}}
        ]
    }
}
```

---

### C003: New Instruction - Full Onboarding
**Input:**
```
POST /query
{
    "query": "Instruction signed for 47 Oak Road, M20 2QR - begin full onboarding",
    "context": {"property_id": "PROP-2024-5678", "vendor_id": "VEN-001"},
    "require_approval": true
}
```
**Terminal Shows:**
```
📋 Plan ID: PLAN-007
📝 Plan Name: Full Property Onboarding
...
📋 Execution Steps:
  Step 1: [scout] Create CRM property record
  Step 2: [scout] Verify EPC certificate
  Step 3: [compliance] Run AML checks
  Step 4: [content] Generate property description
  Step 5: [intelligence] Match buyers from database
  Step 6: [compliance] Validate description
  Step 7: [orchestrator] Schedule property launch
```
**Expected Output:**
```json
{
    "status": "completed",
    "results": {
        "steps_completed": [
            {"step": 1, "result": {"status": "success", "record_id": "..."}},
            {"step": 2, "result": {"status": "success", "epc_valid": true}},
            {"step": 3, "result": {"status": "success", "aml_passed": true}},
            {"step": 4, "result": {"status": "success", "word_count": 170}},
            {"step": 5, "result": {"status": "success", "matches_found": 15}},
            {"step": 6, "result": {"status": "success", "approved": true}},
            {"step": 7, "result": {"status": "success"}}
        ]
    }
}
```

---

### C009: Offer Qualification
**Input:**
```
POST /query
{
    "query": "New offer received: £275,000 from Michael Brown for 47 Oak Road - verify buyer",
    "context": {"property_id": "PROP-2024-5678", "buyer_id": "BUY-2024-3001", "offer_amount": 275000},
    "require_approval": true
}
```
**Expected Steps:**
```
Step 1: [scout] Get buyer details
Step 2: [compliance] Verify proof of funds
Step 3: [scout] Check chain status
Step 4: [intelligence] Score buyer strength
Step 5: [content] Prepare offer presentation
```
**Expected Output:**
```json
{
    "status": "completed",
    "results": {
        "steps_completed": [
            {"step": 1, "result": {"status": "success", "data": {"buyer_type": "chain_free_cash"}}},
            {"step": 2, "result": {"status": "success", "funds_verified": true}},
            {"step": 3, "result": {"status": "success", "chain_status": "chain_free"}},
            {"step": 4, "result": {"status": "success", "score": 95, "rating": "EXCELLENT"}},
            {"step": 5, "result": {"status": "success", "content": "..."}}
        ]
    }
}
```

---

## EDGE CASE TESTS (E001-E011)

### E001: Invalid Property ID
**Input:**
```
POST /agents/scout
{
    "action": "Get property",
    "context": {"property_id": "INVALID-999"}
}
```
**Expected Output:**
```json
{
    "status": "success",
    "type": "llm_response",
    "response": "..."
}
```
*Note: Returns LLM response when data not found*

---

### E004: Missing Property ID
**Input:**
```
POST /agents/content
{
    "action": "Generate description",
    "context": {}
}
```
**Expected Output:**
```json
{
    "status": "error",
    "message": "No property_id provided"
}
```

---

### E007: Empty Query
**Input:**
```
POST /query
{
    "query": "",
    "require_approval": false
}
```
**Expected Output:**
```json
{
    "status": "completed",
    "plan": {
        "plan_id": "CUSTOM",
        "plan_name": "Custom Workflow",
        ...
    }
}
```

---

## VERIFICATION CHECKLIST

### For Each Test, Verify:

| Check | Description |
|-------|-------------|
| ✅ Status | Response has `"status": "success"` or `"status": "completed"` |
| ✅ No Errors | No `"error"` key in response |
| ✅ Data Present | Expected data fields are populated |
| ✅ Correct Types | Numbers are numbers, strings are strings |
| ✅ Valid IDs | IDs match format (PROP-XXXX, BUY-XXXX, etc.) |
| ✅ Time Reasonable | Response time < 30 seconds for simple, < 60 for complex |

### Quick Verification Commands:

```bash
# Check health
curl http://localhost:8000/health

# Check property exists
curl http://localhost:8000/data/properties/PROP-2024-5678

# Check buyer matching works
curl -X POST http://localhost:8000/agents/intelligence \
  -H "Content-Type: application/json" \
  -d '{"action": "Match buyers", "context": {"property_id": "PROP-2024-5678"}}'

# Check AML works
curl -X POST http://localhost:8000/agents/compliance \
  -H "Content-Type: application/json" \
  -d '{"action": "AML check", "context": {"vendor_id": "VEN-001"}}'
```

---

## TROUBLESHOOTING

| Issue | Cause | Fix |
|-------|-------|-----|
| `"error": "Connection failed"` | Server not running | Run `python main.py` |
| `"Error calling LLM"` | API key issue | Check `.env` file |
| `"status": "rejected"` | Human said "no" | Type "yes" at prompt |
| Empty `data` | ID not found | Check CSV files exist |
| Timeout | LLM slow | Wait or retry |
