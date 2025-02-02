from fastapi import APIRouter, Depends, status, Query
from typing import Any, List, Optional, Union
from app.services.user import CurrentUserDep
from app.db import SessionDep
from app.schemas.text_language import TextRequest
from app.services.openai import OpenAIService

router = APIRouter(tags=["Language Model"], prefix="/model")
openAIService = OpenAIService()

@router.post("/suggest_grammar_correction", status_code=status.HTTP_200_OK)
async def suggest_grammar_correction(
    grammar_text: TextRequest,
        current_user: CurrentUserDep
):
    return await openAIService.suggest_grammar_correction(grammar_text.text)

@router.post("/suggest_summarization", status_code=status.HTTP_200_OK)
async def suggest_summarization(
    grammar_text: TextRequest,
    current_user: CurrentUserDep
):
    return await openAIService.suggest_summarization(grammar_text.text)

@router.post("/suggest_keyword_extraction", status_code=status.HTTP_200_OK)
async def suggest_keyword_extraction(
    grammar_text: TextRequest,
        current_user: CurrentUserDep
):
    return await openAIService.suggest_keyword_extraction(grammar_text.text)

@router.post("/suggest_text_categorization", status_code=status.HTTP_200_OK)
async def suggest_text_categorization(
        current_user: CurrentUserDep,
    grammar_text: TextRequest,
    category: Union[List[str], None] = Query(None, description="A single category or a list of categories"),
):
    return await openAIService.suggest_text_categorization(grammar_text.text, category)

@router.post("/suggest_sentiment_analysis", status_code=status.HTTP_200_OK)
async def suggest_sentiment_analysis(
    grammar_text: TextRequest,
        current_user: CurrentUserDep

):
    return await openAIService.suggest_sentiment_analysis(grammar_text.text)



