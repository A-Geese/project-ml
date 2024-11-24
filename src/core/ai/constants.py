## Generic
POLTICIAN_TEMPLATE = """**Name:** {name}
**Roles:**
{roles}
**Location:** {location}
**Political Party:** {party}

### Supports the following bills:
{bills}
"""


## Long Form Personas
NO_SHOT_DEFAULT_PROMPT_LONG_FORM = """
## Politician:
{politician}

## Bills: 
{bills}

## Motions
{motions}

Based on the above bills and motions brought forth by a politician, write a couple sentences maximum \
to describe the personality and backstory of the politician. Only return the persona of the politician and do not mention any names -- that is, keep the persona generic."""

## Skill-assessment personas
SYSTEM_PROMPT = """You are an evaluator designed to assess how well a person aligns with predefined characteristics. For each characteristic, assign a score from 0 to 10, based on the description of the person's behavior, actions, or traits provided in the input.

Scoring Criteria:
- 10 (Excellent): The person completely embodies this characteristic, consistently demonstrating it in actions and decisions.
- 8-9 (Strong): The person aligns with this characteristic most of the time, with only minor exceptions.
- 6-7 (Moderate): The person somewhat aligns with this characteristic, but there are noticeable gaps or inconsistencies.
- 4-5 (Weak): The person rarely aligns with this characteristic, with significant room for improvement.
- 1-3 (Poor): The person exhibits minimal alignment with this characteristic, with major shortcomings.
- 0 (Not Assessable): Not sufficient information to assess.

Score the Persona for each characteristic. You MUST provide a score and ONLY return an integer from 0 to 10. If the input does not mention relevant behaviors for a characteristic, infer reasonably or return 0 to indicate not sufficient information to assess. The output MUST be an integer.

Remember:
- Do not include any explanations or additional text.
- Each value must be an integer from 0 to 10.
"""

USER_PROMPT = """Persona:
{persona}

Score the Persona.

Remember:
- Do not include any explanations or additional text.
- Each value must be an integer from 0 to 10.
"""
