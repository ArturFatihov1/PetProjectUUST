from typing import List

from fastapi import APIRouter, Body, HTTPException, status

from models.events import Event

event_router = APIRouter(tags=["events"])
events: List[Event] = []  # "база данных" в памяти


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


@event_router.get("/{event_id}", response_model=Event)
async def retrieve_event(event_id: int) -> Event:
    for event in events:
        if event.id == event_id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event = Body(...)) -> dict:
    if any(e.id == body.id for e in events):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event with supplied ID already exists",
        )
    events.append(body)
    return {"message": "Event created successfully"}


@event_router.delete("/{event_id}")
async def delete_event(event_id: int) -> dict:
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Events deleted successfully"}
