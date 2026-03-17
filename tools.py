"""Custom CrewAI tool for searching the Indian Constitution."""

import json
import os
from crewai.tools import BaseTool
from pydantic import Field
from typing import ClassVar, List, Dict, Any


class ConstitutionSearchTool(BaseTool):
    """Tool to search the Indian Constitution articles from const.json."""

    name: str = "ConstitutionSearchTool"
    description: str = (
        "Searches the Indian Constitution (const.json) for articles matching a query. "
        "Input should be a search keyword or phrase. Returns matching articles with "
        "their article number, title, and full description. Use this tool to find "
        "constitutional provisions relevant to a user's question."
    )
    data_path: str = Field(default="const.json", description="Path to const.json")

    # Class-level cache so the JSON is loaded only once across all instances
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        """Load and cache the JSON data. Only reads from disk on first call."""
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)

        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)

        return self._cache[json_path]

    def _run(self, query: str) -> str:
        """Search const.json for articles matching the query."""
        try:
            articles = self._load_data()
        except FileNotFoundError:
            return f"Error: Could not find const.json"
        except json.JSONDecodeError:
            return f"Error: Could not parse const.json"

        keywords = query.lower().split()
        results = []

        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            article_num = str(article.get("article", ""))
            searchable = f"{title} {description} {article_num}"

            # Score: how many keywords match
            score = sum(1 for kw in keywords if kw in searchable)

            if score > 0:
                results.append((score, article))

        # Sort by relevance (highest score first), take top 5
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]

        if not top_results:
            return f"No articles found matching: '{query}'. Try different keywords."

        output = f"Found {len(top_results)} relevant articles:\n\n"
        for _score, art in top_results:
            desc = art.get("description", "")
            # Truncate long descriptions to keep LLM context small
            if len(desc) > 500:
                desc = desc[:500] + "..."
            output += f"--- Article {art['article']}: {art['title']} ---\n"
            output += f"{desc}\n\n"

        return output


class IPCSearchTool(BaseTool):
    """Tool to search the Indian Penal Code sections from ipc.json."""

    name: str = "IPCSearchTool"
    description: str = (
        "Searches the Indian Penal Code (ipc.json) for sections matching a query. "
        "Input should be a search keyword or phrase. Returns matching sections with "
        "their section number, title, chapter info, and full description. Use this "
        "tool to find IPC provisions relevant to a user's question."
    )
    data_path: str = Field(default="ipc.json", description="Path to ipc.json")

    # Class-level cache so the JSON is loaded only once across all instances
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        """Load and cache the JSON data. Only reads from disk on first call."""
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)

        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)

        return self._cache[json_path]

    def _run(self, query: str) -> str:
        """Search ipc.json for sections matching the query."""
        try:
            sections = self._load_data()
        except FileNotFoundError:
            return "Error: Could not find ipc.json"
        except json.JSONDecodeError:
            return "Error: Could not parse ipc.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            section_title = section.get("section_title", "").lower()
            section_desc = section.get("section_desc", "").lower()
            chapter_title = section.get("chapter_title", "").lower()
            section_num = str(section.get("Section", ""))
            searchable = f"{section_title} {section_desc} {chapter_title} {section_num}"

            # Score: how many keywords match
            score = sum(1 for kw in keywords if kw in searchable)

            if score > 0:
                results.append((score, section))

        # Sort by relevance (highest score first), take top 5
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]

        if not top_results:
            return f"No sections found matching: '{query}'. Try different keywords."

        output = f"Found {len(top_results)} relevant IPC sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("section_desc", "")
            # Truncate long descriptions to keep LLM context small
            if len(desc) > 500:
                desc = desc[:500] + "..."
            chapter = sec.get("chapter", "")
            ch_title = sec.get("chapter_title", "")
            output += f"--- Section {sec['Section']} (Ch.{chapter}: {ch_title}): {sec['section_title']} ---\n"
            output += f"{desc}\n\n"

        return output


class CPCSearchTool(BaseTool):
    """Tool to search the Code of Civil Procedure from cpc.json."""

    name: str = "CPCSearchTool"
    description: str = (
        "Searches the Code of Civil Procedure (cpc.json) for sections matching a query. "
        "Input should be a search keyword or phrase. Returns matching sections. "
        "Use this tool to find CPC provisions relevant to a user's question."
    )
    data_path: str = Field(default="cpc.json", description="Path to cpc.json")

    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read cpc.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]

        if not top_results:
            return f"No sections found in CPC matching: '{query}'."

        output = f"Found {len(top_results)} relevant CPC sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- Section {sec.get('section', '')}: {sec.get('title', '')} ---\n{desc}\n\n"
        return output


