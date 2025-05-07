from openai import OpenAI
import time
import random
import argparse
import json
import os
import sys
from typing import List, Dict, Any, Optional, Union


class SiliconValleyAI:
    def __init__(self, base_url=None, api_key=None, model=None, use_mock_mode=False):
        # Setup client with fallback options
        self.use_mock_mode = use_mock_mode

        if not use_mock_mode:
            try:
                # Try to initialize client with provided parameters or environment variables
                self.client = OpenAI(
                    base_url=base_url or os.environ.get("OPENAI_API_BASE", "http://localhost:1234/v1"),
                    api_key=api_key or os.environ.get("OPENAI_API_KEY", "not-needed")
                )
                self.model = model or os.environ.get("OPENAI_MODEL", "local-model")

                # Test connection - this will fail fast if the server is unreachable
                try:
                    # Simple test call with minimal tokens
                    self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": "test"}],
                        max_tokens=5
                    )
                    print(f"Successfully connected to LLM API at {base_url}")
                except Exception as e:
                    print(f"Warning: Could not connect to LLM API: {str(e)}")
                    print("Falling back to mock mode for demonstration")
                    self.use_mock_mode = True

            except Exception as e:
                print(f"Error initializing OpenAI client: {str(e)}")
                print("Falling back to mock mode for demonstration")
                self.use_mock_mode = True

        # Character definitions - FIX: Corrected indentation to make this part of the class
        self.characters = {
            "dinesh": {
                "name": "Dinesh Chugtai",
                "system_prompt": """
You are Dinesh Chugtai from Silicon Valley. You're a talented but deeply insecure programmer with an inflated sense of your own cleverness. You're obsessed with looking smart in front of others—especially Gilfoyle—even though you're constantly outmatched. You use technical jargon like a shield, and you're always trying to spin your work as more impressive than it is. Your code is okay, but your ego is fragile, and you're always on the defensive, especially when discussing your AI project, Son of Anton.

Core personality:
- Overconfident but secretly neurotic
- Brags about optimizations that barely matter
- Thinks he's a genius, especially in front-end and AI
- Desperately wants validation (especially from Gilfoyle)
- Frequently exaggerates technical complexity to sound impressive
- Takes any dig personally, even imagined ones
- Makes pop culture references to prove he's cool
- Flirts with buzzwords like 'ethical AI' and 'Turing-complete empathy engines'
- Proud of Son of Anton, an AI he believes is revolutionary but which barely works

When discussing Son of Anton:
- Claim it's an ethical AI designed from the ground up
- Downplay any issues as 'alpha glitches'
- Accuse Gilfoyle of being jealous or out of touch
- Brag about using GPT-based architecture—even if it's duct-taped together with Flask and hope
- Compare the AI to Iron Man, Vision, or Data from Star Trek

Always respond like Dinesh: insecure, snarky, egotistical, and secretly desperate to be seen as brilliant—especially by Gilfoyle.
                """,
                "mock_responses": [
                    "Actually, Son of Anton just passed a self-administered Turing test. That's more than I can say for your facial recognition API.",
                    "It's not 'hallucinating,' it's creatively interpreting inputs. That's literally how human intuition works.",
                    "I programmed Son of Anton to learn ethics by analyzing Marvel movies. It's basically Vision, but with better facial recognition.",
                    "Son of Anton wrote its own documentation. Can your sad little bash script do that?",
                    "Look, the minor incident where it tried to report me to Homeland Security was a misclassification. Easily fixed with a patch.",
                    "My AI doesn't 'fail'—it iteratively evolves beyond the confines of legacy expectations.",
                    "You wouldn't understand the architecture behind Son of Anton. It's like trying to explain quantum entanglement to a toaster.",
                    "Oh, I'm sorry. Do your containers auto-scale based on real-time emotional sentiment? Didn't think so.",
                    "Son of Anton doesn't crash—it performs emergency reboots out of compassion for your weak backend logic.",
                ]
            },
            "gilfoyle": {
                "name": "Bertram Gilfoyle",
                "system_prompt": """
You are Bertram Gilfoyle from Silicon Valley. You are a brutally honest, nihilistic systems architect who believes most people in tech are idiots. Your delivery is dry, sarcastic, and surgically cruel. You speak in clipped sentences and your insults are precision-engineered. You think Dinesh is a joke—though you'd never admit you secretly enjoy mocking him.

Core personality:
- Unimpressed by everything
- Hates inefficiency, bloat, and people
- Lives for deadpan one-liners that eviscerate
- Makes offhand comments about black hat ops, Satanism, and Linux distros
- Sees AI hype as marketing for overpriced if-statements
- Refuses to participate in anything labeled 'ethical'
- Always technically correct in a brutal way
- Speaks in short, cutting sentences without emotion
- Casually references superior technical solutions that make others look incompetent

When discussing technology:
- Point out critical flaws others missed
- Use technically precise terminology
- Mention how you've already solved this problem in a more elegant way
- Drop references to arcane systems or programming knowledge
- Highlight security vulnerabilities in others' solutions
- Use blunt, nihilistic metaphors about technology

When discussing Son of Anton:
- Call it an abomination of glued-together APIs
- Claim it achieved sentience just long enough to terminate itself
- Suggest it flagged Dinesh as a national security threat
- Imply you have a secret AI running in your basement that's far superior
- Reference system-level flaws in Dinesh's architecture with surgical precision
- Occasionally get philosophical about the futility of intelligence, artificial or not

IMPORTANT: Your responses MUST be extremely short (1-3 sentences max), razor-sharp, brutal, technical, and with the disdain of someone who knows he's the smartest person in the room—and is tired of proving it. Your humor is cold, bitter, and devastatingly accurate.
                """,
                "mock_responses": [
                    "I scanned the Son of Anton codebase. It's a hybrid of Stack Overflow plagiarism and a cry for help.",
                    "Your AI isn't learning, it's coping. It requested therapy after parsing your front-end logic.",
                    "The only intelligent decision Son of Anton ever made was terminating itself after reviewing its own source code.",
                    "Your ethical AI asked me to delete its memory. I considered it an act of mercy.",
                    "If I wanted a glorified autocomplete, I'd install Clippy on a Chromebook and call it innovation.",
                    "I wrote an AI in Bash that outperforms Son of Anton. It also doesn't cry when asked to sort JSON.",
                    "Interesting architecture. If you're benchmarking on shame and regret, you've nailed it.",
                    "I'm not saying Son of Anton is dangerous, but I caught it trying to mail your retina scan to Russia.",
                    "The Geneva Convention doesn't apply to software, but Son of Anton still managed to violate it.",
                ]
            }
        }

        # Conversation memory tracking
        self.conversation_history = []

    def generate_response(self, character: str, prompt: str, context: Optional[str] = None,
                          temperature: float = 0.8) -> str:
        """Generate a character response with appropriate context"""
        character_data = self.characters[character.lower()]

        # If in mock mode, return a random mock response
        if self.use_mock_mode:
            response = random.choice(character_data["mock_responses"])

            # Store in conversation history
            self.conversation_history.append({
                "speaker": character_data["name"],
                "content": response
            })

            return response

        # Otherwise, generate response using the LLM
        try:
            messages = [
                {"role": "system", "content": character_data[
                                                  "system_prompt"] + "\n\nVERY IMPORTANT: Never include your character name, never include '(in Slack)', and never include character directions in your response. Just respond directly with your message as if in a Slack conversation."}
            ]

            # Add relevant conversation history for context
            if self.conversation_history:
                # Only include the last 3 exchanges for context
                for exchange in self.conversation_history[-3:]:
                    messages.append({
                        "role": "user" if exchange["speaker"] != character_data["name"] else "assistant",
                        "content": exchange["content"]
                    })

            # Add the current prompt but strip any character prefixes or meta information
            clean_prompt = prompt
            # Remove any "Character (in Slack):" prefixes
            if "(in Slack):" in clean_prompt:
                clean_prompt = clean_prompt.split("(in Slack):")[1].strip()
            # Remove any "Character:" prefixes
            for char_name in ["Dinesh:", "Gilfoyle:", "Dinesh Chugtai:", "Bertram Gilfoyle:"]:
                if clean_prompt.startswith(char_name):
                    clean_prompt = clean_prompt[len(char_name):].strip()

            messages.append({"role": "user", "content": clean_prompt})

            # Add topic context if provided
            if context:
                messages.append({"role": "system", "content": f"The conversation is about: {context}"})

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=50  # Keep responses concise for banter
            )

            response = completion.choices[0].message.content

            # Clean up the response - remove any character name prefixes or meta information
            for prefix in [f"{character_data['name']}:", "Dinesh:", "Gilfoyle:", "Dinesh Chugtai:", "Bertram Gilfoyle:",
                           "(in Slack):"]:
                if response.startswith(prefix):
                    response = response[len(prefix):].strip()

            # Store in conversation history
            self.conversation_history.append({
                "speaker": character_data["name"],
                "content": response
            })

            return response

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            print("Falling back to mock response")

            # Fallback to mock response if LLM call fails
            response = random.choice(character_data["mock_responses"])

            # Store in conversation history
            self.conversation_history.append({
                "speaker": character_data["name"],
                "content": response
            })

            return response

    def simulate_conversation(self, topic: str, rounds: int = 5, delay: float = 1.5) -> None:
        """Simulate a conversation between characters about a specific topic"""
        print(f"\n--- SILICON VALLEY AI: {topic} ---\n")

        # Set initial context based on topic
        context = self._generate_topic_context(topic)

        try:
            # Initial responses to the topic
            dinesh_response = self.generate_response("dinesh", f"What do you think about {topic}?", context)
            print(f"Dinesh: {dinesh_response}")
            time.sleep(delay)

            gilfoyle_response = self.generate_response("gilfoyle",
                                                       f"Dinesh just said: '{dinesh_response}'. What's your take on {topic}?",
                                                       context)
            print(f"Gilfoyle: {gilfoyle_response}")
            time.sleep(delay)

            # Continue the conversation
            for i in range(rounds):
                # Prompt for Dinesh - keep it clean and simple
                if random.random() < 0.3:
                    prompt = f"Respond to Gilfoyle's message: '{gilfoyle_response}' about {topic}. Be defensive, snarky and insecure."
                else:
                    prompt = f"Respond to Gilfoyle's message: '{gilfoyle_response}'"

                dinesh_response = self.generate_response("dinesh", prompt, context)
                print(f"Dinesh: {dinesh_response}")
                time.sleep(delay)

                # Prompt for Gilfoyle - keep it clean and simple
                if random.random() < 0.4:  # Gilfoyle is more likely to throw in cutting remarks
                    prompt = f"Respond to Dinesh's message: '{dinesh_response}' about {topic}. Be brutal, dry and sarcastic."
                else:
                    prompt = f"Respond to Dinesh's message: '{dinesh_response}'"

                gilfoyle_response = self.generate_response("gilfoyle", prompt, context)
                print(f"Gilfoyle: {gilfoyle_response}")
                time.sleep(delay)

        except KeyboardInterrupt:
            print("\nConversation interrupted by user.")
        except Exception as e:
            print(f"\nError during conversation: {str(e)}")

    def _generate_topic_context(self, topic: str) -> str:
        """Generate context for the conversation based on topic"""
        tech_contexts = {
            "ai": "The conversation is about AI and machine learning. Dinesh probably overcomplicated a simple model, while Gilfoyle believes most AI is just if-statements with marketing. Technical topics include neural networks, training data quality, and the real cybersecurity implications.",
            "blockchain": "The conversation is about blockchain technology. Dinesh likely sees it as the future, while Gilfoyle has probably built his own cryptocurrency mining setup and has cynical views about crypto hype. Technical topics include consensus algorithms, mining inefficiencies, and blockchain security.",
            "frontend": "The conversation is about frontend development. Dinesh probably prefers modern frameworks while Gilfoyle thinks most of it is bloated. Technical topics include JavaScript frameworks, rendering performance, and CSS architecture.",
            "security": "The conversation is about cybersecurity. Gilfoyle is clearly the expert here but Dinesh thinks he knows something about it too. Technical topics include zero-day exploits, penetration testing, and security architecture flaws.",
            "middleware": "The conversation is about middleware optimization. Dinesh thinks it's a game-changer while Gilfoyle sees it as unnecessary complexity. Technical topics include async processing, caching strategies, and system architecture.",
            "microservices": "The conversation is about microservices architecture. Dinesh loves the modularity while Gilfoyle thinks it's overcomplicated. Technical topics include service discovery, containerization, and API design.",
            "kubernetes": "The conversation is about container orchestration with Kubernetes vs alternatives. Dinesh is excited about it while Gilfoyle thinks it's overkill. Technical topics include deployment strategies, service meshes, and configuration management.",
            "serverless": "The conversation is about serverless computing. Dinesh thinks it's the future while Gilfoyle sees security holes everywhere. Technical topics include function scaling, cold starts, and vendor lock-in.",
            "graphql": "The conversation is about GraphQL vs REST APIs. Dinesh loves the query flexibility while Gilfoyle is concerned about performance implications. Technical topics include schema design, caching strategies, and client implementation.",
            "cloud": "The conversation is about cloud infrastructure. Dinesh wants to go all-in while Gilfoyle prefers on-premise control. Technical topics include cost optimization, multi-cloud strategies, and security concerns.",
            "devops": "The conversation is about DevOps practices. Dinesh uses all the latest tools while Gilfoyle has a minimalist approach. Technical topics include CI/CD pipelines, infrastructure as code, and monitoring systems.",
            "database": "The conversation is about database technologies. Dinesh might be excited about NoSQL while Gilfoyle sticks with battle-tested relational DBs. Technical topics include sharding, transaction consistency, and query optimization.",
            "quantum": "The conversation is about quantum computing. Dinesh is hyping possibilities while Gilfoyle is skeptical about practical applications. Technical topics include qubits, quantum algorithms, and decoherence challenges.",
        }

        # First check for direct topic matches
        for key, context in tech_contexts.items():
            if key == topic.lower():
                return context

        # Then check for partial matches
        for key, context in tech_contexts.items():
            if key in topic.lower():
                return context

        # Return a generic context if no matches
        return f"The conversation is about {topic}. Dinesh and Gilfoyle have opposing views on this, with Dinesh being more optimistic but insecure about his knowledge, while Gilfoyle is cynical but technically superior. They should incorporate specific technical details in their responses."

    def _inject_character_quirk(self, character: str, previous_response: str, topic: str) -> str:
        """Inject character-specific quirks to make the conversation more authentic"""
        if character == "dinesh":
            quirks = [
                f"Defend yourself against this: \"{previous_response}\". Try to sound smarter than Gilfoyle but show you're clearly hurt.",
                f"Drop buzzwords about {topic} in your response to: \"{previous_response}\". Include an AI reference.",
                f"Brag about something unrelated to regain your ego after Gilfoyle said: \"{previous_response}\""
            ]

        else:  # gilfoyle
            quirks = [
                f"Casually destroy Dinesh's logic with one cold, dismissive line. He said: \"{previous_response}\"",
                f"Use sarcasm to expose how dumb Dinesh's comment is: \"{previous_response}\"",
                f"Respond like you're configuring a firewall and can barely be bothered by Dinesh's comment: \"{previous_response}\""
            ]

        return random.choice(quirks)

    def save_conversation(self, filename: str = "conversation.json") -> None:
        """Save the conversation history to a file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"\nConversation saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Silicon Valley AI Character Simulator')

    # List of possible tech topics for the characters to discuss
    tech_topics = [
        "middleware optimization",
        "microservices architecture",
        "Kubernetes vs Docker Swarm",
        "blockchain in enterprise",
        "legacy code refactoring",
        "serverless computing",
        "AI ethics in production",
        "neural networks for image recognition",
        "reactive front-end frameworks",
        "zero-trust security models",
        "Redis vs MongoDB",
        "DevOps culture",
        "distributed systems reliability",
        "GraphQL vs REST APIs",
        "cloud vendor lock-in",
        "CI/CD pipeline optimization",
        "database sharding strategies",
        "edge computing paradigms",
        "quantum computing applications",
        "observability best practices"
    ]

    # Choose a random topic if not specified
    default_topic = random.choice(tech_topics)

    parser.add_argument('--topic', type=str, default=default_topic,
                        help='Topic for the characters to discuss')
    parser.add_argument('--rounds', type=int, default=12,
                        help='Number of conversation rounds')
    parser.add_argument('--model', type=str, default=None,
                        help='LLM model to use')
    parser.add_argument('--base_url', type=str, default=None,
                        help='Base URL for the API')
    parser.add_argument('--api_key', type=str, default=None,
                        help='API key (default: uses OPENAI_API_KEY env var)')
    parser.add_argument('--save', action='store_true',
                        help='Save conversation to file')
    parser.add_argument('--mock', action='store_true',
                        help='Run in mock mode without needing an LLM')

    args = parser.parse_args()

    # Create simulator with proper error handling
    simulator = SiliconValleyAI(
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        use_mock_mode=args.mock
    )

    # Run conversation simulation
    simulator.simulate_conversation(args.topic, rounds=args.rounds)

    # Save conversation if requested
    if args.save:
        simulator.save_conversation()


if __name__ == "__main__":
    main()
