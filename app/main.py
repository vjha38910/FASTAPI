from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.vote import vote
from app.schemas import Vote

from.import models
from.database import engine
from .routers import post, user, auth, vote
from .config import settings

from app import database



#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#my_posts= [{"title":"title of post ", "content":"post content","id":1},{"title":"food", "content":"dosa","id":2}]
  
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

app.include_router(vote.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)









