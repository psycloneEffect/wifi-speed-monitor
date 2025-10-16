# AGENTS.md

## Overview

This document provides guidance for building AI agents in Python using the Microsoft Agent Framework (MAF), announced in October 2025. MAF is an open-source SDK and runtime that simplifies the creation, orchestration, and deployment of AI agents and multi-agent systems. It extends concepts from Semantic Kernel (enterprise-grade orchestration) and AutoGen (multi-agent collaboration), offering support for Python via the `agent-framework` package.

Designed for developers working in Visual Studio Code (VS Code), this guide emphasizes Pythonic implementations, best practices for code structure, and integration with VS Code tools like extensions for Python (e.g., IntelliSense, debugging), Git integration for version control, and Markdown preview for documentation. Use VS Code's built-in terminal for pip installations and running scripts, and leverage extensions like Python Debugger for stepping through agent workflows.

Key goals:

- Propose architectures suited for AI agent projects.
- Outline code review processes.
- Highlight anti-patterns to avoid.
- Recommend frameworks and approaches based on project scale.

For installation: In VS Code's terminal, run `pip install agent-framework`. Ensure you have compatible LLM providers (e.g., Azure OpenAI or OpenAI) configured via environment variables.

## Architecture Proposals

MAF promotes a layered architecture that aligns with established patterns like Layered Architecture and Onion Architecture, adapted for AI agents. This ensures separation of concerns, modularity, and scalability.

### Layered Architecture (Recommended for Most Projects)

- **Presentation/Interface Layer**: Handles user inputs/outputs, e.g., CLI, web APIs, or conversational interfaces. In Python, use libraries like `click` for CLI or `fastapi` for APIs to interact with agents.
- **Application Layer**: Orchestrates agents and workflows. Define AI agents using MAF's `AIAgent` class, which integrates LLMs for reasoning, context (via threads), and tools.
- **Domain Layer**: Core business logic, including tools and functions. Tools are defined via Model Context Protocol (MCP) or OpenAPI specs, encapsulating actions like API calls or data queries.
- **Infrastructure Layer**: Integrates external services, e.g., LLM providers (Azure OpenAI), databases for state persistence, and observability tools like OpenTelemetry.

Example Python snippet for a simple layered agent:

```python
from agent_framework import AIAgent, ChatClient, AIFunctionFactory

# Infrastructure: LLM client
client = ChatClient(model="gpt-4o-mini")

# Domain: Define a tool
def add_numbers(a: int, b: int) -> int:
    return a + b
tool = AIFunctionFactory.create(add_numbers)

# Application: Create agent
agent = AIAgent(client=client, tools=[tool])

# Presentation: Interact
response = agent.process("What is 5 + 3?")
print(response)
```

### Onion Architecture (For Complex, Domain-Driven Projects)

- **Core (Domain Model)**: Pure Python classes for agent behaviors, independent of external dependencies. Focus on entities like `AgentThread` for state and `ContextProvider` for memory.
- **Inner Layers**: Add repositories or adapters for tools and MCP integrations.
- **Outer Layers**: Plug in infrastructure (e.g., LLM clients) and interfaces.
This hexagonal pattern keeps the core testable and adaptable, ideal for evolving AI systems. MAF's composability supports this by allowing workflows to nest agents and functions without tight coupling.

For multi-agent systems, use MAF Workflows (graph-based) to define explicit execution paths, supporting patterns like sequential, concurrent, handoff, or Magentic (group chat). This extends layered/onion patterns for orchestration.

In VS Code, visualize architectures using extensions like PlantUML or Draw.io for diagrams.

## Code Review

Conduct code reviews to ensure robustness, security, and efficiency in AI agent projects. Use VS Code's Git integration or extensions like GitHub Pull Requests for collaborative reviews.

### Key Review Checklist

1. **Modularity and Readability**: Ensure agents are composable. Check for single-responsibility principle—e.g., one agent per specialized task (researcher, summarizer). Use type hints and docstrings for Python code.
2. **Error Handling and Resilience**: Verify retries, checkpointing in workflows, and middleware for authentication/rate limiting. Test for LLM failures using MAF's built-in filters.
3. **Performance and Cost**: Review tool calls to minimize unnecessary LLM invocations. Use telemetry (OpenTelemetry integration) to monitor latency and token usage.
4. **Security and Responsible AI**: Check for data sharing risks in MCP integrations. Implement safeguards like content filters to prevent harmful outputs.
5. **Testing**: Require unit tests for tools/functions (e.g., via `pytest`) and integration tests for workflows. Use MAF's evaluation tools for A/B testing agent responses.
6. **Documentation**: Inline comments for complex logic; update this AGENTS.md for project-specific adaptations.

