from openai import OpenAI
from dotenv import load_dotenv
import requests
import json

load_dotenv()

client = OpenAI()

def get_weather(city: str) :
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"Weather in {city}: {response.text}"
    return "Weather information not available."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]



def main():
    user_query = input("What is your question? ")

    messages = [
        {"role": "system", "content": "Use the get_weather tool whenever user asks about weather."},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

       # 🔥 Check if tool is called
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "get_weather":
            result = get_weather(arguments["city"])

            # Append tool response
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            # 🔁 Send back to model for final response
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            print("Response Tool Called:", second_response.choices[0].message.content)

    else:
        print("Response:", message.content)

main()
