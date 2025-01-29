from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.review_service import get_review_trends, get_reviews_by_category
from tasks.log_access import log_access
from typing import Optional

router = APIRouter()


@router.get("/reviews/trends")
def fetch_review_trends(db: Session = Depends(get_db)):
    trends = get_review_trends(db)
    log_access.delay("GET /reviews/trends")

    return trends


@router.get("/reviews/")
def fetch_reviews_by_category(
    category_id: int,
    cursor: Optional[int] = None,
    db: Session = Depends(get_db),
):
    reviews = get_reviews_by_category(db, category_id, cursor)

    log_access.delay(f"GET /reviews/?category_id={category_id}")

    return reviews
