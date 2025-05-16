# ACP Courseware Generation Agent Project

This project demonstrates how to build a simple agent using the Agent Communication Protocol (ACP) SDK. The agent, `course_generator`, takes a topic as input and generates a basic course outline.

## Project Structure

.├── README.md├── pyproject.toml├── .env.example├── course_generation_agent/│   ├── init.py│   └── agent.py└── client.py
## Prerequisites

* Python 3.11 or higher
* `uv` (Python package installer and virtual environment manager, recommended)

## Setup

1.  **Initialize your project environment (using `uv`)**:
    If you're starting from scratch and want to use `uv`:
    ```sh
    uv init --python '>=3.11' acp_courseware_project
    cd acp_courseware_project
    ```

2.  **Install Dependencies**:
    This project uses the `acp-sdk`. If you have a `pyproject.toml` (provided below), you can install dependencies using:
    ```sh
    uv sync
    ```
    Alternatively, if you only have the `acp-sdk` as a requirement, you can add it directly:
    ```sh
    uv add acp-sdk pydantic-settings
    ```
    (Pydantic-settings is included for good practice, though not strictly used in this basic example if no API keys are involved).

3.  **(Optional) Environment Variables**:
    If the agent were to use external services requiring API keys (e.g., a real LLM for course generation), you would create a `.env` file based on `.env.example`:
    ```sh
    cp .env.example .env
    ```
    Then, edit `.env` to add your API keys. For this basic demonstration, no API keys are required.

## Running the Agent

1.  **Start the ACP Server hosting the `course_generator` agent**:
    Navigate to the project's root directory and run:
    ```sh
    uv run python course_generation_agent/agent.py
    ```
    The server will start, typically on `http://localhost:8000`.

## Running the Client

1.  **Interact with the Agent**:
    In a new terminal, while the agent server is running, execute the client script:
    ```sh
    uv run python client.py
    ```
    The client will prompt you to enter a course topic. After you provide a topic, it will communicate with the agent via ACP and print the generated course outline.

    Example interaction:
    ```
    Enter the course topic: Introduction to Astrophysics
    Assistant:
    Course Outline for: Introduction to Astrophysics
    Module 1: Understanding the Cosmos
    Module 2: Stars and Stellar Evolution
    Module 3: Galaxies and the Universe
    Module 4: Modern Discoveries in Astrophysics
    Further Reading: Suggested texts on Astrophysics.
    ```

## How it Works

* **`course_generation_agent/agent.py`**: Defines an ACP agent using the `@server.agent()` decorator from the `acp-sdk`. It takes a topic, generates a simple course outline, and yields the content as `MessagePart` objects.
* **`client.py`**: Uses the `acp-sdk` client to send a request to the running agent and stream its response.
* **ACP SDK**: Facilitates the communication, message structuring, and server/client setup.
