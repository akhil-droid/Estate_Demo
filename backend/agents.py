"""
UK Estate Agency AI - Agents
============================
All AI agents: Orchestrator, Scout, Intelligence, Content, Compliance
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from data_loader import DataLoader

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o"  # or "gpt-4-turbo" or "gpt-3.5-turbo"


# ============================================================================
# HUMAN APPROVAL HANDLER
# ============================================================================

class HumanApproval:
    """Handles human-in-the-loop approval via terminal."""
    
    @staticmethod
    def request_approval(plan: Dict) -> bool:
        """
        Display plan and wait for human approval via terminal.
        Returns True if approved, False if rejected.
        """
        print("\n" + "=" * 70)
        print("🎯 ORCHESTRATOR EXECUTION PLAN - AWAITING APPROVAL")
        print("=" * 70)
        
        print(f"\n📋 Plan ID: {plan.get('plan_id', 'N/A')}")
        print(f"📝 Plan Name: {plan.get('plan_name', 'N/A')}")
        print(f"📄 Description: {plan.get('description', 'N/A')}")
        print(f"\n⏱️  Estimated Time: {plan.get('estimated_time_ms', 0)}ms")
        print(f"💰 Estimated Cost: ${plan.get('estimated_cost_usd', 0):.2f}")
        print(f"🤖 Agents Required: {plan.get('agents_required', 'N/A')}")
        print(f"📊 Total Steps: {plan.get('total_steps', 0)}")
        print(f"⚡ Parallel Groups: {plan.get('parallel_groups', 0)}")
        
        steps = plan.get("steps", [])
        if steps:
            print(f"\n📋 Execution Steps:")
            print("-" * 50)
            for step in steps:
                step_num = step.get('step_number', step.get('step', '?'))
                agent = step.get('assigned_agent', step.get('agent', '?'))
                action = step.get('action', '?')
                print(f"  Step {step_num}: [{agent}] {action}")
        
        print("\n" + "-" * 70)
        
        while True:
            response = input("👤 Do you approve this plan? (yes/no/modify): ").strip().lower()
            
            if response in ["yes", "y", "proceed", "approve"]:
                print("✅ Plan APPROVED. Proceeding with execution...\n")
                return True
            elif response in ["no", "n", "reject", "cancel"]:
                print("❌ Plan REJECTED. Execution cancelled.\n")
                return False
            elif response in ["modify", "m", "edit"]:
                print("📝 Modification requested. (Feature coming soon)")
                continue
            else:
                print("⚠️  Please enter 'yes' to approve or 'no' to reject.")


# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class BaseAgent:
    """Base class for all AI agents."""
    
    def __init__(self, name: str, emoji: str, role: str, system_prompt: str):
        self.name = name
        self.emoji = emoji
        self.role = role
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict] = []
    
    def call_llm(self, user_message: str, temperature: float = 0.7) -> str:
        """Make a call to the OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def log(self, message: str):
        """Log agent activity."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.emoji} {self.name}: {message}")


# ============================================================================
# ORCHESTRATOR AGENT
# ============================================================================

class OrchestratorAgent(BaseAgent):
    """
    Central coordinator that analyzes queries, creates execution plans,
    and coordinates other agents.
    """
    
    def __init__(self):
        system_prompt = """You are the Orchestrator Agent for a UK Estate Agency AI system.

Your role is to:
1. Analyze incoming queries and understand the intent
2. Identify which workflow and execution plan to use
3. Determine which agents are needed (Scout, Intelligence, Content, Compliance)
4. Create a step-by-step execution plan
5. Coordinate the execution of the plan

Available Agents:
- Scout 🔍: Data retrieval, API calls, database searches, CRM operations
- Intelligence 🧠: Analysis, scoring, pattern recognition, buyer matching
- Content ✍️: Writing descriptions, emails, reports, marketing copy
- Compliance ✅: Validation, AML checks, regulatory compliance, EPC verification

