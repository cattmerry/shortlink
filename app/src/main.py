from fastapi import FastAPI


from src.routers import short_link_router

app = FastAPI(
    title="Short_Link"
)

app.include_router(short_link_router.short_link_route)
