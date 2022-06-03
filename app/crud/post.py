from sqlalchemy import or_, nullslast
from sqlalchemy.orm import Session
from enum import Enum
from app.db.db_models import Post
from app.schemas import post as post_schema


class SortValues(str, Enum):
    default = "default"
    new = "new"
    cheaper = "cheaper"
    expensive = "expensive"


def get_posts_page_by_page(db: Session,
                           page: int = 1,
                           page_limit: int = 60,
                           price_from: int = None,
                           with_contract_price: bool = None,
                           search_string: str = None,
                           sort: SortValues = "default"):
    offset = (page - 1) * page_limit
    query = db.query(Post)
    posts_count = None
    if price_from:
        if with_contract_price:
            query = query.filter(or_(Post.priceAmount >= price_from, Post.priceAmount == None))
        else:
            query = query.filter(Post.priceAmount >= price_from)
    if search_string:
        query = query.filter(Post.title.ilike("%" + search_string + "%"))
    match sort:
        case SortValues.default.name:
            query = query.order_by(Post.date.desc())
        case SortValues.new.name:
            query = query.order_by(Post.date.desc())
        case SortValues.cheaper.name:
            query = query.order_by(nullslast(Post.priceAmount.asc()))
        case SortValues.expensive.name:
            query = query.order_by(nullslast(Post.priceAmount.desc()))

    if page == 1:
        posts_count = query.count()
    posts = query.offset(offset).limit(page_limit).all()
    return post_schema.Posts(posts=posts, postsCount=posts_count)
