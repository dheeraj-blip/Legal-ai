"""CrewAI task definitions for the Indian Law Query Assistant."""

from crewai import Task, Agent


# Shared instruction block for Supreme Court case search + Google fallback
_CASE_INSTRUCTIONS = (
    "5. Use the SupremeCourtCaseSearchTool to search for related Supreme Court cases. "
    "If any relevant case is found, briefly cite the case name, year, and explain how it relates to the question.\n"
    "6. If the results from both the domain-specific search and the Supreme Court cases "
    "feel insufficient or unsatisfying, perform a Google search on your own "
    "for additional insights and cite the sources you find.\n"
)



def create_routing_task(agent: Agent, user_query: str) -> Task:
    """Create a task to classify the user's query into the correct legal domain."""
    return Task(
        description=(
            f"Classify the following user question into one of these categories:\n\n"
            f"'{user_query}'\n\n"
            f"Categories:\n"
            f"- CONSTITUTION: Indian Constitution, rights, government, parliament.\n"
            f"- IPC: Indian Penal Code, crimes, offences, punishments, theft, murder.\n"
            f"- CPC: Civil Procedure Code, civil suits, decrees, civil courts.\n"
            f"- CRPC: Criminal Procedure Code, arrests, FIR procedure, police powers.\n"
            f"- DIVORCE: Divorce Act, Christian marriages, dissolution, alimony.\n"
            f"- ENVIRON: Environment Protection Act, pollution, hazardous substances.\n"
            f"- MARRIAGE: Hindu Marriage Act, marriage rituals, restitution, annulment.\n"
            f"- MVA: Motor Vehicles Act, traffic rules, licensing, vehicle registration.\n"
            f"- EVIDENCE: Evidence Act, admissibility, burden of proof, witnesses.\n"
            f"- ADMIN: Administrative law, government procedures, governance.\n"
            f"- BANKING: Banking regulations, deposits, loans, banking operations.\n"
            f"- BANKRUPTCY: Bankruptcy proceedings, insolvency, creditor rights.\n"
            f"- COMPANY_LAW: Company law, incorporation, corporate governance, shares.\n"
            f"- COPYRIGHT: Copyright law, literary works, intellectual property.\n"
            f"- CORPORATE_PRACTICE: Corporate law practice, compliance, governance.\n"
            f"- DESIGN: Design law, registered designs, industrial designs.\n"
            f"- HUMAN_RIGHTS: Human rights, civil rights, constitutional protections.\n"
            f"- INFORMATION_TECHNOLOGY: IT law, cyber security, data protection.\n"
            f"- MINIMUM_WAGES: Minimum wage law, labor standards, wage protection.\n"
            f"- PATENT: Patent law, innovation, patent registration.\n"
            f"- PROPERTY: Property law, land law, real estate, conveyance.\n"
            f"- TAX: Tax law, income tax, GST, tax compliance.\n"
            f"- TRADEMARK: Trademark law, brand protection, trademark registration.\n\n"
            f"Respond with ONLY one category name (single word, e.g., CONSTITUTION or PATENT)"
        ),
        expected_output="A single word representing the category.",
        agent=agent,
    )


def create_constitution_query_task(agent: Agent, user_query: str) -> Task:
    """Create a task to answer a user's constitutional query."""
    return Task(
        description=(
            f"Answer the following user question about the Indian Constitution:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Use the ConstitutionSearchTool to search for relevant articles.\n"
            f"2. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"3. Analyze the retrieved articles in the context of the question.\n"
            f"4. Provide a clear, structured, and reader-friendly answer (not boring) that:\n"
            f"   - Directly addresses the user's question\n"
            f"   - Cites specific Article numbers and their titles\n"
            f"   - Quotes key provisions where relevant\n"
            f"   - Explains the constitutional provisions in simple, engaging language\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output=(
            "A comprehensive, well-structured, and reader-friendly answer to the user's question about "
            "the Indian Constitution, with specific article references, related Supreme Court case insights, "
            "clear explanations, and engaging language."
        ),
        agent=agent,
    )


def create_ipc_query_task(agent: Agent, user_query: str) -> Task:
    """Create a task to answer a user's IPC query."""
    return Task(
        description=(
            f"Answer the following user question about the Indian Penal Code:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Use the IPCSearchTool to search for relevant sections.\n"
            f"2. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"3. Analyze the retrieved sections in the context of the question.\n"
            f"4. Provide a clear, structured, and reader-friendly answer (not boring) that:\n"
            f"   - Directly addresses the user's question\n"
            f"   - Cites specific Section numbers and chapter names\n"
            f"   - Quotes key provisions where relevant\n"
            f"   - Explains the legal provisions in simple, engaging language\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output=(
            "A comprehensive, well-structured, and reader-friendly answer to the user's question about "
            "the Indian Penal Code, with specific section references, related Supreme Court case insights, "
            "clear explanations, and engaging language."
        ),
        agent=agent,
    )


def create_cpc_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Code of Civil Procedure (CPC):\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the CPC with specific section references and related Supreme Court case insights.",
        agent=agent,
    )

def create_crpc_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Code of Criminal Procedure (CrPC):\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the CrPC with specific section references and related Supreme Court case insights.",
        agent=agent,
    )

def create_divorce_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Divorce Act:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the Divorce Act with specific section references and related Supreme Court case insights.",
        agent=agent,
    )

def create_environ_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Environment Protection Act:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the Environment Protection Act with specific references and related Supreme Court case insights.",
        agent=agent,
    )

def create_marriage_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Hindu Marriage Act:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the Hindu Marriage Act with specific references and related Supreme Court case insights.",
        agent=agent,
    )

def create_mva_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Motor Vehicles Act:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the Motor Vehicles Act with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_evidence_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about the Indian Evidence Act:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific section numbers, and explains the legal provisions in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about the Evidence Act with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_administrative_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Administrative Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the legal concepts in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Administrative Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_banking_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Banking Regulation:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the banking regulations in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Banking Regulation with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_bankruptcy_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Bankruptcy Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the bankruptcy procedures in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Bankruptcy Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_company_law_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Company Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the company law concepts in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Company Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_copyright_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Copyright Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the copyright protections in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Copyright Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_corporate_practice_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Corporate Practice:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the corporate practice requirements in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Corporate Practice with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_design_law_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Design Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the design protections in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Design Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_human_rights_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Human Rights Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the human rights protections in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Human Rights with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_information_technology_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Information Technology Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains IT law and cybersecurity concepts in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about IT Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_minimum_wages_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Minimum Wages Act:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the minimum wage requirements in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Minimum Wages Act with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_patent_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Patent Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the patent protections in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Patent Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_property_law_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Property Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the property law concepts in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Property Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_tax_law_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Tax Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the tax law concepts in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Tax Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )


def create_trademark_law_query_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"Answer the following user question about Trademark Law:\n\n"
            f"'{user_query}'\n\n"
            f"Instructions:\n"
            f"1. Search with multiple relevant keywords to ensure comprehensive coverage.\n"
            f"2. Analyze the retrieved sections in the context of the question.\n"
            f"3. Provide a clear, structured, and reader-friendly answer that directly addresses the question, \n"
            f"cites specific provisions, and explains the trademark protections in an engaging, non-boring way.\n"
            f"4. You may use google search only if you feel data is insufficient.\n"
            + _CASE_INSTRUCTIONS
        ),
        expected_output="A comprehensive, well-structured answer about Trademark Law with specific references and related Supreme Court case insights.",
        agent=agent,
    )
