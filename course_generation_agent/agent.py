import asyncio
from collections.abc import AsyncGenerator
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, RunYield, RunYieldResume, Server

load_dotenv()  # Load environment variables from .env file
# Initialize the OpenAI client

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_course_content(topic: str) -> dict:
    """Generate course content using OpenAI."""
    prompt = f"""Create a detailed course outline for '{topic}'. Include:
    1. A brief course description
    2. 5 modules with their titles
    3. Brief instructor notes for each module
    Format as JSON with keys: description, modules (array of objects with title and notes)"""
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return eval(response.choices[0].message.content)

# Initialize the ACP server
server = Server()

@server.agent(name="course_generator")
async def course_generator_agent(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    Generates a basic course outline for a given topic.
    Accepts a topic as a simple text message.
    Yields parts of the course outline as separate MessagePart objects.
    """
    # For simplicity, this agent expects a single message with a single text part as input.
    # In a real application, you might want more robust input parsing.
    if not input or not input[0].parts:
        yield MessagePart(content="Error: No topic provided.", content_type="text/plain", role="assistant")
        return

    topic = str(input[0].parts[0].content).strip()
    if not topic:
        yield MessagePart(content="Error: Topic cannot be empty.", content_type="text/plain", role="assistant")
        return

    # Simulate some processing delay
    await asyncio.sleep(0.2)
    yield MessagePart(
        content=f"Course Outline for: {topic}",
        content_type="text/plain",
        role="assistant"
    )
    await asyncio.sleep(0.2)

    # Generate course content using OpenAI
    course_content = await generate_course_content(topic)
    
    yield MessagePart(
        content=f"Course Outline for: {topic}\n\n{course_content['description']}",
        content_type="text/plain",
        role="assistant"
    )
    await asyncio.sleep(0.2)

    # Output each module with its instructor notes
    for module in course_content['modules']:
        yield MessagePart(
            content=f"\n{module['title']}\nInstructor Notes: {module['notes']}",
            content_type="text/plain",
            role="assistant"
        )
        await asyncio.sleep(0.1)

    yield MessagePart(
        content="\nNote: This course outline was generated using OpenAI. Feel free to modify it according to your needs.",
        content_type="text/plain",
        role="assistant"
    )

def main():
    """
    Main function to run the ACP server.
    This allows the script to be executed directly.
    """
    print("Starting Course Generation ACP Agent Server on http://localhost:8000...")
    print("Available agents: /agents")
    print("Run agent: POST /runs with body {'agent_name': 'course_generator', 'input': [{'parts': [{'content': 'Your Topic'}]}]}")
    server.run()

if __name__ == "__main__":
    main()
