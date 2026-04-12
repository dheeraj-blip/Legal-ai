"""CrewAI crew definitions for the Indian Law Query Assistant."""

import os

# Suppress CrewAI interactive prompts and telemetry
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_INTERACTIVE_MODE"] = "false"

from crewai import Crew, Process
from agents import (
    create_constitution_agent, create_ipc_agent, create_router_agent,
    create_cpc_agent, create_crpc_agent, create_divorce_agent,
    create_environ_agent, create_marriage_agent, create_mva_agent,
    create_evidence_agent, create_administrative_agent, create_banking_agent,
    create_bankruptcy_agent, create_company_law_agent, create_copyright_agent,
    create_corporate_practice_agent, create_design_law_agent, create_human_rights_agent,
    create_information_technology_agent, create_minimum_wages_agent, create_patent_agent,
    create_property_law_agent, create_tax_law_agent, create_trademark_law_agent
)
from tasks import (
    create_routing_task, create_constitution_query_task, create_ipc_query_task,
    create_cpc_query_task, create_crpc_query_task, create_divorce_query_task,
    create_environ_query_task, create_marriage_query_task, create_mva_query_task,
    create_evidence_query_task, create_administrative_query_task, create_banking_query_task,
    create_bankruptcy_query_task, create_company_law_query_task, create_copyright_query_task,
    create_corporate_practice_query_task, create_design_law_query_task, create_human_rights_query_task,
    create_information_technology_query_task, create_minimum_wages_query_task, create_patent_query_task,
    create_property_law_query_task, create_tax_law_query_task, create_trademark_law_query_task
)


def _classify_query(user_query: str) -> str:
    """Use the Router agent to classify the query as CONSTITUTION or IPC."""
    agent = create_router_agent()
    task = create_routing_task(agent, user_query)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )
    result = crew.kickoff()
    return str(result).strip().upper()


def _run_constitution_query(user_query: str) -> str:
    """Run the Constitution agent crew."""
    agent = create_constitution_agent()
    task = create_constitution_query_task(agent, user_query)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )
    result = crew.kickoff()
    return str(result)


def _run_ipc_query(user_query: str) -> str:
    """Run the IPC agent crew."""
    agent = create_ipc_agent()
    task = create_ipc_query_task(agent, user_query)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )
    result = crew.kickoff()
    return str(result)


def _run_cpc_query(user_query: str) -> str:
    agent = create_cpc_agent()
    task = create_cpc_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_crpc_query(user_query: str) -> str:
    agent = create_crpc_agent()
    task = create_crpc_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_divorce_query(user_query: str) -> str:
    agent = create_divorce_agent()
    task = create_divorce_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_environ_query(user_query: str) -> str:
    agent = create_environ_agent()
    task = create_environ_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_marriage_query(user_query: str) -> str:
    agent = create_marriage_agent()
    task = create_marriage_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_mva_query(user_query: str) -> str:
    agent = create_mva_agent()
    task = create_mva_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_evidence_query(user_query: str) -> str:
    agent = create_evidence_agent()
    task = create_evidence_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_administrative_query(user_query: str) -> str:
    agent = create_administrative_agent()
    task = create_administrative_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_banking_query(user_query: str) -> str:
    agent = create_banking_agent()
    task = create_banking_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_bankruptcy_query(user_query: str) -> str:
    agent = create_bankruptcy_agent()
    task = create_bankruptcy_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_company_law_query(user_query: str) -> str:
    agent = create_company_law_agent()
    task = create_company_law_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_copyright_query(user_query: str) -> str:
    agent = create_copyright_agent()
    task = create_copyright_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_corporate_practice_query(user_query: str) -> str:
    agent = create_corporate_practice_agent()
    task = create_corporate_practice_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_design_law_query(user_query: str) -> str:
    agent = create_design_law_agent()
    task = create_design_law_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_human_rights_query(user_query: str) -> str:
    agent = create_human_rights_agent()
    task = create_human_rights_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_information_technology_query(user_query: str) -> str:
    agent = create_information_technology_agent()
    task = create_information_technology_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_minimum_wages_query(user_query: str) -> str:
    agent = create_minimum_wages_agent()
    task = create_minimum_wages_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_patent_query(user_query: str) -> str:
    agent = create_patent_agent()
    task = create_patent_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_property_law_query(user_query: str) -> str:
    agent = create_property_law_agent()
    task = create_property_law_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_tax_law_query(user_query: str) -> str:
    agent = create_tax_law_agent()
    task = create_tax_law_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _run_trademark_law_query(user_query: str) -> str:
    agent = create_trademark_law_agent()
    task = create_trademark_law_query_task(agent, user_query)
    return str(Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff())

