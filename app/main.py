from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, votes
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/") # / this is path and can be modified but if modified we have to add that in our URl
def root(): # async word is used only when we want to do async work which can be optional and function name here can be anything
    return {"message": "Hello World"} # we change our message but to change it in our website we have to quit and restart
#unicorn but an alternative way is to use uvicorn man:app --reload adding reload automatically does this for us





