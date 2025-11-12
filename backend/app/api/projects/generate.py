from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from app.libs.prompts.system_prompt import system_prompt
from app.agent.llm import openAI_llm

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    history: Optional[List[str]] = None

@router.post("/api/generate")
async def generate_code(req: GenerateRequest):
    try: 
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt.replace("{", "{{").replace("}", "}}")),
            ("user", "{prompt}")
        ])

        chain = prompt_template | openAI_llm

        result = await chain.invoke({'prompt': req.prompt})

        return JSONResponse(
            content={
                "success": True,
                "output": result.content.strip()
            }
        )
    
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(exc)
        )



