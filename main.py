import json
import os
import argparse
from pyexpat.errors import messages
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function



def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
            raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")


    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": args.user_prompt},
    ]



    
    result_message = None
    
    for i in range(20):    
        #print("Hello from ai-agent-project!")

        if i == 19:
            raise RuntimeError("Maximum number of iterations reached.  Likely the model is not returning a response.")

        # Now we can access `args.user_prompt`

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message


        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            if response.usage.completion_tokens == None:
                raise RuntimeError("Response does not contain completion tokens.  Likely the model is not returning a response.  Check your API key and model name.")
            print(f"Response tokens: {response.usage.completion_tokens}")
            if response.usage.total_tokens == None:
                raise RuntimeError("Response does not contain total tokens.  Likely the model is not returning a response.  Check your API key and model name.")


        messages.append(message)


        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise RuntimeError("Function call did not return a result message.  Likely the model is not returning a response.  Check your API key and model name.")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            return message.content



if __name__ == "__main__":
    main()