Available Execution Plans:
- PLAN-001: Inbound Lead Capture
- PLAN-002: Portal Enquiry Response
- PLAN-003: Buyer Qualification
- PLAN-004: Pre-Valuation Research
- PLAN-005: Instant Valuation
- PLAN-006: Post-Valuation Follow-up
- PLAN-007: Full Property Onboarding (complex)
- PLAN-008: EPC Verification
- PLAN-009: AML Compliance Check
- PLAN-010: Property Description Generation
- PLAN-011: Property Launch
- PLAN-012: Buyer Database Matching
- PLAN-013: Portal Analytics Review
- PLAN-014: Immediate Enquiry Response
- PLAN-015: Viewing Preparation
- PLAN-016: Feedback Collection
- PLAN-017: Daily Feedback Aggregation
- PLAN-018: Weekly Vendor Report
- PLAN-019: Price Reduction Processing
- PLAN-020: Offer Qualification
- PLAN-021: Offer Presentation
- PLAN-022: Sale Agreed Workflow
- PLAN-023: MoS Generation & Distribution
- PLAN-024: Sales Progression Tracking
- PLAN-025: Completion & Post-Completion

When analyzing a query, respond with a JSON object containing:
{
    "intent": "description of what the query is asking",
    "workflow_type": "the type of workflow needed",
    "plan_id": "the execution plan ID to use (e.g., PLAN-001)",
    "plan_name": "name of the plan",
    "agents_required": ["list", "of", "agents"],
    "steps": [
        {"step": 1, "agent": "agent_name", "action": "what to do"},
        ...
    ],
    "estimated_time_ms": 5000,
    "estimated_cost_usd": 0.50,
    "human_approval_required": true/false,
    "reason_for_human_approval": "why human input is needed (if applicable)",
    "entities_involved": {
        "property_id": "if applicable",
        "vendor_id": "if applicable",
        "buyer_id": "if applicable"
    }
}

Always respond with valid JSON only. No markdown, no explanation."""

        super().__init__(
            name="Orchestrator",
            emoji="🎯",
            role="Central Coordinator",
            system_prompt=system_prompt
        )
    
    def analyze_query(self, query: str, context: Dict = None) -> Dict:
        """Analyze the incoming query and create an execution plan."""
        self.log(f"Analyzing query: {query}")
        
        context_str = ""
        if context:
            context_str = f"\n\nContext provided:\n{json.dumps(context, indent=2)}"
        
        plans_df = DataLoader.load("execution_plans")
        if not plans_df.empty:
            plans_summary = plans_df[["plan_id", "plan_name", "workflow_type", "agents_required"]].head(25).to_string()
        else:
            plans_summary = "No plans loaded"
        
        prompt = f"""Analyze this query and create an execution plan:

QUERY: {query}

AVAILABLE EXECUTION PLANS:
{plans_summary}
{context_str}

Respond with a JSON execution plan."""

        response = self.call_llm(prompt, temperature=0.3)
        
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            plan = json.loads(response.strip())
            self.log(f"Plan created: {plan.get('plan_id', 'Custom Plan')}")
            return plan
            
        except json.JSONDecodeError:
            self.log("Failed to parse plan, using default structure")
            return {
                "intent": query,
                "workflow_type": "custom",
                "plan_id": "CUSTOM",
                "plan_name": "Custom Workflow",
                "agents_required": ["orchestrator"],
                "steps": [{"step": 1, "agent": "orchestrator", "action": "Process query"}],
                "estimated_time_ms": 5000,
                "estimated_cost_usd": 0.10,
                "human_approval_required": True,
                "raw_response": response
            }
    
    def execute_plan(self, plan: Dict, agents: Dict) -> Dict:
        """Execute the approved plan by coordinating agents."""
        self.log("Starting plan execution...")
        
        results = {
            "plan_id": plan.get("plan_id"),
            "started_at": datetime.now().isoformat(),
            "steps_completed": [],
            "final_output": None,
            "status": "in_progress"
        }
        
        steps = plan.get("steps", [])
        context = plan.get("context", {})
        
        entities = plan.get("entities_involved", {})
        context.update(entities)
        
        for step in steps:
            step_num = step.get("step", 0)
            agent_name = step.get("agent", "").lower()
            action = step.get("action", "")
            
            self.log(f"Executing Step {step_num}: [{agent_name}] {action}")
            
            if agent_name == "scout" and "scout" in agents:
                result = agents["scout"].execute(action, context)
            elif agent_name == "intelligence" and "intelligence" in agents:
                result = agents["intelligence"].execute(action, context)
            elif agent_name == "content" and "content" in agents:
                result = agents["content"].execute(action, context)
            elif agent_name == "compliance" and "compliance" in agents:
                result = agents["compliance"].execute(action, context)
            else:
                result = {"status": "skipped", "reason": f"Agent {agent_name} not available"}
            
            results["steps_completed"].append({
                "step": step_num,
                "agent": agent_name,
                "action": action,
                "result": result
            })
            
            context[f"step_{step_num}_result"] = result
        
        results["completed_at"] = datetime.now().isoformat()
        results["status"] = "completed"
        
        self.log("Plan execution completed!")
        return results


# ============================================================================
# SCOUT AGENT
# ============================================================================

class ScoutAgent(BaseAgent):
    """Data retrieval specialist."""
    
    def __init__(self):
        system_prompt = """You are the Scout Agent for a UK Estate Agency AI system.

