"""
UK Estate Agency AI - API
=========================
FastAPI routes and endpoints for the multi-agent system.
"""

from typing import Optional, Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents import AgentManager
from data_loader import DataLoader


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="UK Estate Agency AI - Multi-Agent System",
    description="AI-powered estate agency automation with human-in-the-loop approval",
    version="1.0.0"
)

# Initialize agent manager
agent_manager = AgentManager()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for processing a query."""
    query: str
    context: Optional[Dict] = None
    require_approval: bool = True


class QueryResponse(BaseModel):
    """Response model for query results."""
    status: str
    plan: Optional[Dict] = None
    results: Optional[Dict] = None
    message: Optional[str] = None


class AgentActionRequest(BaseModel):
    """Request model for direct agent actions."""
    action: str
    context: Optional[Dict] = None


class SearchRequest(BaseModel):
    """Request model for search operations."""
    criteria: Dict


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check and service info."""
    return {
        "status": "running",
        "service": "UK Estate Agency AI - Multi-Agent System",
        "version": "1.0.0",
        "agents": ["Orchestrator", "Scout", "Intelligence", "Content", "Compliance"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/debug/data")
async def debug_data():
    """Debug endpoint to check data loading status."""
    import os
    
    # Use DataLoader directly (already imported at top)
    base_path = os.path.join(os.path.dirname(__file__), "..", "demo_mock_data")
    
    status = {
        "data_base_path": os.path.abspath(base_path),
        "data_base_exists": os.path.exists(base_path),
        "files": {}
    }
    
    # Check key files
    key_files = ["properties", "vendors", "buyers", "employees", "execution_plans"]
    
    for name in key_files:
        try:
            df = DataLoader.load(name)
            status["files"][name] = {
                "loaded": True,
                "records": len(df),
                "columns": list(df.columns)[:5] if not df.empty else []
            }
        except Exception as e:
            status["files"][name] = {
                "loaded": False,
                "error": str(e)
            }
    
    return status


@app.get("/agents")
async def list_agents():
    """List all available agents."""
    return {
        "agents": agent_manager.list_agents()
    }


# ============================================================================
# MAIN QUERY ENDPOINT
# ============================================================================

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query through the multi-agent system.
    
    - Orchestrator analyzes the query and creates an execution plan
    - Plan is displayed in terminal for human approval
    - On approval, agents execute the plan
    - Results are returned
    """
    try:
        result = agent_manager.process_query(
            query=request.query,
            context=request.context,
            require_approval=request.require_approval
        )
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DIRECT AGENT ENDPOINTS
# ============================================================================

@app.post("/agents/scout")
async def scout_action(request: AgentActionRequest):
    """Direct call to Scout agent."""
    try:
        result = agent_manager.scout.execute(request.action, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/intelligence")
async def intelligence_action(request: AgentActionRequest):
    """Direct call to Intelligence agent."""
    try:
        result = agent_manager.intelligence.execute(request.action, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/content")
async def content_action(request: AgentActionRequest):
    """Direct call to Content agent."""
    try:
        result = agent_manager.content.execute(request.action, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/compliance")
async def compliance_action(request: AgentActionRequest):
    """Direct call to Compliance agent."""
    try:
        result = agent_manager.compliance.execute(request.action, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DATA ENDPOINTS
# ============================================================================

@app.get("/data/properties")
async def get_all_properties():
    """Get all properties."""
    try:
        data = DataLoader.get_all_properties()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading properties: {str(e)}")


@app.get("/data/properties/{property_id}")
async def get_property(property_id: str):
    """Get a specific property by ID."""
    try:
        data = DataLoader.get_property(property_id)
        if not data:
            raise HTTPException(status_code=404, detail="Property not found")
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/data/properties/search")
async def search_properties(request: SearchRequest):
    """Search properties by criteria."""
    try:
        results = DataLoader.search_properties(request.criteria)
        return {"count": len(results), "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/data/buyers")
async def get_all_buyers():
    """Get all buyers."""
    try:
        data = DataLoader.get_all_buyers()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading buyers: {str(e)}")


@app.get("/data/buyers/{buyer_id}")
async def get_buyer(buyer_id: str):
    """Get a specific buyer by ID."""
    try:
        data = DataLoader.get_buyer(buyer_id)
        if not data:
            raise HTTPException(status_code=404, detail="Buyer not found")
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/data/buyers/search")
async def search_buyers(request: SearchRequest):
    """Search buyers by criteria."""
    try:
        results = DataLoader.search_buyers(request.criteria)
        return {"count": len(results), "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/data/buyers/hot")
async def get_hot_buyers():
    """Get all hot priority buyers."""
    try:
        data = DataLoader.get_hot_buyers()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/data/vendors")
async def get_all_vendors():
    """Get all vendors."""
    try:
        data = DataLoader.get_all_vendors()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading vendors: {str(e)}")


@app.get("/data/vendors/{vendor_id}")
async def get_vendor(vendor_id: str):
    """Get a specific vendor by ID."""
    try:
        data = DataLoader.get_vendor(vendor_id)
        if not data:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/data/employees")
async def get_all_employees():
    """Get all employees."""
    try:
        data = DataLoader.get_all_employees()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading employees: {str(e)}")


@app.get("/data/employees/{employee_id}")
async def get_employee(employee_id: str):
    """Get a specific employee by ID."""
    try:
        data = DataLoader.get_employee(employee_id)
        if not data:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# EXECUTION PLAN ENDPOINTS
# ============================================================================

@app.get("/plans")
async def get_all_plans():
    """Get all execution plans."""
    try:
        df = DataLoader.load("execution_plans")
        if df.empty:
            return {"data": []}
        return {"data": df.to_dict("records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading plans: {str(e)}")


@app.get("/plans/{plan_id}")
async def get_plan(plan_id: str):
    """Get a specific execution plan by ID."""
    try:
        data = DataLoader.get_execution_plan(plan_id)
        if not data:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        steps = DataLoader.get_execution_steps(plan_id)
        data["steps"] = steps
        
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/plans/{plan_id}/steps")
async def get_plan_steps(plan_id: str):
    """Get execution steps for a plan."""
    try:
        steps = DataLoader.get_execution_steps(plan_id)
        return {"plan_id": plan_id, "count": len(steps), "steps": steps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# HISTORY ENDPOINT
# ============================================================================

@app.get("/history")
async def get_execution_history():
    """Get execution history."""
    return {"history": agent_manager.execution_history}


@app.delete("/history")
async def clear_history():
    """Clear execution history."""
    agent_manager.execution_history.clear()
    return {"status": "cleared"}


# ============================================================================
# METRICS ENDPOINT
# ============================================================================

@app.get("/metrics")
async def get_metrics():
    """Get all metrics."""
    try:
        data = DataLoader.get_metrics()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading metrics: {str(e)}")