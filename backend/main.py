
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# ✅ Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "FastAPI backend is running!"}


@app.post("/api/save-payload")
async def save_payload(request: Request):
    try:
        payload = await request.json()

        # Validate userId
        if not payload.get("userId"):
            raise HTTPException(
                status_code=400, detail="Invalid payload: missing userId")

        # Directory to save JSON files
        dir_path = os.path.join(os.getcwd(), "saved_payloads")
        os.makedirs(dir_path, exist_ok=True)

        # ✅ Correct f-string here
        file_path = os.path.join(dir_path, f"enrollment_payload_{payload['userId']}.json")

        # Save the file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        print(f"✅ Saved payload to: {file_path}")

        return JSONResponse(
            content={"message": "Saved successfully", "filePath": file_path},
            status_code=200
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Error saving payload: {e}")
        return JSONResponse(
            content={"message": "Server error", "error": str(e)},
            status_code=500
        )


@app.get("/api/test")
async def test():
    return {"message": "API working fine"}
