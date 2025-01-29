from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from db.models import ReviewHistory, Category
from utils.utils import analyze_review


def get_review_trends(db: Session, limit: int = 5):
    subquery = (
        db.query(
            ReviewHistory.review_id,
            func.max(ReviewHistory.created_at).label("max_created_at"),
        )
        .group_by(ReviewHistory.review_id)
        .subquery()
    )

    latest_reviews = (
        db.query(ReviewHistory)
        .join(
            subquery,
            (ReviewHistory.review_id == subquery.c.review_id) &
            (ReviewHistory.created_at == subquery.c.max_created_at),
        )
        .subquery()
    )

    # Query to calculate trends
    trends = (
        db.query(
            Category.id,
            Category.name,
            Category.description,
            func.count(latest_reviews.c.id).label("total_reviews"),
            func.avg(latest_reviews.c.stars).label("average_stars"),
        )
        .join(latest_reviews, Category.id == latest_reviews.c.category_id)
        .group_by(Category.id)
        .order_by(desc("average_stars"))
        .limit(limit)
        .all()
    )

    return [
        {
            "id": trend.id,
            "name": trend.name,
            "description": trend.description,
            "average_stars": float(trend.average_stars),
            "total_reviews": trend.total_reviews,
        }
        for trend in trends
    ]


def get_reviews_by_category(db: Session, category_id: int, cursor: int = None, page_size: int = 15):
    query = (
        db.query(ReviewHistory)
        .filter(ReviewHistory.category_id == category_id)
        .order_by(desc(ReviewHistory.created_at))
    )

    if cursor:
        query = query.filter(ReviewHistory.id < cursor)

    reviews = query.limit(page_size).all()

    for review in reviews:
        if review.tone is None or review.sentiment is None:
            analysis = analyze_review(review.text, review.stars)
            review.tone = analysis.get("tone")
            review.sentiment = analysis.get("sentiment")
            db.commit()

    return [
        {
            "id": review.id,
            "text": review.text,
            "stars": review.stars,
            "review_id": review.review_id,
            "created_at": review.created_at,
            "tone": review.tone,
            "sentiment": review.sentiment,
            "category_id": review.category_id,
        }
        for review in reviews
    ]
