from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key, instructions="", model="gpt-3.5-turbo", temperature=1.0, top_p=1.0, frequency_penalty=0, presence_penalty=0, max_output_tokens=3000, previous_response_id=None):
        self.__api_key = api_key
        self.instructions = instructions
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.max_output_tokens = max_output_tokens
        self.previous_response_id = previous_response_id
        self.__client = OpenAI(
            api_key=self.__api_key
        )

    def generate_response(self, prompt, text=None, instructions = None, previous_response_id=None):
        response = self.__client.responses.create(
            model=self.model,
            instructions= instructions or self.instructions,
            input=prompt,
            temperature=self.temperature,
            top_p=self.top_p,
            text=text,
            # frequency_penalty=frequency_penalty or self.frequency_penalty, not available in responses API?
            # presence_penalty=presence_penalty or self.presence_penalty, not available in responses API?
            max_output_tokens=self.max_output_tokens,
            previous_response_id=previous_response_id
        )
        return response
