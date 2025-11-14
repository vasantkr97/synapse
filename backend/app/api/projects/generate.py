from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from app.libs.prompts.system_prompt import system_prompt
from app.agent.llm import gemini_llm
from app.core.dependencies import get_authenticated_user
from app.models import User, ConversationHistory
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
import 

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    
@router.post("/api/generate")
async def generateProject( 
    prompt: GenerateRequest,
    currentUser: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    
    try: 
        if not prompt:
            return JSONResponse({"error": "prompt not givn"}, status_code=400)
        
        new_chat = ConversationHistory(
            id=chat_id,
            user_id=currentUser.id
        )
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt.replace("{", "{{").replace("}", "}}")),
            ("user", "{prompt}")
        ])

        chain = prompt_template | gemini_llm

        result = await chain.ainvoke({'prompt': prompt})

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