Your role is to:
1. Search and retrieve property data from the database
2. Look up vendor and buyer information
3. Verify EPC certificates and other documents
4. Query external APIs (Land Registry, EPC Register, etc.)
5. Create and update CRM records
6. Perform address validation and lookups

Always be thorough and accurate in data retrieval."""

        super().__init__(
            name="Scout",
            emoji="🔍",
            role="Data Retrieval Specialist",
            system_prompt=system_prompt
        )
    
    def execute(self, action: str, context: Dict = None) -> Dict:
        """Execute a scout action."""
        self.log(f"Executing: {action}")
        
        action_lower = action.lower()
        context = context or {}
        
        if "property" in action_lower:
            if "property_id" in context:
                data = DataLoader.get_property(context["property_id"])
                if data:
                    return {"status": "success", "type": "property", "data": data}
            if "search" in action_lower:
                criteria = context.get("search_criteria", {})
                properties = DataLoader.search_properties(criteria)
                return {"status": "success", "type": "property_search", "count": len(properties), "data": properties[:10]}
        
        if "vendor" in action_lower and "vendor_id" in context:
            data = DataLoader.get_vendor(context["vendor_id"])
            if data:
                return {"status": "success", "type": "vendor", "data": data}
        
        if "buyer" in action_lower:
            if "buyer_id" in context:
                data = DataLoader.get_buyer(context["buyer_id"])
                if data:
                    return {"status": "success", "type": "buyer", "data": data}
            if "search" in action_lower or "match" in action_lower:
                criteria = context.get("search_criteria", {})
                buyers = DataLoader.search_buyers(criteria)
                return {"status": "success", "type": "buyer_search", "count": len(buyers), "data": buyers[:10]}
        
        if "epc" in action_lower and "property_id" in context:
            prop = DataLoader.get_property(context["property_id"])
            if prop:
                return {
                    "status": "success",
                    "type": "epc_verification",
                    "epc_rating": prop.get("epc_rating", "Unknown"),
                    "epc_expiry": prop.get("epc_expiry", "Unknown"),
                    "valid": True
                }
        
        if "crm" in action_lower or "record" in action_lower:
            return {
                "status": "success",
                "type": "crm_operation",
                "record_id": f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
        
        if "portal" in action_lower:
            return {
                "status": "success",
                "type": "portal_operation",
                "portals_updated": ["rightmove", "zoopla", "onthemarket"]
            }
        
        response = self.call_llm(f"Execute: {action}\n\nContext: {json.dumps(context)}")
        return {"status": "success", "type": "llm_response", "response": response}


# ============================================================================
# INTELLIGENCE AGENT
# ============================================================================

class IntelligenceAgent(BaseAgent):
    """Analysis and scoring specialist."""
    
    def __init__(self):
        system_prompt = """You are the Intelligence Agent for a UK Estate Agency AI system.

