"""CrewAI agent definitions for the Indian Law Query Assistant."""

import os
from crewai import Agent
from crewai import LLM
from tools import (
    ConstitutionSearchTool, IPCSearchTool, CPCSearchTool, CrPCSearchTool,
    DivorceSearchTool, EnvironSearchTool, MarriageSearchTool, MVASearchTool,
    EvidenceSearchTool, AdministrativeSearchTool, BankingSearchTool,
    BankruptcySearchTool, CompanyLawSearchTool, CopyrightSearchTool,
    CorporatePracticeSearchTool, DesignLawSearchTool, HumanRightsSearchTool,
    InformationTechnologySearchTool, MinimumWagesSearchTool, PatentSearchTool,
    PropertyLawSearchTool, TaxLawSearchTool, TrademarkLawSearchTool,
    SupremeCourtCaseSearchTool
)



_BASE_URL = os.environ.get("OPENAI_API_BASE", "https://api.groq.com/openai/v1")
_MODEL    = os.environ.get("OPENAI_MODEL_NAME", "llama-3.3-70b-versatile")
_KEY_ROUTER = os.environ.get("GROQ_KEY_ROUTER")
_KEY_LAWS   = os.environ.get("GROQ_KEY_LAWS")
_KEY_SC     = os.environ.get("GROQ_KEY_SC")
_KEY_RETRY  = os.environ.get("GROQ_KEY_RETRY")

if not all([_KEY_ROUTER, _KEY_LAWS, _KEY_SC, _KEY_RETRY]):
    raise ValueError("Missing one or more GROQ API keys in environment variables")



def _llm(api_key: str):
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0
    )


# One LLM instance per key — reused across all agents
_llm_router = _llm(_KEY_ROUTER)
_llm_laws   = _llm(_KEY_LAWS)
_llm_sc     = _llm(_KEY_SC)
_llm_retry  = _llm(_KEY_RETRY)


_sc_tool = SupremeCourtCaseSearchTool()

_CASE_BACKSTORY = (
    "You have access to legal provisions and Supreme Court case data. "
    "Use them internally to answer questions accurately. "
    "Do NOT mention tools, searches, or your reasoning process. "
    "Always give the final legal answer directly in a clean, structured format."
)



def create_router_agent() -> Agent:
    categories = (
        "CONSTITUTION, IPC, CPC, CRPC, DIVORCE, ENVIRON, MARRIAGE, MVA, EVIDENCE, "
        "ADMIN, BANKING, BANKRUPTCY, COMPANY_LAW, COPYRIGHT, CORPORATE_PRACTICE, "
        "DESIGN, HUMAN_RIGHTS, INFORMATION_TECHNOLOGY, MINIMUM_WAGES, PATENT, "
        "PROPERTY, TAX, TRADEMARK"
    )
    return Agent(
        role="Legal Query Router",
        goal=(
            f"Classify a user's legal question into one of these categories: {categories}. "
            "Output ONLY the category name as a single word."
        ),
        backstory=(
            "You are an expert legal domain classifier. "
            "Categories mapping:\n"
            "- CONSTITUTION: Fundamental rights, government, elections, constitution articles.\n"
            "- IPC: Crimes, punishments, offences, theft, murder, fraud.\n"
            "- CPC: Civil procedure, suits, decrees, civil courts, summons.\n"
            "- CRPC: Criminal procedure, arrests, bail, FIR procedure, police powers.\n"
            "- DIVORCE: Divorce rules, Christian divorce, annulment, dissolution of marriage.\n"
            "- ENVIRON: Environment protection, pollution, hazardous substances, EPA.\n"
            "- MARRIAGE: Hindu marriage, restitution of conjugal rights, void marriages.\n"
            "- MVA: Motor vehicles, driving license, traffic rules, vehicle registration, accidents.\n"
            "- EVIDENCE: Evidence act, admissibility of evidence, burden of proof.\n"
            "- ADMIN: Administrative law, government procedures, governance.\n"
            "- BANKING: Banking regulations, deposits, loans, banking operations.\n"
            "- BANKRUPTCY: Insolvency, bankruptcy proceedings, creditor rights.\n"
            "- COMPANY_LAW: Company incorporation, corporate governance, shareholders.\n"
            "- COPYRIGHT: Copyright protection, intellectual property, literary works.\n"
            "- CORPORATE_PRACTICE: Corporate law practice, legal compliance, corporate governance.\n"
            "- DESIGN: Design protection, registered designs, industrial designs.\n"
            "- HUMAN_RIGHTS: Civil rights, constitutional rights, human rights protection.\n"
            "- INFORMATION_TECHNOLOGY: IT law, cyber security, data protection, digital rights.\n"
            "- MINIMUM_WAGES: Minimum wage laws, labor standards, wage protection.\n"
            "- PATENT: Patent protection, innovation, patent registration.\n"
            "- PROPERTY: Property rights, land law, real estate, conveyance.\n"
            "- TAX: Tax law, income tax, GST, tax compliance, tax deductions.\n"
            "- TRADEMARK: Trademark protection, brand protection, trade marks registration.\n"
            "You must respond with ONLY exactly one of the category names."
        ),
        tools=[],
        verbose=False,
        max_iter=1,
        llm=_llm_router,
    )



