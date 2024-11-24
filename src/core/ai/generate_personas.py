import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict

import aiohttp
import pandas as pd
import requests
from constants import NO_SHOT_DEFAULT_PROMPT_LONG_FORM, POLTICIAN_TEMPLATE
from ratelimit import limits, sleep_and_retry

API_CALLS_PER_MINUTE = 10
API_CALLS_TIME_PERIOD = 15


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
        mpp = MPP(
            _id=i,
            name=mpp_df["name"][i],
            party=mpp_df["party"][i],
            role=mpp_df["role"][i],
            location=mpp_df["location"][i],
        )
        mpps.append(mpp)
    return mpps


def get_mpp_bills(_id: int, bills_df: pd.DataFrame) -> list[Bill]:
    bill_df = bills_df[
        (bills_df["mpp_id"] == _id) & (bills_df["explanatory_notes"] != "")
    ].reset_index(drop=True)
    bills = []
    for i in range(len(bill_df)):
        if type(bill_df["explanatory_notes"][i]) != str:
            continue
        bill = Bill(
            name=bill_df["bill_name"][i], details=bill_df["explanatory_notes"][i]
        )
        bills.append(bill)
    return bills


def get_mpp_motions(_id: int, motions_df: pd.DataFrame) -> list[Motion]:
    motion_df = motions_df[
        (motions_df["mpp_id"] == _id) & (motions_df["motion_details"] != None)
    ].reset_index(drop=True)
    motions = []
    for i in range(len(motion_df)):
        if type(motion_df["motion_details"][i]) != str:
            continue
        motion = Motion(
            name=motion_df["motion_name"][i],
            motion_details=motion_df["motion_details"][i],
        )
        motions.append(motion)
    return motions


def format_prompt_lf(mpp: MPP, bills: list[Bill], motions: list[Motion]) -> str:
    bills_str = "\n".join([str(bill) for bill in bills])
    motions_str = "\n".join([str(motion) for motion in motions])
    return NO_SHOT_DEFAULT_PROMPT_LONG_FORM.format(
        bills=bills_str, motions=motions_str, politician=mpp.anonymous_repr()
    )


def format_prompt_skills(mpp: MPP, bills: list[Bill], motions: list[Motion]) -> str:
    if len(bills) == 0:
        bills_str = "None"
    else:
        bills_str = "\n".join([bill.details for bill in bills])
    if len(motions) == 0:
        motions_str = "None"
    else:
        motions_str = "\n".join([motion.motion_details for motion in motions])
    return POLTICIAN_TEMPLATE.format(
        name=mpp.name,
        roles=mpp.role,
        location=mpp.location,
        party=mpp.party,
        bills=bills_str,
        motions=motions_str,
    )


@sleep_and_retry
@limits(calls=API_CALLS_PER_MINUTE, period=API_CALLS_TIME_PERIOD)
async def generate_llama_response(
    prompt: str,
    model: str = "llama3.1:70b",
    stream: bool = False,
    base_url: str = "http://127.0.0.1:11435",
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
    data = {"model": model, "prompt": prompt, "stream": stream}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, json=data, timeout=30
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


def generate_llama_response(
    prompt: str,
    model: str = "llama3.1:70b",
    stream: bool = False,
    base_url: str = "http://127.0.0.1:11435",
) -> Dict[str, Any]:
    """
    Make a request to the Llama API.

    Args:
        prompt (str): The input prompt for the model
        model (str): Model identifier
        stream (bool): Whether to stream the response
        base_url (str): Base URL for the API

    Returns:
        Dict[str, Any]: API response as a dictionary

    Raises:
        requests.RequestException: For HTTP-related errors
        requests.Timeout: If the request times out
        Exception: For other unexpected errors
    """
    url = f"{base_url}/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": model, "prompt": prompt, "stream": stream}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()

    except requests.Timeout:
        print("Request timed out")
        raise
    except requests.RequestException as e:
        print(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


# def get_persona_traits(persona_prompt: str) -> dict:
#     client = instructor.from_openai(
#         OpenAI(
#             base_url="http://localhost:11434/v1",
#             api_key="ollama",
#         ),
#         mode=instructor.Mode.JSON,
#     )

#     persona_traits = {}
#     for field_name, field in Characteristics.model_fields.items():
#         while True:
#             try:
#                 print([
#                         {"role": "system", "content": SYSTEM_PROMPT},
#                         {
#                             "role": "user",
#                             "content": USER_PROMPT.format(persona=persona_prompt),
#                         },
#                     ]   )
#                 response = client.chat.completions.create(
#                     model="llama3.2",
#                     messages=[
#                         {"role": "system", "content": SYSTEM_PROMPT},
#                         {
#                             "role": "user",
#                             "content": USER_PROMPT.format(persona=persona_prompt),
#                         },
#                     ],
#                     response_model=field.annotation,
#                 )
#             except Exception:
#                 print(f"Retrying structured outputs on: {field.annotation}")
#                 continue

#             persona_traits[field_name] = response.model_dump()
#             break

#     return persona_traits


async def main():
    mpp_df = pd.read_csv("data/mpps.csv")
    bills_df = pd.read_csv("data/bills.csv")
    motions_df = pd.read_csv("data/motions.csv")

    mpps = load_mpps(mpp_df)
    lf_prompts = []
    skill_prompts = []
    mpp_ids = []
    ## Parse out prompts to generate personas for each mpp
    for mpp in mpps:
        mpp_id = mpp._id
        bills = get_mpp_bills(mpp._id, bills_df)
        motions = get_mpp_motions(mpp._id, motions_df)
        if not bills and not motions:
            continue
        prompt_lf = format_prompt_lf(mpp, bills, motions)
        prompt_skill = format_prompt_skills(mpp, bills, motions)
        skill_prompts.append(prompt_skill)

        lf_prompts.append(prompt_lf)
        mpp_ids.append(mpp_id)

    # Generate personas (long form)
    results = [generate_llama_response(p) for p in lf_prompts]
    personas_lf = []
    for result in results:
        personas_lf.append(result["response"])
    # try:
    #     results = await asyncio.gather(
    #         *[generate_llama_response(p) for p in lf_prompts],
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
    #     results = ""

    # personas_lf = []
    # for result in results:
    #     if isinstance(result, Exception):
    #         personas_lf.append("")
    #     else:
    #         personas_lf.append(result['response'])

    # save as json
    with open("personas_lf.json", "w") as f:
        f.write(json.dumps({"mpp_id": mpp_ids, "persona": personas_lf}))
    # personas_df = pd.DataFrame({"mpp_id": mpp_ids, "persona": results})
    # personas_df = personas_df[personas_df["persona"] != ""].reset_index(drop=True)

    # skill_results = [get_persona_traits(prompt) for prompt in skill_prompts]
    # personas_df2 = pd.DataFrame({"mpp_id": mpp_ids, "persona": skill_results})
    # personas_df2 = personas_df2[personas_df2["persona"] != ""].reset_index(drop=True)

    # personas_df = pd.merge(personas_df, personas_df2, on="mpp_id", how="inner")
    # personas_df = pd.DataFrame({"mpp_id": mpp_ids, "persona_lf": personas_lf, 'persona_skills': skill_results})
    # personas_df = personas_df[personas_df["persona"] != ""].reset_index(drop=True)
    # personas_df.to_csv("p1_personas.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())
