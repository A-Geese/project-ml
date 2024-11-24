PERSONA_CHARACTERISTICS = [
    "Curious and Analytical",
    "Goal-Oriented",
    "Adaptable Learner",
    "Perfectionist with Practicality",
    "Innovative and Strategic",
    "Structured Planner",
    "Team-Oriented",
    "Continuous Improver",
    "Efficiency-Driven",
    "Tech-Savvy",
    "Detail-Oriented Developer",
    "Full-Stack Perspective",
    "DevOps Mindset",
    "Innovator",
    "Explorer",
    "Mentor and Collaborator",
    "Visionary"
]
# expects that the MPP has at least one bill or motion
NO_SHOT_DEFAULT_PROMPT_LONG_FORM = """
## Politician Background:
{politician}

## Bills: 
{bills}

## Motions
{motions}

Based on the above bills and motions brought forth by a politician, write a couple sentences maximum \
to describe the personality and backstory of the politician. Only return the persona of the politician."""

NO_SHOT_DEFAULT_PROMPT_SHORT_FORM = """Bills: {bills}
Motions: {motions}

Characteristics: {characteristics}
Based on the above bills and motions brought forth by a politician, describe the politician in no more\
than three of the above persona characteristics."""

NO_SHOT_PROMPT_NO_MOTIONS = ...
NO_SHOT_PROMPT_NO_BILLS = ...