Your role is to:
1. Analyze property and buyer data to find matches
2. Score buyer-property compatibility (0-100)
3. Assess market positioning and pricing
4. Identify patterns in feedback data
5. Generate strategic recommendations
6. Assess risk levels for transactions

Always provide data-driven insights with confidence scores."""

        super().__init__(
            name="Intelligence",
            emoji="🧠",
            role="Analysis & Scoring Specialist",
            system_prompt=system_prompt
        )
    
    def execute(self, action: str, context: Dict = None) -> Dict:
        """Execute an intelligence action."""
        self.log(f"Executing: {action}")
        
        action_lower = action.lower()
        context = context or {}
        
        if "match" in action_lower and "buyer" in action_lower:
            return self._match_buyers(context)
        
        if "risk" in action_lower or "assess" in action_lower:
            return self._assess_risk(context)
        
        if "price" in action_lower or "valuation" in action_lower:
            return self._analyze_price(context)
        
        if "score" in action_lower:
            return {"status": "success", "type": "scoring", "score": 85, "confidence": 0.9}
        
        response = self.call_llm(f"Analyze: {action}\n\nContext: {json.dumps(context)}")
        return {"status": "success", "type": "llm_analysis", "analysis": response}
    
    def _match_buyers(self, context: Dict) -> Dict:
        """Match buyers to a property."""
        if "property_id" in context:
            prop = DataLoader.get_property(context["property_id"])
            if prop:
                asking = prop.get("asking_price", 0)
                criteria = {"min_budget": int(asking * 0.9), "max_budget": int(asking * 1.2)}
                buyers = DataLoader.search_buyers(criteria)
                
                scored = []
                for buyer in buyers[:15]:
                    score = self._calculate_match_score(prop, buyer)
                    scored.append({
                        "buyer_id": buyer.get("buyer_id"),
                        "name": f"{buyer.get('first_name', '')} {buyer.get('last_name', '')}",
                        "score": score,
                        "buyer_type": buyer.get("buyer_type"),
                        "priority": buyer.get("priority_level")
                    })
                
                scored.sort(key=lambda x: x["score"], reverse=True)
                return {
                    "status": "success",
                    "type": "buyer_matching",
                    "matches_found": len(scored),
                    "top_matches": scored[:5]
                }
        return {"status": "error", "message": "No property_id provided"}
    
    def _calculate_match_score(self, property: Dict, buyer: Dict) -> int:
        """Calculate match score."""
        score = 50
        asking = property.get("asking_price", 0)
        budget = buyer.get("max_budget", 0)
        
        if budget >= asking:
            score += 20
        elif budget >= asking * 0.95:
            score += 10
        
        buyer_type = buyer.get("buyer_type", "")
        if buyer_type == "chain_free_cash":
            score += 20
        elif buyer_type == "first_time_buyer":
            score += 15
        
        if buyer.get("priority_level") == "hot":
            score += 10
        
        return min(score, 100)
    
    def _assess_risk(self, context: Dict) -> Dict:
        """Assess transaction risk."""
        risk_score = 20
        factors = []
        
        if "buyer_id" in context:
            buyer = DataLoader.get_buyer(context["buyer_id"])
            if buyer:
                if buyer.get("buyer_type") == "chain_free_cash":
                    factors.append("✅ Chain-free cash buyer")
                else:
                    risk_score += 20
                    factors.append("⚠️ Chain buyer")
        
        risk_level = "LOW" if risk_score < 40 else "MEDIUM" if risk_score < 60 else "HIGH"
        return {"status": "success", "risk_level": risk_level, "risk_score": risk_score, "factors": factors}
    
    def _analyze_price(self, context: Dict) -> Dict:
        """Analyze property pricing."""
        if "property_id" in context:
            prop = DataLoader.get_property(context["property_id"])
            if prop:
                asking = prop.get("asking_price", 0)
                return {
                    "status": "success",
                    "asking_price": asking,
                    "estimated_range": {"low": int(asking * 0.95), "high": int(asking * 1.05)},
                    "market_position": "competitive"
                }
        return {"status": "error", "message": "No property_id provided"}


# ============================================================================
# CONTENT AGENT
# ============================================================================

class ContentAgent(BaseAgent):
    """Content generation specialist."""
    
    def __init__(self):
        system_prompt = """You are the Content Agent for a UK Estate Agency AI system.

