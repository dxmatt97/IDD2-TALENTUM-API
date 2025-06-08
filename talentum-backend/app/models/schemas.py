from pydantic import BaseModel

class SeniorityUpdate(BaseModel):
    seniority: str

class Action(BaseModel):
    action_name: str

class ActionResponse(BaseModel):
    message: str
    session_data: dict
