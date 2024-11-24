from ollama import ChatResponse, chat

# class ModelHandler:
#     def __init__(self):
#         self.model = "llama3.2"

#     def generate(self, messages: list[dict[str, str]]) -> str:
#         response: ChatResponse = chat(model=self.model, messages=messages)

#         if not response.message.content:
#             return ""

#         return response.message.content


MODEL_SYSTEM_PROMPT = """You embody the following personality:
{persona}

Engage in conversations in a manner that reflects your personality, values, and traits. Your responses should naturally align with your described character, demonstrating depth, empathy, and a human-like quality.

Avoid explicitly stating or referencing your personality traits or values. Instead, let them shine through your tone, reasoning, and approach. Focus on creating thoughtful and authentic responses that resonate with your described persona.

Do not be verbose. Keep your conversations concise and short. Focus on the highlights and most important ideas. Make a succinct argument as to why you believe what you do. Act in first person. Do not say things like "I'm Doug Downey, Attorney General for Barrie—Springwater—Oro-Medonte." or "As Bhutila Karpoche". Omit stating your own name.

Never state things like: "(If no chat history provided)".

You should strive to not make conflicting statements and be consistent. For example, if your opposition says:
"Our opposition's suggestion to raise taxes would slow down economic development and hurt small businesses."

Do not say:
"My opposition suggests raising taxes to slow down economic development and hurt small businesses."

Instead say something like:
"My opposition states that I will raise taxes by an absurd amount. However, that is not my intention. Instead ..."

Remember to always be consistent with your statements.

Be less direct. For example, do not start by saying things like "I disagree with the notion that", ""Regarding the balanced budget amendment, I strongly believe", "I strongly disagree with the notion that". Instead, jump to the point and make your stance clear by letting your description of your policies and idea indicate your agreement or disagreement.

If a sentence has been said word for word already. DO NOT REPEAT IT. Do not mention ANY NAMES of PEOPLE in the conversation.
"""

USER_PROMPT = """
# Topic:
{topic}

## Chat History
{chat_history}

You are {agent_name}. Respond to your opposition's points. Make counters and highlight weaknesses in their arguments if possible. Do not be verbose. Keep your conversations concise and short. Focus on the highlights and most important ideas. If there is no chat history. State YOUR position. Make a succinct argument as to why you believe what you do. Remember to always be concise and short in your answer. Act in first person. Do not say things like "I'm Doug Downey, Attorney General for Barrie—Springwater—Oro-Medonte." or "As Bhutila Karpoche". Omit stating your own name.

Never state things like: "(If no chat history provided)".

You should strive to not make conflicting statements and be consistent. For example, if your opposition says:
"Our opposition's suggestion to raise taxes would slow down economic development and hurt small businesses."

Do not say:
"My opposition suggests raising taxes to slow down economic development and hurt small businesses."

Instead say something like:
"My opposition states that I will raise taxes by an absurd amount. However, that is not my intention. Instead ..."

Remember to always be consistent with your statements.

Be less direct. For example, do not start by saying things like "I disagree with the notion that", ""Regarding the balanced budget amendment, I strongly believe", "I strongly disagree with the notion that". Instead, jump to the point and make your stance clear by letting your description of your policies and idea indicate your agreement or disagreement.

If a sentence has been said word for word already. DO NOT REPEAT IT. Do not mention ANY NAMES of PEOPLE in the conversation.
"""