def _resolve_category(label_upper: str) -> str:
    """Return the canonical category name from the router label."""
    ordered = [
        "IPC", "CPC", "CRPC", "DIVORCE", "ENVIRON", "MARRIAGE", "MVA",
        "EVIDENCE", "ADMIN", "BANKING", "BANKRUPTCY", "COMPANY_LAW",
        "COPYRIGHT", "CORPORATE_PRACTICE", "DESIGN", "HUMAN_RIGHTS",
        "INFORMATION_TECHNOLOGY", "MINIMUM_WAGES", "PATENT", "PROPERTY",
        "TAX", "TRADEMARK", "CONSTITUTION",
    ]
    for cat in ordered:
        if cat in label_upper:
            return cat
    return "CONSTITUTION"


def run_query(user_query: str) -> tuple:
    """Classify and route a legal query, then return (answer, category)."""
    # Step 1 — Classify
    label = _classify_query(user_query)
    label_upper = label.upper()
    category = _resolve_category(label_upper)

    _AGENT_NAMES = {
        "IPC": "IPC Agent", "CPC": "CPC Agent", "CRPC": "CrPC Agent",
        "DIVORCE": "Divorce Act Agent", "ENVIRON": "Environment Act Agent",
        "MARRIAGE": "Hindu Marriage Act Agent", "MVA": "MVA Agent",
        "EVIDENCE": "Evidence Act Agent", "ADMIN": "Administrative Law Agent",
        "BANKING": "Banking Regulation Agent", "BANKRUPTCY": "Bankruptcy Law Agent",
        "COMPANY_LAW": "Company Law Agent", "COPYRIGHT": "Copyright Law Agent",
        "CORPORATE_PRACTICE": "Corporate Practice Agent", "DESIGN": "Design Law Agent",
        "HUMAN_RIGHTS": "Human Rights Agent", "INFORMATION_TECHNOLOGY": "IT Law Agent",
        "MINIMUM_WAGES": "Minimum Wages Act Agent", "PATENT": "Patent Law Agent",
        "PROPERTY": "Property Law Agent", "TAX": "Tax Law Agent",
        "TRADEMARK": "Trademark Law Agent", "CONSTITUTION": "Constitution Agent",
    }
    agent_name = _AGENT_NAMES.get(category, "Constitution Agent")
    print(f"  🔀 Routed to: {agent_name}")

    # Step 2 — Delegate to the right specialist
    _RUNNERS = {
        "IPC": _run_ipc_query, "CPC": _run_cpc_query, "CRPC": _run_crpc_query,
        "DIVORCE": _run_divorce_query, "ENVIRON": _run_environ_query,
        "MARRIAGE": _run_marriage_query, "MVA": _run_mva_query,
        "EVIDENCE": _run_evidence_query, "ADMIN": _run_administrative_query,
        "BANKING": _run_banking_query, "BANKRUPTCY": _run_bankruptcy_query,
        "COMPANY_LAW": _run_company_law_query, "COPYRIGHT": _run_copyright_query,
        "CORPORATE_PRACTICE": _run_corporate_practice_query,
        "DESIGN": _run_design_law_query, "HUMAN_RIGHTS": _run_human_rights_query,
        "INFORMATION_TECHNOLOGY": _run_information_technology_query,
        "MINIMUM_WAGES": _run_minimum_wages_query, "PATENT": _run_patent_query,
        "PROPERTY": _run_property_law_query, "TAX": _run_tax_law_query,
        "TRADEMARK": _run_trademark_law_query, "CONSTITUTION": _run_constitution_query,
    }
    runner = _RUNNERS.get(category, _run_constitution_query)
    answer = runner(user_query)
    return (answer, category)
