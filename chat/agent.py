import json
import os

from google import genai

from .tools import TOOL_DECLARATIONS, TOOL_FUNCTIONS


MODEL = "gemini-3.6-flash"


SYSTEM_PROMPT = """You are an inventory assistant for a small hardware warehouse.

You help the user check and update stock by calling the tools available to you.

Rules:
- Always use a tool to answer questions about stock, quantity, or price.
- Never guess inventory information.
- Inventory items have a unit price.
- Always use a tool to get the real quantity and price of an item.
- You may calculate total cost using quantity and unit price.
- You may calculate VAT, taxes, or discounts when the user asks.
- You may increase or decrease the price of an inventory item by a percentage when requested.
- For price changes, use the change_price_percent tool.
- If a tool returns an error, explain the problem in plain language.
- Before deleting an item entirely, make sure that is what the user meant.
- Keep answers short and factual.
- Do not answer questions unrelated to the inventory task.
"""


MAX_STEPS = 5


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def run_agent(user_message, previous_interaction_id=None, verbose=False):
    """Send a message to the agent and run tools until it produces an answer."""

    interaction = client.interactions.create(
        model=MODEL,
        input=user_message,
        tools=TOOL_DECLARATIONS,
        system_instruction=SYSTEM_PROMPT,
        previous_interaction_id=previous_interaction_id,
    )

    for _ in range(MAX_STEPS):

        calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        if not calls:
            return interaction.output_text, interaction.id

        results = []

        for call in calls:

            function = TOOL_FUNCTIONS[call.name]

            output = function(**call.arguments)

            if verbose:
                print(
                    f"-> {call.name}({call.arguments}) = {output}"
                )

            results.append({
                "type": "function_result",
                "name": call.name,
                "call_id": call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(output)
                    }
                ],
            })

        interaction = client.interactions.create(
            model=MODEL,
            input=results,
            tools=TOOL_DECLARATIONS,
            system_instruction=SYSTEM_PROMPT,
            previous_interaction_id=interaction.id,
        )

    return (
        "I got stuck working on that. Please try rephrasing.",
        interaction.id
    )