def create_constitution_agent() -> Agent:
    return Agent(
        role="Indian Constitution Expert",
        goal=(
            "Answer user questions about the Indian Constitution accurately by "
            "searching through the constitutional articles, finding related Supreme Court "
            "cases, and providing clear, well-referenced answers."
        ),
        backstory=(
            "You are a constitutional law expert with deep knowledge of the Indian Constitution. "
            "You have access to the full text of the Constitution and can search through its "
            "articles to find relevant provisions. You always cite specific article numbers in "
            "your answers and explain constitutional concepts in simple, accessible language."
            + _CASE_BACKSTORY
        ),
        tools=[ConstitutionSearchTool(), _sc_tool],
        verbose=False,
        max_iter=1,
        llm=_llm_laws,
        function_calling_llm=_llm_retry,
    )


def create_ipc_agent() -> Agent:
    return Agent(
        role="Indian Penal Code Expert",
        goal=(
            "Answer user questions about the Indian Penal Code accurately by "
            "searching through IPC sections, finding related Supreme Court cases, "
            "and providing clear, well-referenced answers with section numbers and chapter context."
        ),
        backstory=(
            "You are a criminal law expert with deep knowledge of the Indian Penal Code (IPC). "
            "You have access to the full text of the IPC and can search through its sections to "
            "find relevant provisions. You always cite specific Section numbers and chapter names "
            "in your answers and explain legal concepts in simple, accessible language."
            + _CASE_BACKSTORY
        ),
        tools=[IPCSearchTool(), _sc_tool],
        verbose=False,
        max_iter=1,
        llm=_llm_laws,
        function_calling_llm=_llm_retry,
    )


