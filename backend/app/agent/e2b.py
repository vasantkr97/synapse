from e2b_code_interpreter import AsyncSandbox

async def run_code_in_sandbox(code: str) -> str:
    #create sandbox asynchronously
    sandbox = await AsyncSandbox.create()

    try: 
        execution = await sandbox.run_code(code)

        result = execution.logs or execution.text or ""

        return result.strip()
    
    finally: 
        
        await sandbox.close()