from dataclasses import dataclass

import asyncio
import aiohttp
from ratelimit import limits, sleep_and_retry
from typing import Dict, Any, Optional

from prompts import NO_SHOT_DEFAULT_PROMPT_LONG_FORM, NO_SHOT_DEFAULT_PROMPT_SHORT_FORM


API_CALLS_PER_MINUTE = 100
API_CALLS_TIME_PERIOD = 60


@dataclass
class MPP:
    name: str
    party: str
    role: str
    location: str

    def anonymous_repr(self) -> str:
        return f"A member of the {self.party} party, serving as the {self.role} in the Ontario Government."


@dataclass
class Bill:
    name: str
    details: str

    def __str__(self) -> str:
        return f"{self.name}: {self.details}"

@dataclass
class Motion:
    name: str
    motion_details: str
    
    def __str__(self) -> str:
        return self.motion_details


async def generate_llama_response(
    prompt: str,
    model: str = "llama3.1:70b",
    stream: bool = False,
    base_url: str = "http://127.0.0.1:11435"
) -> Dict[str, Any]:
    """
    Make a rate-limited async request to the Llama API.
    
    Args:
        prompt (str): The input prompt for the model
        model (str): Model identifier
        stream (bool): Whether to stream the response
        base_url (str): Base URL for the API
        
    Returns:
        Dict[str, Any]: API response as a dictionary
        
    Raises:
        aiohttp.ClientError: For HTTP-related errors
        asyncio.TimeoutError: If the request times out
        Exception: For other unexpected errors
    """
    url = f"{base_url}/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            ) as response:
                response.raise_for_status()
                return await response.json()
                
    except aiohttp.ClientError as e:
        print(f"HTTP error occurred: {e}")
        raise
    except asyncio.TimeoutError:
        print("Request timed out")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


async def generate_persona(mpps: list[MPP],
                           bills: list[list[Bill]], 
                           motions: list[list[Motion]]
                           ) -> str:
    return ""



async def main():

    example_MPP = MPP(name="peter bethlenfalvy", party="Progressive Conservative Party of Ontario", role="Minister of Finance", location="Pickering—Uxbridge")
    example_bill = Bill(name="Building Ontario For You Act (Budget Measures), 2024", details="Paragraph 4.0.1 of subsection 3 (1) of the Assessment Act sets out the conditions that must be satisfied for land leased and occupied solely by a university to be exempt from taxation under the Act. These include a condition that land must form part of the main campus of the university. This paragraph is amended to allow for land used to provide residential accommodation for students of the university to be exempt from taxation, even if the land does not form part of the main campus of the university.")
    example_motion = Motion(name="That this House approves in general the Budgetary Policy of the Government.", motion_details="That this House approves in general the Budgetary Policy of the Government.")
    
    example_bills = [example_bill]
    example_motions = [example_motion]

    example_bills = "\n".join([str(bill) for bill in example_bills])
    example_motions = "\n".join([str(motion) for motion in example_motions])
    
    print(NO_SHOT_DEFAULT_PROMPT_LONG_FORM.format(bills=example_bills, motions=example_motions, politician=example_MPP.anonymous_repr()))
    
    # requests = ["hello! :)"] * 10
    # try:
    #     results = await asyncio.gather(
    #         *[generate_llama_response(r) for r in requests],
    #         return_exceptions=True
    #     )
        
    #     # Process results
    #     for i, result in enumerate(results):
    #         if isinstance(result, Exception):
    #             print(f"Request {i} failed: {result}")
    #         else:
    #             print(f"Request {i} succeeded: {result}")
                
    # except Exception as e:
    #     print(f"Failed to process requests: {e}")


if __name__ == "__main__":
    asyncio.run(main())
