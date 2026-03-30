import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
# Ensure these function names match exactly what is in your services.py
from services import parse_docx_table, get_tag_from_llm

router = APIRouter()

# This variable will be populated by main.py during the startup lifespan
tag_db = None 

@router.post("/tag-fact")
async def tag_fact_endpoint(
    fact_query: str = Form(...), 
    file: UploadFile = File(...)
):
    """
    Endpoint to receive a fact and a Word document, 
    and return the matching Tag.
    """
    global tag_db
    
    # 1. Check if the database was actually initialized
    if tag_db is None:
        print("ERROR: tag_db is None. Check main.py startup logic.")
        raise HTTPException(
            status_code=500, 
            detail="Vector database not initialized. Check server logs."
        )

    try:
        # 2. Read the uploaded file
        print(f"--- Processing Request for Fact: {fact_query} ---")
        content = await file.read()
        
        # 3. Convert Word Table to Markdown
        table_md = parse_docx_table(content)
        
        if not table_md:
            print("ERROR: No table found in the uploaded .docx file.")
            raise HTTPException(
                status_code=400, 
                detail="No table found in the uploaded document."
            )
        
        print("Table successfully converted to Markdown.")

        # 4. Call the LLM service to get the tag
        # We pass the query, the table context, and the database instance
        result_tag = get_tag_from_llm(fact_query, table_md, tag_db)
        
        print(f"Success! Assigned Tag: {result_tag}")
        
        return {
            "status": "success",
            "fact": fact_query,
            "tag": result_tag
        }

    except Exception as e:
        # This catches errors like API Key issues or connection timeouts
        print(f"CRITICAL ERROR during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")