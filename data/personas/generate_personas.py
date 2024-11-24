from dataclasses import dataclass
import asyncio
import aiohttp
from ratelimit import limits, sleep_and_retry
from typing import Dict, Any, Optional
from prompts import NO_SHOT_DEFAULT_PROMPT_LONG_FORM, NO_SHOT_DEFAULT_PROMPT_SHORT_FORM
import pandas as pd


API_CALLS_PER_MINUTE = 100
API_CALLS_TIME_PERIOD = 60


@dataclass
class MPP:
    _id: int
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
        

def load_mpps(mpp_df: pd.DataFrame) -> list[MPP]:
    mpps = []
    for i in range(len(mpp_df)):
        mpp = MPP(_id=i, name=mpp_df["name"][i], party=mpp_df["party"][i], role=mpp_df["role"][i], location=mpp_df["location"][i])
        mpps.append(mpp)
    return mpps


def get_mpp_bills(_id: int, bills_df: pd.DataFrame) -> list[Bill]:
    bill_df = bills_df[(bills_df["mpp_id"] == _id) & (bills_df["explanatory_notes"] != "")].reset_index(drop=True)
    bills = []
    for i in range(len(bill_df)):
        bill = Bill(name=bill_df["bill_name"][i], details=bill_df["explanatory_notes"][i])
        bills.append(bill)
    return bills


def get_mpp_motions(_id: int, motions_df: pd.DataFrame) -> list[Motion]:
    motion_df = motions_df[(motions_df["mpp_id"] == _id) & (motions_df["motion_details"] != None)].reset_index(drop=True)
    motions = []
    for i in range(len(motion_df)):
        if type(motion_df["motion_details"][i]) != str:
            continue
        motion = Motion(name=motion_df["motion_name"][i], motion_details=motion_df["motion_details"][i])
        motions.append(motion)
    return motions


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


def format_prompt(mpp: MPP, bills: list[Bill], motions: list[Motion]) -> str:
    bills_str = "\n".join([str(bill) for bill in bills])
    motions_str = "\n".join([str(motion) for motion in motions])
    return NO_SHOT_DEFAULT_PROMPT_LONG_FORM.format(bills=bills_str, motions=motions_str, politician=mpp.anonymous_repr())


async def main():
    mpp_df = pd.read_csv("data/mpps.csv")
    bills_df = pd.read_csv("data/bills.csv")
    motions_df = pd.read_csv("data/motions.csv")

    mpps = load_mpps(mpp_df)
    prompts = []
    mpp_ids = []
    for mpp in mpps[:20]:
        mpp_id = mpp._id
        bills = get_mpp_bills(mpp._id, bills_df)
        motions = get_mpp_motions(mpp._id, motions_df)
        if not bills and not motions:
            continue
        prompt = format_prompt(mpp, bills, motions)
        prompts.append(prompt)
        mpp_ids.append(mpp_id)

    # Generate personas
    try:
        results = await asyncio.gather(
            *[generate_llama_response(p) for p in prompts],
            return_exceptions=True
        )
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Request {i} failed: {result}")
            else:
                print(f"Request {i} succeeded: {result}")
    except Exception as e:
        print(f"Failed to process requests: {e}")
        results = ""

    print(results)
    personas = []
    for result in results:
        if isinstance(result, Exception):
            personas.append("")
        else:
            personas.append(result['response'])

    personas_df = pd.DataFrame({"mpp_id": mpp_ids, "persona": personas})
    personas_df = personas_df[personas_df["persona"] != ""].reset_index(drop=True)
    personas_df.to_csv("data/personas.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())
