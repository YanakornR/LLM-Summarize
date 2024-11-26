import ollama
from fastapi import FastAPI, HTTPException, Form

app = FastAPI()

# summarize function
def summarize_text(input_text, total_words):
    """
    Summarizes the given text using the specified Ollama model.
    
    Args:
        input_text (str): The text to summarize.
        model_name (str): The name of the Ollama model to use.
    
    Returns:
        str: The summary of the input text.
    """
    model_name = "llama3.2"
    prompt = f"Summarize the following text concisely and accurately in approximately {total_words} words. Provide only the summary, without any additional context, commentary, or introductory statements:\n\n{input_text}"
    try:
        messages = [{'role': 'user', 'content': prompt}]
        response = ollama.chat(model=model_name, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"An error occurred: {e}"

# api endpoint
@app.post("/summarize/")
async def summarize(
        text: str = Form(...),
        total_words: int = Form(...),
    ):
    """
    API endpoint to summarize a given text using Ollama.
    """
    try:
        summary = summarize_text(text, total_words)
        if summary.startswith("An error occurred"):
            raise HTTPException(status_code=500, detail=summary)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



