from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Talentum+"}