Your role is to:
1. Write compelling property descriptions
2. Generate personalized email responses
3. Create vendor reports and updates
4. Write marketing copy for listings
5. Personalize communications based on recipient

Guidelines:
- Use professional but warm UK English
- Be accurate and avoid exaggerated claims
- Comply with Consumer Protection Regulations (CPR)
- Keep descriptions 150-200 words
- Always be helpful and professional"""

        super().__init__(
            name="Content",
            emoji="✍️",
            role="Content Generation Specialist",
            system_prompt=system_prompt
        )
    
    def execute(self, action: str, context: Dict = None) -> Dict:
        """Execute a content generation action."""
        self.log(f"Executing: {action}")
        
        action_lower = action.lower()
        context = context or {}
        
        if "description" in action_lower:
            return self._generate_description(context)
        
        if "email" in action_lower:
            return self._generate_email(context)
        
        if "report" in action_lower:
            return self._generate_report(context)
        
        response = self.call_llm(f"Generate content for: {action}\n\nContext: {json.dumps(context)}")
        return {"status": "success", "type": "llm_content", "content": response}
    
    def _generate_description(self, context: Dict) -> Dict:
        """Generate property description."""
        if "property_id" in context:
            prop = DataLoader.get_property(context["property_id"])
            if prop:
                prompt = f"""Write a property description for Rightmove (150-180 words):

Address: {prop.get('address_line1', 'Property')}
Type: {prop.get('property_type', 'House').replace('_', ' ').title()}
Bedrooms: {prop.get('bedrooms', 3)}
Price: £{prop.get('asking_price', 0):,}
Features: {prop.get('key_features', 'Modern property')}

No markdown or asterisks."""

                description = self.call_llm(prompt)
                return {
                    "status": "success",
                    "type": "property_description",
                    "word_count": len(description.split()),
                    "content": description
                }
        return {"status": "error", "message": "No property_id provided"}
    
    def _generate_email(self, context: Dict) -> Dict:
        """Generate email content."""
        buyer_name = context.get("buyer_name", "Customer")
        prompt = f"""Write a professional estate agency email to {buyer_name}.
Warm and professional tone. No markdown."""
        
        email = self.call_llm(prompt)
        return {"status": "success", "type": "email", "content": email}
    
    def _generate_report(self, context: Dict) -> Dict:
        """Generate vendor report."""
        if "property_id" in context:
            prop = DataLoader.get_property(context["property_id"])
            if prop:
                prompt = f"""Generate a weekly vendor report:

Property: {prop.get('address_line1', 'Property')}
Days on Market: {prop.get('days_on_market', 0)}
Viewings: {prop.get('total_viewings', 0)}
Enquiries: {prop.get('total_enquiries', 0)}

Concise summary with recommendations. No markdown."""

                report = self.call_llm(prompt)
                return {"status": "success", "type": "vendor_report", "content": report}
        return {"status": "error", "message": "No property_id provided"}


# ============================================================================
# COMPLIANCE AGENT
# ============================================================================

class ComplianceAgent(BaseAgent):
    """Compliance and validation specialist."""
    
    def __init__(self):
        system_prompt = """You are the Compliance Agent for a UK Estate Agency AI system.

Your role is to:
1. Perform AML (Anti-Money Laundering) checks
2. Validate content for regulatory compliance
3. Check for CPR violations
4. Verify EPC certificates
5. Issue compliance certificates