Process: In VS Code, use Live Share for real-time reviews. Aim for <200 LOC per PR to focus on AI-specific issues like non-determinism in LLM responses.

## Avoiding Anti-Patterns

MAF helps mitigate common pitfalls in AI agent development. Key anti-patterns to avoid:

1. **Over-Reliance on Single Agents for Complex Tasks**: Anti-Pattern: Using one agent with 20+ tools, leading to hallucination or inefficiency. Solution: Decompose into workflows with specialized agents. MAF workflows provide type-safe routing and checkpointing.

2. **Using Agents for Structured Tasks**: Anti-Pattern: Employing LLMs for rule-based logic (e.g., simple calculations), increasing cost/latency. Solution: Prefer pure Python functions; reserve agents for unstructured, exploratory tasks.

3. **Ignoring State Management**: Anti-Pattern: Stateless agents in multi-turn conversations, causing context loss. Solution: Use MAF's `AgentThread` for persistent state and human-in-the-loop support.

4. **Tight Coupling to Providers**: Anti-Pattern: Hardcoding LLM clients, limiting portability. Solution: Abstract via MAF's model clients; support multiple providers (OpenAI, Azure).

5. **Neglecting Observability**: Anti-Pattern: Building without monitoring, leading to undetectable failures. Solution: Integrate OpenTelemetry from the start for tracing workflows.

6. **Premature Scaling**: Anti-Pattern: Over-engineering small projects with full workflows. Solution: Start simple and compose as needed.

In VS Code, use linters like Pylint or Ruff to catch code smells early.

## Project Scale-Based Framework Proposals

Tailor your approach to project size using MAF's flexible building blocks. Recommendations assume Python as the primary language.

### Small Projects (Prototypes, Single-Developer, <1K LOC)

- **Framework**: Core MAF for single agents. No heavy dependencies.
- **Approach**: Build interactive agents for tasks like chatbots or code generators. Use VS Code's Jupyter extension for rapid prototyping.
- **Example**: A customer support agent processing queries with 2-3 tools.
- **Why**: Minimizes overhead; focus on LLM integration and basic tools.

### Medium Projects (Team of 2-5, Multi-Agent, 1K-10K LOC)

- **Framework**: MAF Workflows + lightweight web framework like FastAPI for hosting.
- **Approach**: Orchestrate 3-5 agents in patterns like sequential (e.g., writer → editor). Add middleware for logging. Use Git for collaboration in VS Code.
- **Example**: Research assistant with researcher, fact-checker, and summarizer agents.
- **Why**: Handles moderate complexity with composability; add observability via OpenTelemetry.

### Large Projects (Enterprise, 5+ Developers, >10K LOC, Production Deployment)

- **Framework**: MAF + Azure AI Foundry for deployment. Integrate with full-stack tools like Django/Flask for APIs, databases (e.g., PostgreSQL for state), and CI/CD (GitHub Actions).
- **Approach**: Use nested workflows for multi-step processes (e.g., financial transactions). Include responsible AI features, evaluations for testing, and A2A protocol for third-party integrations. Deploy to Azure for scalability and compliance.
- **Example**: Global supply chain automation with multiple agents, human-in-the-loop, and error recovery.
- **Why**: Supports durability, telemetry, and governance for regulated environments. In VS Code, use multi-root workspaces for modular codebases.

For all scales, start with MAF's preview features and contribute feedback via GitHub. Monitor updates, as MAF is in public preview as of October 2025.

## Resources

- Official Docs: [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- GitHub Repo: Search for "microsoft/agent-framework" on GitHub.
- VS Code Extensions: Python, GitHub Copilot (for AI-assisted coding), Markdown All in One.

This document evolves with your project—update it via VS Code's Markdown editor. For FIRE (Financial Independence, Retire Early) goals, consider agents for automation in finance or productivity tools.