class CrPCSearchTool(BaseTool):
    """Tool to search the Code of Criminal Procedure from crpc.json."""

    name: str = "CrPCSearchTool"
    description: str = "Searches the Code of Criminal Procedure (crpc.json) for sections matching a query."
    data_path: str = Field(default="crpc.json", description="Path to crpc.json")

    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read crpc.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("section_title", "").lower()
            desc = section.get("section_desc", "").lower()
            sec_num = str(section.get("section", ""))
            ch_num = str(section.get("chapter", ""))
            searchable = f"{title} {desc} {sec_num} {ch_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No sections found in CrPC matching: '{query}'."

        output = f"Found {len(top_results)} relevant CrPC sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("section_desc", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- Section {sec.get('section', '')} (Ch.{sec.get('chapter', '')}): {sec.get('section_title', '')} ---\n{desc}\n\n"
        return output


class DivorceSearchTool(BaseTool):
    """Tool to search the Divorce Act from div.json."""

    name: str = "DivorceSearchTool"
    description: str = "Searches the Divorce Act (div.json) for sections matching a query."
    data_path: str = Field(default="div.json", description="Path to div.json")

    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read div.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No sections found in Divorce Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Divorce Act sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- Section {sec.get('section', '')}: {sec.get('title', '')} ---\n{desc}\n\n"
        return output


class EnvironSearchTool(BaseTool):
    """Tool to search the Environment Protection Act from environ.json."""

    name: str = "EnvironSearchTool"
    description: str = "Searches the Environment Protection Act (environ.json) for sections matching a query."
    data_path: str = Field(default="environ.json", description="Path to environ.json")

    _cache: ClassVar[Dict[str, Any]] = {}

    def _load_data(self) -> dict:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            data = self._load_data()
        except Exception:
            return "Error: Could not read environ.json"

        keywords = query.lower().split()
        results = []

        for chapter in data.get("chapters", []):
            ch_title = chapter.get("title", "").lower()
            for sec in chapter.get("sections", []):
                heading = sec.get("heading", "").lower()
                content_list = sec.get("content", [])
                content_str = " ".join(content_list).lower()
                searchable = f"{ch_title} {heading} {content_str}"

                score = sum(1 for kw in keywords if kw in searchable)
                if score > 0:
                    results.append((score, chapter.get("chapter", ""), sec.get("heading", ""), content_list))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Environment Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Environment Act provisions:\n\n"
        for _score, ch, heading, content in top_results:
            desc = " ".join(content)
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {ch} | {heading} ---\n{desc}\n\n"
        return output


class MarriageSearchTool(BaseTool):
    """Tool to search the Hindu Marriage Act from mar.json."""

    name: str = "MarriageSearchTool"
    description: str = "Searches the Hindu Marriage Act (mar.json) for sections matching a query."
    data_path: str = Field(default="mar.json", description="Path to mar.json")

    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read mar.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("section_title", "").lower()
            desc = section.get("section_desc", "").lower()
            sec_num = str(section.get("section", ""))
            ch_num = str(section.get("chapter", ""))
            searchable = f"{title} {desc} {sec_num} {ch_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No sections found in Hindu Marriage Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Marriage Act sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("section_desc", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- Section {sec.get('section', '')} (Ch.{sec.get('chapter', '')}): {sec.get('section_title', '')} ---\n{desc}\n\n"
        return output


class MVASearchTool(BaseTool):
    """Tool to search the Motor Vehicles Act from mva.json."""

    name: str = "MVASearchTool"
    description: str = "Searches the Motor Vehicles Act (mva.json) for sections matching a query."
    data_path: str = Field(default="mva.json", description="Path to mva.json")

    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read mva.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No sections found in Motor Vehicles Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Motor Vehicles Act sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- Section {sec.get('section', '')}: {sec.get('title', '')} ---\n{desc}\n\n"
        return output


