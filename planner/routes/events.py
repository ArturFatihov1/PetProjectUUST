from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database.connection import get_session
from models.events import Event, EventUpdate

event_router = APIRouter(tags=["events"])


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(
    session: Session = Depends(get_session),
) -> List[Event]:
    return list(session.exec(select(Event)).all())


@event_router.get("/{event_id}", response_model=Event)
async def retrieve_event(
    event_id: int,
    session: Session = Depends(get_session),
) -> Event:
    event = session.get(Event, event_id)
    if event:
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(
    body: Event,
    session: Session = Depends(get_session),
) -> dict:
    body.id = None
    session.add(body)
    session.commit()
    session.refresh(body)
    return {"message": "Event created successfully"}


@event_router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: int,
    new_data: EventUpdate,
    session: Session = Depends(get_session),
) -> Event:
    event = session.get(Event, event_id)
    if event:
        event_data = new_data.model_dump(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.delete("/{event_id}")
async def delete_event(
    event_id: int,
    session: Session = Depends(get_session),
) -> dict:
    event = session.get(Event, event_id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.delete("/")
async def delete_all_events(
    session: Session = Depends(get_session),
) -> dict:
    events = session.exec(select(Event)).all()
    for event in events:
        session.delete(event)
    session.commit()
    return {"message": "Events deleted successfully"}