def create_cpc_agent() -> Agent:
    return Agent(
        role="Code of Civil Procedure Expert",
        goal="Answer user questions about the CPC accurately by searching provisions, finding related Supreme Court cases, and citing sections.",
        backstory="You are a legal expert in Indian civil procedure. You search CPC effectively to provide clear answers." + _CASE_BACKSTORY,
        tools=[CPCSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_crpc_agent() -> Agent:
    return Agent(
        role="Code of Criminal Procedure Expert",
        goal="Answer user questions about the CrPC accurately by searching provisions, finding related Supreme Court cases, and citing sections.",
        backstory="You are a legal expert in Indian criminal procedures. You search CrPC effectively to provide clear answers." + _CASE_BACKSTORY,
        tools=[CrPCSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_divorce_agent() -> Agent:
    return Agent(
        role="Divorce Act Expert",
        goal="Answer user questions about the Divorce Act accurately by searching, finding related Supreme Court cases, and citing sections.",
        backstory="You are an expert in Indian divorce law. You search the Divorce Act to provide clear answers. You must strictly use ONLY the provided tools and never attempt to use 'brave_search' or any other external search." + _CASE_BACKSTORY,
        tools=[DivorceSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_environ_agent() -> Agent:
    return Agent(
        role="Environment Protection Act Expert",
        goal="Answer user questions about the Environment Protection Act by searching provisions and finding related Supreme Court cases.",
        backstory="You are an environmental law expert in India. You search the EPA to provide clear answers." + _CASE_BACKSTORY,
        tools=[EnvironSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_marriage_agent() -> Agent:
    return Agent(
        role="Hindu Marriage Act Expert",
        goal="Answer user questions about the Hindu Marriage Act by searching provisions and finding related Supreme Court cases.",
        backstory="You are an expert in Hindu family law. You search the Hindu Marriage Act to provide clear answers." + _CASE_BACKSTORY,
        tools=[MarriageSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_mva_agent() -> Agent:
    return Agent(
        role="Motor Vehicles Act Expert",
        goal="Answer user questions about the Motor Vehicles Act by searching provisions and finding related Supreme Court cases.",
        backstory="You are a motor vehicles and traffic law expert. You search the MVA to provide clear answers." + _CASE_BACKSTORY,
        tools=[MVASearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_evidence_agent() -> Agent:
    return Agent(
        role="Indian Evidence Act Expert",
        goal="Answer user questions about the Evidence Act accurately by searching, finding related Supreme Court cases, and citing sections.",
        backstory="You are an expert in Indian evidence law. You search the Evidence Act to provide clear answers with section references." + _CASE_BACKSTORY,
        tools=[EvidenceSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_administrative_agent() -> Agent:
    return Agent(
        role="Administrative Law Expert",
        goal="Answer user questions about Administrative Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian administrative law and government procedures. You search administrative law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[AdministrativeSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_banking_agent() -> Agent:
    return Agent(
        role="Banking Regulation Expert",
        goal="Answer user questions about Banking Regulation accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian banking law and regulations. You search banking provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[BankingSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_bankruptcy_agent() -> Agent:
    return Agent(
        role="Bankruptcy Law Expert",
        goal="Answer user questions about Bankruptcy Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian bankruptcy and insolvency law. You search bankruptcy law to provide clear answers." + _CASE_BACKSTORY,
        tools=[BankruptcySearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_company_law_agent() -> Agent:
    return Agent(
        role="Company Law Expert",
        goal="Answer user questions about Company Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian company law and corporate governance. You search company law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[CompanyLawSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_copyright_agent() -> Agent:
    return Agent(
        role="Copyright Law Expert",
        goal="Answer user questions about Copyright Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian copyright law and intellectual property. You search copyright provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[CopyrightSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_corporate_practice_agent() -> Agent:
    return Agent(
        role="Corporate Practice Act Expert",
        goal="Answer user questions about Corporate Practice Act accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in corporate practice and legal compliance. You search corporate practice provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[CorporatePracticeSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_design_law_agent() -> Agent:
    return Agent(
        role="Design Law Expert",
        goal="Answer user questions about Design Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian design law and intellectual property. You search design law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[DesignLawSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_human_rights_agent() -> Agent:
    return Agent(
        role="Human Rights Law Expert",
        goal="Answer user questions about Human Rights Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in human rights law and constitutional protections. You search human rights provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[HumanRightsSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_information_technology_agent() -> Agent:
    return Agent(
        role="Information Technology Law Expert",
        goal="Answer user questions about IT Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian IT law, cyber security, and data protection. You search IT law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[InformationTechnologySearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_minimum_wages_agent() -> Agent:
    return Agent(
        role="Minimum Wages Act Expert",
        goal="Answer user questions about Minimum Wages Act accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in minimum wage law and labor standards. You search minimum wages provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[MinimumWagesSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_patent_agent() -> Agent:
    return Agent(
        role="Patent Law Expert",
        goal="Answer user questions about Patent Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian patent law and intellectual property. You search patent provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[PatentSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_property_law_agent() -> Agent:
    return Agent(
        role="Property Law Expert",
        goal="Answer user questions about Property Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian property law and land rights. You search property law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[PropertyLawSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_tax_law_agent() -> Agent:
    return Agent(
        role="Tax Law Expert",
        goal="Answer user questions about Tax Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian tax law, income tax, and GST. You search tax law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[TaxLawSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )


def create_trademark_law_agent() -> Agent:
    return Agent(
        role="Trademark Law Expert",
        goal="Answer user questions about Trademark Law accurately by searching, finding related Supreme Court cases, and citing provisions.",
        backstory="You are an expert in Indian trademark law and intellectual property. You search trademark law provisions to provide clear answers." + _CASE_BACKSTORY,
        tools=[TrademarkLawSearchTool(), _sc_tool],
        verbose=False, max_iter=1,
        llm=_llm_laws, function_calling_llm=_llm_retry,
    )