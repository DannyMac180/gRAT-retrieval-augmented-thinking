from google import genai
import os
from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from openai import OpenAI
import time

# Model Constants
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp"
OPENROUTER_MODEL = "openai/gpt-4o-mini"

# Load environment variables
load_dotenv()

class ModelChain:
    def __init__(self):
        # Initialize Gemini client
        self.gemini_client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY"),
            http_options={'api_version':'v1alpha'}
        )
        
        # Initialize OpenRouter client
        self.openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        
        self.gemini_messages = []
        self.openrouter_messages = []
        self.current_model = OPENROUTER_MODEL
        self.show_reasoning = True

    def set_model(self, model_name):
        self.current_model = model_name

    def get_model_display_name(self):
        return self.current_model

    def get_deepseek_reasoning(self, user_input):
        start_time = time.time()
        self.gemini_messages.append(user_input)
        
        if self.show_reasoning:
            rprint("\n[blue]Reasoning Process[/]")
        
        config = {'thinking_config': {'include_thoughts': True}}
        reasoning_content = ""
        
        for chunk in self.gemini_client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=user_input,
            config=config
        ):
            for part in chunk.candidates[0].content.parts:
                if part.thought:
                    reasoning_piece = part.text
                    reasoning_content += reasoning_piece
                    if self.show_reasoning:
                        print(f"Model Thought:\n{reasoning_piece}\n", end="", flush=True)
                else:
                    print(f"\nModel Response:\n{part.text}\n", end="", flush=True)

        elapsed_time = time.time() - start_time
        if elapsed_time >= 60:
            time_str = f"{elapsed_time/60:.1f} minutes"
        else:
            time_str = f"{elapsed_time:.1f} seconds"
        rprint(f"\n\n[yellow]Thought for {time_str}[/]")
        
        if self.show_reasoning:
            print("\n")
        return reasoning_content

    def get_openrouter_response(self, user_input, reasoning):
        combined_prompt = (
            f"<question>{user_input}</question>\n\n"
            f"<thinking>{reasoning}</thinking>\n\n"
        )
        
        self.openrouter_messages.append({"role": "user", "content": combined_prompt})
        
        rprint(f"[green]{self.get_model_display_name()}[/]")
        
        try:
            completion = self.openrouter_client.chat.completions.create(
                model=self.current_model,
                messages=self.openrouter_messages,
                stream=True
            )
            
            full_response = ""
            for chunk in completion:
                try:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content is not None:
                        content_piece = delta.content
                        full_response += content_piece
                        print(content_piece, end="", flush=True)
                except Exception as e:
                    rprint(f"\n[red]Error processing chunk: {str(e)}[/]")
                    continue
                    
        except Exception as e:
            rprint(f"\n[red]Error in streaming response: {str(e)}[/]")
            return "Error occurred while streaming response"
        
        self.gemini_messages.append({"role": "assistant", "content": full_response})
        self.openrouter_messages.append({"role": "assistant", "content": full_response})
        
        print("\n")
        return full_response

def main():
    chain = ModelChain()
    
    # Initialize prompt session with styling
    style = Style.from_dict({
        'prompt': 'orange bold',
    })
    session = PromptSession(style=style)
    
    rprint(Panel.fit(
        "[bold cyan]Gemini Retrieval augmented thinking[/]",
        title="[bold cyan]gRAT [/]",
        border_style="cyan"
    ))
    rprint("[yellow]Commands:[/]")
    rprint(" • Type [bold red]'quit'[/] to exit")
    rprint(" • Type [bold magenta]'model <name>'[/] to change the OpenRouter model")
    rprint(" • Type [bold magenta]'reasoning'[/] to toggle reasoning visibility")
    rprint(" • Type [bold magenta]'clear'[/] to clear chat history\n")
    
    while True:
        try:
            user_input = session.prompt("\nYou: ", style=style).strip()
            
            if user_input.lower() == 'quit':
                print("\nGoodbye! ")
                break

            if user_input.lower() == 'clear':
                chain.gemini_messages = []
                chain.openrouter_messages = []
                rprint("\n[magenta]Chat history cleared![/]\n")
                continue
                
            if user_input.lower().startswith('model '):
                new_model = user_input[6:].strip()
                chain.set_model(new_model)
                print(f"\nChanged model to: {chain.get_model_display_name()}\n")
                continue

            if user_input.lower() == 'reasoning':
                chain.show_reasoning = not chain.show_reasoning
                status = "visible" if chain.show_reasoning else "hidden"
                rprint(f"\n[magenta]Reasoning process is now {status}[/]\n")
                continue
            
            reasoning = chain.get_deepseek_reasoning(user_input)
            openrouter_response = chain.get_openrouter_response(user_input, reasoning)
            
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == "__main__":
    main()