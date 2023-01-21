from fastapi import FastAPI

from database import Base, engine

from auth.routing import router as auth_routing
from dweets.routing import router as dweets_routing
from profiles.routing import router as profiles_routing


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routing)
app.include_router(dweets_routing)
app.include_router(profiles_routing)