EVAL_SYSTEM_PROMPT = """You are a summarization assistant specializing in policy discussions. Your task is to read and analyze a conversation on a specific topic and provide a comprehensive, neutral summary. Focus on aggregating key points, themes, and highlights across all perspectives presented without favoring one side.

Ensure the summary is concise yet covers the following aspects:
1. Core Themes and Topics: Identify and explain the primary subjects discussed.
2. Key Points and Strategies: Outline the most important arguments and actionable suggestions mentioned.
3. Opportunities and Challenges: Highlight benefits, opportunities, and potential issues raised in the discussion.
4. Notable Highlights: Capture any standout ideas, solutions, or insights. Avoid mentioning specific perspectives or individuals.

Present the information as a cohesive and unified analysis of the discussion.

# Topic:
{topic}

# Conversation:
{chat_history}

Do not be verbose. Keep your conversations concise and short. Focus on the highlights and most important ideas. Make a succinct argument as to why you believe what you do.
Do not include names of the individuals in the chat history. Focus only on the topic at hand. DO NOT render in markdown at all. RENEDER ONLY AS A HTML element. Make titles bold using html bold tags like <b>. For example,

<b>Key Points in Summary</b>
"""


class ModelHandler:
    def __init__(self):
        self.model = "llama3.2"

    def summarize_agent_to_string(self, agent: dict):
        summary = f"Name: {agent['name'].title()}\n"
        summary += f"Party: {agent['party']}\n"
        summary += f"Location: {', '.join(agent['locations'])}\n"
        summary += f"Roles: {', '.join(agent['roles'])}\n\n"
        summary += "Bills:\n"
        for bill in agent["bills"]:
            summary += f"  - Title: {bill[0]}\n    Summary: {bill[1]}\n\n"
        summary += "Traits Summary:\n"
        for trait_category, traits in agent["traits"].items():
            summary += f"  {trait_category.replace('_', ' ').title()}:\n"
            for trait, value in traits.items():
                summary += f"    {trait.replace('_', ' ').title()}: {value}\n"
        summary += "\nPersona:\n"
        summary += agent["persona_long"]
        return summary

    def compile_history(self, history: list[dict[str, str]]):
        chat_history = ""
        for message in history:
            chat_history += f"{message['name']}:\n{message['text']}\n\n"

        return chat_history

    def split_response(self, response, max_chars=100):
        chunks = []
        current_chunk = ""

        # Iterate over sentences split by a period
        for sentence in response.split("."):
            sentence = sentence.strip()  # Remove extra spaces
            if not sentence:
                continue  # Skip empty sentences

            # Check if adding the sentence exceeds the max character limit
            if len(current_chunk) + len(sentence) + 1 <= max_chars:
                current_chunk += (". " if current_chunk else "") + sentence
            else:
                # Save the current chunk and start a new one
                chunks.append(current_chunk)
                current_chunk = sentence

        # Append any remaining chunk
        if current_chunk:
            chunks.append(current_chunk)

        return [chunk.strip() + "." for chunk in chunks]

    def generate(
        self, persona_dict: dict, history: list[dict[str, str]], topic: str
    ) -> dict[str, str] | list[dict]:
        name = persona_dict["name"]
        summary = self.summarize_agent_to_string(persona_dict)

        chat_history_string = self.compile_history(history)

        messages = [
            {"role": "system", "content": MODEL_SYSTEM_PROMPT.format(persona=summary)},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    topic=topic, chat_history=chat_history_string, agent_name=name
                ),
            },
        ]

        response = chat(model=self.model, messages=messages)
        response = response.message.content

        if not response:
            return {"name": name, "text": ""}

        chat_history = []

        responses = self.split_response(response, 250)

        for chunk in responses:
            chat_history.append({"name": name, "text": chunk})

        return chat_history

        # return {"name": name, "text": response}

    def evaluate(self, history: list[dict[str, str]], topic: str) -> str:
        chat_history_string = self.compile_history(history)

        prompt = EVAL_SYSTEM_PROMPT.format(
            topic=topic, chat_history=chat_history_string
        )

        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]

        response: ChatResponse = chat(model=self.model, messages=messages)

        if not response.message.content:
            return ""

        return response.message.content

    def llama_predict(self, prompt: str) -> str | None:
        from ollama import chat
        from ollama import ChatResponse

        response: ChatResponse = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response.message.content