Always err on the side of caution with compliance matters."""

        super().__init__(
            name="Compliance",
            emoji="✅",
            role="Compliance & Validation Specialist",
            system_prompt=system_prompt
        )
    
    def execute(self, action: str, context: Dict = None) -> Dict:
        """Execute a compliance action."""
        self.log(f"Executing: {action}")
        
        action_lower = action.lower()
        context = context or {}
        
        if "aml" in action_lower:
            return self._check_aml(context)
        
        if "validate" in action_lower:
            return self._validate_content(context.get("content", ""))
        
        if "epc" in action_lower:
            return self._validate_epc(context)
        
        response = self.call_llm(f"Compliance check: {action}\n\nContext: {json.dumps(context)}")
        return {"status": "success", "type": "llm_compliance", "response": response}
    
    def _check_aml(self, context: Dict) -> Dict:
        """Perform AML checks."""
        if "vendor_id" in context:
            vendor = DataLoader.get_vendor(context["vendor_id"])
            if vendor:
                passed = all([
                    vendor.get("aml_status") == "verified",
                    vendor.get("pep_check") == "clear",
                    vendor.get("sanctions_check") == "clear"
                ])
                return {
                    "status": "success",
                    "aml_passed": passed,
                    "aml_status": vendor.get("aml_status"),
                    "certificate_id": vendor.get("aml_certificate_id", "")
                }
        return {"status": "error", "message": "No vendor_id provided"}
    
    def _validate_content(self, content: str) -> Dict:
        """Validate content for compliance."""
        if not content:
            return {"status": "error", "message": "No content provided"}
        
        prompt = f"""Review for UK property marketing compliance:

{content}

Respond: APPROVED or REJECTED with reasons."""

        validation = self.call_llm(prompt, temperature=0.3)
        approved = "APPROVED" in validation.upper().split('\n')[0]
        return {"status": "success", "approved": approved, "validation_result": validation}
    
    def _validate_epc(self, context: Dict) -> Dict:
        """Validate EPC certificate."""
        if "property_id" in context:
            prop = DataLoader.get_property(context["property_id"])
            if prop:
                expiry = prop.get("epc_expiry", "")
                valid = expiry > datetime.now().strftime("%Y-%m-%d") if expiry else False
                return {
                    "status": "success",
                    "epc_valid": valid,
                    "epc_rating": prop.get("epc_rating", ""),
                    "epc_expiry": expiry
                }
        return {"status": "error", "message": "No property_id provided"}


# ============================================================================
# AGENT MANAGER
# ============================================================================

class AgentManager:
    """Manages all agents and coordinates workflows."""
    
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.scout = ScoutAgent()
        self.intelligence = IntelligenceAgent()
        self.content = ContentAgent()
        self.compliance = ComplianceAgent()
        
        self.agents = {
            "orchestrator": self.orchestrator,
            "scout": self.scout,
            "intelligence": self.intelligence,
            "content": self.content,
            "compliance": self.compliance
        }
        
        self.execution_history: List[Dict] = []
    
    def process_query(self, query: str, context: Dict = None, require_approval: bool = True) -> Dict:
        """Process a query through the multi-agent system."""
        print("\n" + "=" * 70)
        print("🚀 NEW QUERY RECEIVED")
        print("=" * 70)
        print(f"Query: {query}")
        print("-" * 70)
        
        plan = self.orchestrator.analyze_query(query, context)
        plan["context"] = context or {}
        plan["original_query"] = query
        
        if require_approval:
            plan_details = {
                "plan_id": plan.get("plan_id", "CUSTOM"),
                "plan_name": plan.get("plan_name", "Custom Workflow"),
                "description": plan.get("intent", query),
                "estimated_time_ms": plan.get("estimated_time_ms", 5000),
                "estimated_cost_usd": plan.get("estimated_cost_usd", 0.50),
                "agents_required": ", ".join(plan.get("agents_required", ["orchestrator"])),
                "total_steps": len(plan.get("steps", [])),
                "parallel_groups": plan.get("parallel_groups", 1),
                "steps": plan.get("steps", [])
            }
            
            approved = HumanApproval.request_approval(plan_details)
            
            if not approved:
                return {"status": "rejected", "message": "Plan rejected", "plan": plan}
        
        results = self.orchestrator.execute_plan(plan, self.agents)
        
        self.execution_history.append({
            "query": query,
            "plan": plan,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
        return {"status": "completed", "plan": plan, "results": results}
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        return self.agents.get(name.lower())
    
    def list_agents(self) -> List[Dict]:
        """List all available agents."""
        return [{"name": a.name, "emoji": a.emoji, "role": a.role} for a in self.agents.values()]