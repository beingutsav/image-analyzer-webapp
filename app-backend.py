from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from fastapi.responses import JSONResponse
from typing import List
import base64
import requests

app = FastAPI()

# OpenAI API Key
api_key = "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"

def encode_image_to_base64(file_content):
    return base64.b64encode(file_content).decode('utf-8')

def create_dynamic_request(image_paths, prompt):
    initial_content = {
        "type": "text",
        "text": prompt
    }

    content_array = [initial_content] + [
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encode_image_to_base64(path)}"}
        for path in image_paths
    ]

    final_payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": content_array
            }
        ],
        "max_tokens": 300
    }

    return final_payload

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

@app.post("/process-images/")
async def process_images(
    prompt: str = Query(..., title="Prompt", min_length=1),  # Adjust the validation as needed
    image_files: List[UploadFile] = File(...)
):
    image_contents = [await file.read() for file in image_files]

    request_payload = create_dynamic_request(image_contents, prompt)

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=request_payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="OpenAI API request failed")

    return JSONResponse(content=response.json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
