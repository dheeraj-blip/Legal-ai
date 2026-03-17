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

def run_query(user_query: str) -> str:
    """Classify and route a legal query, then return the answer."""
    # Step 1 — Classify
    label = _classify_query(user_query)
    label_upper = label.upper()
    agent_name = "Constitution Agent"
    
    if "IPC" in label_upper: agent_name = "IPC Agent"
    elif "CPC" in label_upper: agent_name = "CPC Agent"
    elif "CRPC" in label_upper: agent_name = "CrPC Agent"
    elif "DIVORCE" in label_upper: agent_name = "Divorce Act Agent"
    elif "ENVIRON" in label_upper: agent_name = "Environment Act Agent"
    elif "MARRIAGE" in label_upper: agent_name = "Hindu Marriage Act Agent"
    elif "MVA" in label_upper: agent_name = "MVA Agent"
    elif "EVIDENCE" in label_upper: agent_name = "Evidence Act Agent"
    elif "ADMIN" in label_upper: agent_name = "Administrative Law Agent"
    elif "BANKING" in label_upper: agent_name = "Banking Regulation Agent"
    elif "BANKRUPTCY" in label_upper: agent_name = "Bankruptcy Law Agent"
    elif "COMPANY_LAW" in label_upper: agent_name = "Company Law Agent"
    elif "COPYRIGHT" in label_upper: agent_name = "Copyright Law Agent"
    elif "CORPORATE_PRACTICE" in label_upper: agent_name = "Corporate Practice Agent"
    elif "DESIGN" in label_upper: agent_name = "Design Law Agent"
    elif "HUMAN_RIGHTS" in label_upper: agent_name = "Human Rights Agent"
    elif "INFORMATION_TECHNOLOGY" in label_upper: agent_name = "IT Law Agent"
    elif "MINIMUM_WAGES" in label_upper: agent_name = "Minimum Wages Act Agent"
    elif "PATENT" in label_upper: agent_name = "Patent Law Agent"
    elif "PROPERTY" in label_upper: agent_name = "Property Law Agent"
    elif "TAX" in label_upper: agent_name = "Tax Law Agent"
    elif "TRADEMARK" in label_upper: agent_name = "Trademark Law Agent"
    elif "CONSTITUTION" in label_upper: agent_name = "Constitution Agent"
    
    print(f"  🔀 Routed to: {agent_name}")

    # Step 2 — Delegate to the right specialist
    if "IPC" in label_upper: return _run_ipc_query(user_query)
    elif "CPC" in label_upper: return _run_cpc_query(user_query)
    elif "CRPC" in label_upper: return _run_crpc_query(user_query)
    elif "DIVORCE" in label_upper: return _run_divorce_query(user_query)
    elif "ENVIRON" in label_upper: return _run_environ_query(user_query)
    elif "MARRIAGE" in label_upper: return _run_marriage_query(user_query)
    elif "MVA" in label_upper: return _run_mva_query(user_query)
    elif "EVIDENCE" in label_upper: return _run_evidence_query(user_query)
    elif "ADMIN" in label_upper: return _run_administrative_query(user_query)
    elif "BANKING" in label_upper: return _run_banking_query(user_query)
    elif "BANKRUPTCY" in label_upper: return _run_bankruptcy_query(user_query)
    elif "COMPANY_LAW" in label_upper: return _run_company_law_query(user_query)
    elif "COPYRIGHT" in label_upper: return _run_copyright_query(user_query)
    elif "CORPORATE_PRACTICE" in label_upper: return _run_corporate_practice_query(user_query)
    elif "DESIGN" in label_upper: return _run_design_law_query(user_query)
    elif "HUMAN_RIGHTS" in label_upper: return _run_human_rights_query(user_query)
    elif "INFORMATION_TECHNOLOGY" in label_upper: return _run_information_technology_query(user_query)
    elif "MINIMUM_WAGES" in label_upper: return _run_minimum_wages_query(user_query)
    elif "PATENT" in label_upper: return _run_patent_query(user_query)
    elif "PROPERTY" in label_upper: return _run_property_law_query(user_query)
    elif "TAX" in label_upper: return _run_tax_law_query(user_query)
    elif "TRADEMARK" in label_upper: return _run_trademark_law_query(user_query)
    else: return _run_constitution_query(user_query)
