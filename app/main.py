from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.routers.api_router import api_router
from app.settings import settings

tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Language Model",
        "description": "API that takes either short or long text and provides a concise summary\n corrects grammar/spelling."
                       "\nExtracts key topics from a given text.\nClassifies text into predefined categories (e.g., news topics).",

    },
    {
        "name": "Threat Modelling AI Agent",
        "description": "mapping out the creation of a language model for risk analysis. "
                       "It might involve generating risk assessments, summarizing risk documents, or creating risk report templates.",

    },
]
app = FastAPI(title=settings.PROJECT_NAME, version=__version__,openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
