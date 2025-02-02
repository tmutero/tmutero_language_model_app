from fastapi import APIRouter, Depends, status, Query
from typing import Any, List, Optional, Union
from app.db import SessionDep
from app.schemas.text_language import TextRequest
from app.services.openai import OpenAIService
from app.services.user import CurrentUserDep

router = APIRouter(tags=["Threat Modelling AI Agent"], prefix="/threat-modelling")
adviserAIagent = OpenAIService()


@router.post("/assess_application", status_code=status.HTTP_200_OK,)
async def assess_application(
    grammar_text: TextRequest,
    current_user: CurrentUserDep
):
    return await adviserAIagent.assess_application(grammar_text.text)

@router.post("/explain_vulnerability", status_code=status.HTTP_200_OK)
async def explain_vulnerability(
    grammar_text: TextRequest,
    current_user: CurrentUserDep,

):
    return await adviserAIagent.explain_vulnerability(grammar_text.text)

@router.post("/suggest_mitigations", status_code=status.HTTP_200_OK)
async def suggest_mitigations(
    grammar_text: TextRequest,
    current_user: CurrentUserDep
):
    return await adviserAIagent.suggest_mitigations(grammar_text.text)
