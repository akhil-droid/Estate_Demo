"""
UK Estate Agency AI - Data Loader
=================================
Handles loading and searching CSV data files.
"""

import os
import pandas as pd
from typing import Dict, List, Optional


# CSV Data Paths - Update these to match your folder structure
DATA_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "demo_mock_data")

CSV_PATHS = {
    "properties": os.path.join(DATA_BASE_PATH, "entities", "properties.csv"),
    "vendors": os.path.join(DATA_BASE_PATH, "entities", "vendors.csv"),
    "buyers": os.path.join(DATA_BASE_PATH, "entities", "buyers.csv"),
    "employees": os.path.join(DATA_BASE_PATH, "entities", "employees.csv"),
    "solicitors": os.path.join(DATA_BASE_PATH, "entities", "solicitors.csv"),
    "ai_agents": os.path.join(DATA_BASE_PATH, "entities", "ai_agents.csv"),
    "lookup_tables": os.path.join(DATA_BASE_PATH, "entities", "lookup_tables.csv"),
    "query_bank": os.path.join(DATA_BASE_PATH, "query_bank", "query_bank_full.csv"),
    "execution_plans": os.path.join(DATA_BASE_PATH, "execution_plans", "execution_plans_summary.csv"),
    "execution_steps": os.path.join(DATA_BASE_PATH, "execution_plans", "execution_steps_detailed.csv"),
    "happy_paths": os.path.join(DATA_BASE_PATH, "demo_scenarios", "happy_paths.csv"),
    "edge_cases": os.path.join(DATA_BASE_PATH, "demo_scenarios", "edge_cases.csv"),
    "error_recovery": os.path.join(DATA_BASE_PATH, "demo_scenarios", "error_recovery.csv"),
    "showcase": os.path.join(DATA_BASE_PATH, "demo_scenarios", "showcase_multistage.csv"),
    "agent_scripts": os.path.join(DATA_BASE_PATH, "agent_interaction_scripts", "agent_interaction_scripts.csv"),
    "metrics": os.path.join(DATA_BASE_PATH, "metrics_dashboard", "metrics_dashboard.csv"),
}


