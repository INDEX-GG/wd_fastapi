import datetime
from sqlalchemy import or_, nullslast, and_
from sqlalchemy.orm import Session
from enum import Enum
from app.db.db_models import Post, Vacancy, Favorites
from app.schemas import post as post_schema, user as user_schema


class SortValues(str, Enum):
    default = "default"
    new = "new"
    cheaper = "cheaper"
    expensive = "expensive"


def get_posts_page_by_page(db: Session,
                           user: user_schema.UserOut,
                           page: int = 1,
                           page_limit: int = 60,
                           price_from: int = None,
                           with_contract_price: bool = None,
                           search_string: str = None,
                           sort: SortValues = "default"):
    offset = (page - 1) * page_limit

    if user:
        query = db.query(Post, Favorites.id)
        query = query.outerjoin(Favorites, and_(Favorites.objId == Post.id, Favorites.userId == user.id))
    else:
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
            query = query.order_by(Post.date.desc(), nullslast(Post.priority.desc()), Post.random)
        case SortValues.new.name:
            query = query.order_by(Post.date.desc())
        case SortValues.cheaper.name:
            query = query.order_by(nullslast(Post.priceAmount.asc()))
        case SortValues.expensive.name:
            query = query.order_by(nullslast(Post.priceAmount.desc()))

    if page == 1:
        posts_count = query.count()
    posts = query.offset(offset).limit(page_limit).all()

    if user:
        answer = []
        for post in posts:
            like = bool(post[1])
            post = post[0]
            post.inFavorite = like
            answer.append(post)
        return post_schema.Posts(posts=answer, posts_count=posts_count)

    return post_schema.Posts(posts=posts, postsCount=posts_count)


def create_post(db: Session,  vacancy: Vacancy):
    currency = None
    if vacancy.budget:
        currency = "rub"
    db_post = Post(title=vacancy.title,
                   link="https://workdirect.ru/vacancies/{}".format(vacancy.id),
                   description=vacancy.description,
                   priceAmount=vacancy.budget,
                   priceCurrency=currency,
                   date=datetime.datetime.utcnow(),
                   source="https://workdirect.ru/",
                   priority=5)
    db.add(db_post)
    db.commit()
