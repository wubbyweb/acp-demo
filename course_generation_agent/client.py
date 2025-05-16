import asyncio
from contextlib import suppress

from acp_sdk.client import Client
from acp_sdk.models import (
    Message,
    MessagePart,
    MessagePartEvent,
    MessageCompletedEvent,
    ErrorEvent,
    RunFailedEvent,
    RunCompletedEvent,
)

async def run_course_generation_client():
    """
    An asynchronous client to interact with the course_generator ACP agent.
    It prompts the user for a topic, sends it to the agent, and prints the streamed response.
    """
    topic = input("Enter the course topic: ")
    if not topic.strip():
        print("Topic cannot be empty.")
        return

    user_message = Message(parts=[MessagePart(content=topic, content_type="text/plain", role="user")])

    print("Assistant:")
    try:
        async with Client(base_url="http://localhost:8000") as client:
            # Use run_stream to get incremental updates
            async for event in client.run_stream(agent="course_generator", input=[user_message]):
                if isinstance(event, MessagePartEvent):
                    # Print each part of the message as it arrives
                    print(event.part.content, flush=True)
                elif isinstance(event, MessageCompletedEvent):
                    # Optionally, do something when a full message from the agent is completed
                    # print("\n--- Agent Message Complete ---")
                    pass
                elif isinstance(event, RunCompletedEvent):
                    # The run has finished successfully
                    # print("\n--- Agent Run Successfully Completed ---")
                    pass
                elif isinstance(event, (ErrorEvent, RunFailedEvent)):
                    # Handle errors from the agent or the run
                    error_message = event.error.message if isinstance(event, ErrorEvent) else event.run.error.message
                    print(f"\nError: {error_message}", flush=True)
                    break # Stop processing on error
                # You can add more event handling as needed (e.g., for thoughts, tool calls if the agent supported them)

    except ConnectionRefusedError:
        print("\nError: Could not connect to the ACP server. Is it running on http://localhost:8000?")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print() # Ensure a newline at the end

if __name__ == "__main__":
    with suppress(KeyboardInterrupt): # Allow graceful exit with Ctrl+C
        asyncio.run(run_course_generation_client())
