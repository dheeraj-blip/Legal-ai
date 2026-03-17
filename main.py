"""
Indian Law Query Assistant - powered by CrewAI

Handles questions about both the Indian Constitution and the Indian Penal Code.
A Router agent automatically determines which specialist to consult.

Usage:
    python main.py                          # Interactive mode
    python main.py "your question here"     # Single query mode
"""

import sys
import os
import logging
logging.getLogger("crewai").setLevel(logging.ERROR)
os.environ["CREWAI_INTERACTIVE_MODE"] = "false"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from crew import run_query


def main():
    # Single query from command line
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\n{'='*60}")
        print(f"  Question: {query}")
        print(f"{'='*60}\n")
        result = run_query(query)
        print(f"\n{'='*60}")
        print("  ANSWER")
        print(f"{'='*60}")
        print(result)
        return

    # Interactive mode
    print("\n" + "=" * 80)
    print("  🏛️  Indian Law Query Assistant")
    print("=" * 80)
    print("\n  Available Legal Domains:")
    print("\n  Ask about any of these legal areas. Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            query = input("⚖️  Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print(f"\n🔍 Analyzing your question...\n")
        result = run_query(query)
        print(f"\n{'='*60}")
        print("  ANSWER")
        print(f"{'='*60}")
        print(result)
        print()


if __name__ == "__main__":
    main()
