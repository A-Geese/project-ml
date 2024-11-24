from pydantic import BaseModel


class CognitiveSkills(BaseModel):
    curious_and_analytical: int
    creative_problem_solver: int
    independent_thinker: int
    innovative_and_forward_thinking: int


class GoalManagement(BaseModel):
    goal_oriented: int
    self_disciplined: int
    pragmatic_decision_maker: int
    time_conscious: int


class LearningAdaptability(BaseModel):
    adaptable_learner: int
    open_minded: int
    resilient_in_challenging_situations: int


class InterpersonalSkills(BaseModel):
    empathetic_and_supportive: int
    collaborative_team_player: int
    strong_communicator: int


class AttentionToDetail(BaseModel):
    detail_oriented: int
    perfectionist_with_practicality: int


class SelfReflection(BaseModel):
    reflective_and_self_aware: int


class Characteristics(BaseModel):
    cognitive_skills: CognitiveSkills
    goal_management: GoalManagement
    learning_adaptability: LearningAdaptability
    interpersonal_skills: InterpersonalSkills
    attention_to_detail: AttentionToDetail
    self_reflection: SelfReflection