class EvidenceSearchTool(BaseTool):
    """Tool to search the Indian Evidence Act from evid.json."""

    name: str = "EvidenceSearchTool"
    description: str = "Searches the Indian Evidence Act (evid.json) for sections matching a query."
    data_path: str = Field(default="evid.json", description="Path to evid.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read evid.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No sections found in Evidence Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Evidence Act sections:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- Section {sec.get('section', '')}: {sec.get('title', '')} ---\n{desc}\n\n"
        return output


class AdministrativeSearchTool(BaseTool):
    """Tool to search Administrative Law from adm.json."""

    name: str = "AdministrativeSearchTool"
    description: str = "Searches Administrative Law (adm.json) for relevant provisions."
    data_path: str = Field(default="adm.json", description="Path to adm.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read adm.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Administrative Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Administrative Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class BankingSearchTool(BaseTool):
    """Tool to search Banking Regulation from banking.json."""

    name: str = "BankingSearchTool"
    description: str = "Searches Banking Regulation (banking.json) for relevant provisions."
    data_path: str = Field(default="banking.json", description="Path to banking.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read banking.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Banking Regulation matching: '{query}'."

        output = f"Found {len(top_results)} relevant Banking provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class BankruptcySearchTool(BaseTool):
    """Tool to search Bankruptcy Law from bankruptcy.json."""

    name: str = "BankruptcySearchTool"
    description: str = "Searches Bankruptcy Law (bankruptcy.json) for relevant provisions."
    data_path: str = Field(default="bankruptcy.json", description="Path to bankruptcy.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read bankruptcy.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Bankruptcy Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Bankruptcy Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class CompanyLawSearchTool(BaseTool):
    """Tool to search Company Law from cl.json."""

    name: str = "CompanyLawSearchTool"
    description: str = "Searches Company Law (cl.json) for relevant provisions."
    data_path: str = Field(default="cl.json", description="Path to cl.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read cl.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Company Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Company Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class CopyrightSearchTool(BaseTool):
    """Tool to search Copyright Law from Copyright.json."""

    name: str = "CopyrightSearchTool"
    description: str = "Searches Copyright Law (Copyright.json) for relevant provisions."
    data_path: str = Field(default="Copyright.json", description="Path to Copyright.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read Copyright.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Copyright Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Copyright provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class CorporatePracticeSearchTool(BaseTool):
    """Tool to search Corporate Practice Act from cpa.json."""

    name: str = "CorporatePracticeSearchTool"
    description: str = "Searches Corporate Practice Act (cpa.json) for relevant provisions."
    data_path: str = Field(default="cpa.json", description="Path to cpa.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read cpa.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Corporate Practice Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Corporate Practice provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class DesignLawSearchTool(BaseTool):
    """Tool to search Design Law from design.json."""

    name: str = "DesignLawSearchTool"
    description: str = "Searches Design Law (design.json) for relevant provisions."
    data_path: str = Field(default="design.json", description="Path to design.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read design.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Design Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Design Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class HumanRightsSearchTool(BaseTool):
    """Tool to search Human Rights Law from human_rights.json."""

    name: str = "HumanRightsSearchTool"
    description: str = "Searches Human Rights Law (human_rights.json) for relevant provisions."
    data_path: str = Field(default="human_rights.json", description="Path to human_rights.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read human_rights.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Human Rights Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Human Rights provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class InformationTechnologySearchTool(BaseTool):
    """Tool to search Information Technology Law from it.json."""

    name: str = "InformationTechnologySearchTool"
    description: str = "Searches Information Technology Law (it.json) for relevant provisions."
    data_path: str = Field(default="it.json", description="Path to it.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read it.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in IT Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant IT Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class MinimumWagesSearchTool(BaseTool):
    """Tool to search Minimum Wages Act from MinimumWagesact.json."""

    name: str = "MinimumWagesSearchTool"
    description: str = "Searches Minimum Wages Act (MinimumWagesact.json) for relevant provisions."
    data_path: str = Field(default="MinimumWagesact.json", description="Path to MinimumWagesact.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read MinimumWagesact.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Minimum Wages Act matching: '{query}'."

        output = f"Found {len(top_results)} relevant Minimum Wages Act provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class PatentSearchTool(BaseTool):
    """Tool to search Patent Law from patent.json."""

    name: str = "PatentSearchTool"
    description: str = "Searches Patent Law (patent.json) for relevant provisions."
    data_path: str = Field(default="patent.json", description="Path to patent.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read patent.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Patent Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Patent Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class PropertyLawSearchTool(BaseTool):
    """Tool to search Property Law from prop.json."""

    name: str = "PropertyLawSearchTool"
    description: str = "Searches Property Law (prop.json) for relevant provisions."
    data_path: str = Field(default="prop.json", description="Path to prop.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read prop.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Property Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Property Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class TaxLawSearchTool(BaseTool):
    """Tool to search Tax Law from tax.json."""

    name: str = "TaxLawSearchTool"
    description: str = "Searches Tax Law (tax.json) for relevant provisions."
    data_path: str = Field(default="tax.json", description="Path to tax.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read tax.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Tax Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Tax Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output


class TrademarkLawSearchTool(BaseTool):
    """Tool to search Trademark Law from trademarks.json."""

    name: str = "TrademarkLawSearchTool"
    description: str = "Searches Trademark Law (trademarks.json) for relevant provisions."
    data_path: str = Field(default="trademarks.json", description="Path to trademarks.json")
    _cache: ClassVar[Dict[str, List[Dict[str, Any]]]] = {}

    def _load_data(self) -> list:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.data_path)
        if json_path not in self._cache:
            with open(json_path, "r", encoding="utf-8") as f:
                self._cache[json_path] = json.load(f)
        return self._cache[json_path]

    def _run(self, query: str) -> str:
        try:
            sections = self._load_data()
        except Exception:
            return "Error: Could not read trademarks.json"

        keywords = query.lower().split()
        results = []

        for section in sections:
            title = section.get("title", "").lower()
            desc = section.get("description", "").lower()
            sec_num = str(section.get("section", ""))
            searchable = f"{title} {desc} {sec_num}"

            score = sum(1 for kw in keywords if kw in searchable)
            if score > 0:
                results.append((score, section))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:5]
        if not top_results: return f"No provisions found in Trademark Law matching: '{query}'."

        output = f"Found {len(top_results)} relevant Trademark Law provisions:\n\n"
        for _score, sec in top_results:
            desc = sec.get("description", "")
            if len(desc) > 500: desc = desc[:500] + "..."
            output += f"--- {sec.get('title', '')}: {sec.get('section', '')} ---\n{desc}\n\n"
        return output