class DataLoader:
    """Loads and caches CSV data for agents to use."""
    
    _cache: Dict[str, pd.DataFrame] = {}
    
    @classmethod
    def load(cls, name: str) -> pd.DataFrame:
        """Load CSV data by name, with caching."""
        if name not in cls._cache:
            path = CSV_PATHS.get(name)
            if path and os.path.exists(path):
                try:
                    # Try UTF-8 first, then fall back to latin-1
                    try:
                        df = pd.read_csv(path, encoding='utf-8')
                    except UnicodeDecodeError:
                        df = pd.read_csv(path, encoding='latin-1')
                    
                    # Replace NaN with None for JSON compatibility
                    df = df.where(pd.notnull(df), None)
                    
                    cls._cache[name] = df
                    print(f"📂 Loaded: {name} ({len(cls._cache[name])} records)")
                except Exception as e:
                    print(f"❌ Error loading {name}: {str(e)}")
                    cls._cache[name] = pd.DataFrame()
            else:
                print(f"⚠️ File not found: {name} at {path}")
                cls._cache[name] = pd.DataFrame()
        return cls._cache[name]
    
    @classmethod
    def reload(cls, name: str = None) -> None:
        """Reload CSV data, clearing cache."""
        if name:
            if name in cls._cache:
                del cls._cache[name]
            cls.load(name)
        else:
            cls._cache.clear()
            print("🔄 Cache cleared. Data will reload on next access.")
    
    @classmethod
    def get_property(cls, property_id: str) -> Dict:
        """Get property by ID."""
        df = cls.load("properties")
        if df.empty:
            return {}
        row = df[df["property_id"] == property_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def get_vendor(cls, vendor_id: str) -> Dict:
        """Get vendor by ID."""
        df = cls.load("vendors")
        if df.empty:
            return {}
        row = df[df["vendor_id"] == vendor_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def get_buyer(cls, buyer_id: str) -> Dict:
        """Get buyer by ID."""
        df = cls.load("buyers")
        if df.empty:
            return {}
        row = df[df["buyer_id"] == buyer_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def get_employee(cls, employee_id: str) -> Dict:
        """Get employee by ID."""
        df = cls.load("employees")
        if df.empty:
            return {}
        row = df[df["employee_id"] == employee_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def get_solicitor(cls, solicitor_id: str) -> Dict:
        """Get solicitor by ID."""
        df = cls.load("solicitors")
        if df.empty:
            return {}
        row = df[df["solicitor_id"] == solicitor_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def get_execution_plan(cls, plan_id: str) -> Dict:
        """Get execution plan by ID."""
        df = cls.load("execution_plans")
        if df.empty:
            return {}
        row = df[df["plan_id"] == plan_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def get_execution_steps(cls, plan_id: str) -> List[Dict]:
        """Get execution steps for a plan."""
        df = cls.load("execution_steps")
        if df.empty:
            return []
        rows = df[df["plan_id"] == plan_id]
        return rows.to_dict("records")
    
    @classmethod
    def get_query_by_id(cls, query_id: str) -> Dict:
        """Get query from query bank by ID."""
        df = cls.load("query_bank")
        if df.empty:
            return {}
        row = df[df["query_id"] == query_id]
        return row.to_dict("records")[0] if len(row) > 0 else {}
    
    @classmethod
    def search_properties(cls, criteria: Dict) -> List[Dict]:
        """Search properties based on criteria."""
        df = cls.load("properties")
        if df.empty:
            return []
        result = df.copy()
        
        if "min_price" in criteria:
            result = result[result["asking_price"] >= criteria["min_price"]]
        if "max_price" in criteria:
            result = result[result["asking_price"] <= criteria["max_price"]]
        if "bedrooms" in criteria:
            result = result[result["bedrooms"] == criteria["bedrooms"]]
        if "min_bedrooms" in criteria:
            result = result[result["bedrooms"] >= criteria["min_bedrooms"]]
        if "max_bedrooms" in criteria:
            result = result[result["bedrooms"] <= criteria["max_bedrooms"]]
        if "status" in criteria:
            result = result[result["status"] == criteria["status"]]
        if "property_type" in criteria:
            result = result[result["property_type"] == criteria["property_type"]]
        if "postcode_prefix" in criteria:
            result = result[result["postcode"].str.startswith(criteria["postcode_prefix"])]
            
        return result.to_dict("records")
    
    @classmethod
    def search_buyers(cls, criteria: Dict) -> List[Dict]:
        """Search buyers based on criteria."""
        df = cls.load("buyers")
        if df.empty:
            return []
        result = df.copy()
        
        if "min_budget" in criteria:
            result = result[result["max_budget"] >= criteria["min_budget"]]
        if "max_budget" in criteria:
            result = result[result["max_budget"] <= criteria["max_budget"]]
        if "buyer_type" in criteria:
            result = result[result["buyer_type"] == criteria["buyer_type"]]
        if "priority_level" in criteria:
            result = result[result["priority_level"] == criteria["priority_level"]]
        if "financial_status" in criteria:
            result = result[result["financial_status"] == criteria["financial_status"]]
            
        return result.to_dict("records")
    
    @classmethod
    def search_vendors(cls, criteria: Dict) -> List[Dict]:
        """Search vendors based on criteria."""
        df = cls.load("vendors")
        if df.empty:
            return []
        result = df.copy()
        
        if "aml_status" in criteria:
            result = result[result["aml_status"] == criteria["aml_status"]]
        if "chain_status" in criteria:
            result = result[result["chain_status"] == criteria["chain_status"]]
        if "timeline" in criteria:
            result = result[result["timeline"] == criteria["timeline"]]
            
        return result.to_dict("records")
    
    @classmethod
    def get_all_properties(cls) -> List[Dict]:
        """Get all properties."""
        df = cls.load("properties")
        if df.empty:
            return []
        # Convert to records and handle NaN
        records = df.to_dict("records")
        return [{k: (None if pd.isna(v) else v) for k, v in r.items()} for r in records]
    
    @classmethod
    def get_all_buyers(cls) -> List[Dict]:
        """Get all buyers."""
        df = cls.load("buyers")
        if df.empty:
            return []
        records = df.to_dict("records")
        return [{k: (None if pd.isna(v) else v) for k, v in r.items()} for r in records]
    
    @classmethod
    def get_all_vendors(cls) -> List[Dict]:
        """Get all vendors."""
        df = cls.load("vendors")
        if df.empty:
            return []
        records = df.to_dict("records")
        return [{k: (None if pd.isna(v) else v) for k, v in r.items()} for r in records]
    
    @classmethod
    def get_all_employees(cls) -> List[Dict]:
        """Get all employees."""
        df = cls.load("employees")
        if df.empty:
            return []
        records = df.to_dict("records")
        return [{k: (None if pd.isna(v) else v) for k, v in r.items()} for r in records]
    
    @classmethod
    def get_active_properties(cls) -> List[Dict]:
        """Get all active properties."""
        return cls.search_properties({"status": "active"})
    
    @classmethod
    def get_hot_buyers(cls) -> List[Dict]:
        """Get all hot priority buyers."""
        return cls.search_buyers({"priority_level": "hot"})
    
    @classmethod
    def get_metrics(cls) -> List[Dict]:
        """Get all metrics."""
        df = cls.load("metrics")
        if df.empty:
            return []
        records = df.to_dict("records")
        return [{k: (None if pd.isna(v) else v) for k, v in r.items()} for r in records]


# Test function
if __name__ == "__main__":
    print("\n🔍 Testing DataLoader...\n")
    
    # Test loading
    props = DataLoader.get_all_properties()
    print(f"Properties loaded: {len(props)}")
    
    buyers = DataLoader.get_all_buyers()
    print(f"Buyers loaded: {len(buyers)}")
    
    # Test specific lookup
    prop = DataLoader.get_property("PROP-2024-5678")
    print(f"\nProperty PROP-2024-5678: {prop.get('address_line1', 'Not found')}")
    
    # Test search
    results = DataLoader.search_properties({"min_price": 300000, "max_price": 400000})
    print(f"\nProperties £300k-£400k: {len(results)}")