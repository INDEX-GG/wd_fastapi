from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import post as crud_post, user as user_crud
from app.schemas import post as post_schema, user as user_schema


router = APIRouter(prefix="/posts",
                   tags=["Posts"],
                   )


@router.get("", response_model=post_schema.Posts, tags=[], summary="Get posts page by page", description="")
async def get_posts_page_by_page(
        page: int = Query(default=1, ge=1, le=1000),
        page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
        price_from: int = Query(alias="priceFrom", default=None, ge=0, le=1000000000000),
        with_contract_price: bool = Query(alias="withContractPrice", default=None),
        search_string: str = Query(alias="searchString", default=None, min_length=1, max_length=200),
        sort: crud_post.SortValues = Query(default="default"),
        current_user_optional: user_schema.UserOut | None = Depends(user_crud.get_current_user_optional),
        db: Session = Depends(get_db)
):
    items = crud_post.get_posts_page_by_page(db=db,
                                             page=page,
                                             page_limit=page_limit,
                                             price_from=price_from,
                                             with_contract_price=with_contract_price,
                                             search_string=search_string,
                                             sort=sort,
                                             user=current_user_optional)

    return items


@router.get("/my", response_model=post_schema.Posts, tags=[], summary="Get user posts page by page", description="")
async def get_user_posts_page_by_page(
        page: int = Query(default=1, ge=1, le=1000),
        page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
        db: Session = Depends(get_db),
        current_user: user_schema.UserOut = Depends(user_crud.get_current_user)
):
    items = crud_post.get_user_posts_page_by_page(db=db,
                                                  page=page,
                                                  page_limit=page_limit,
                                                  user=current_user)

    return items
