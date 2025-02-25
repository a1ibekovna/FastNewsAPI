"""
Comments API module
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import User, fastapi_users
from src import get_db
from ..models import Comment
from ..schemas import CommentReadSchema, CommentCreateSchema
from ..services import CommentService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.get("/{news_id}", response_model=List[CommentReadSchema])
async def get_comments(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
) -> List[Comment]:
    """
    Get a list of comments for a specific news article.
    """
    return await CommentService.get_comments(db=db, news_id=news_id, offset=offset, limit=limit)


@router.get("/{comment_id}", response_model=CommentReadSchema)
async def get_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
) -> Comment:
    """
    Retrieve a single comment by ID.
    """
    return await CommentService.get_comment(db=db, comment_id=comment_id)


@router.post("", response_model=CommentReadSchema)
async def create_comment(
    comment: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> Comment:
    """
    Create a new comment.
    """
    comment_data = comment.dict()
    return await CommentService.create_comment(db=db, comment_data=comment_data, user=current_user)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> dict:
    """
    Delete a comment if the user is the owner.
    """
    await CommentService.delete_comment(db=db, comment_id=comment_id, user=current_user)
    return {"detail": "Comment deleted"}


@router.put("/{comment_id}", response_model=CommentReadSchema)
async def update_comment(
    comment_id: int,
    comment: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> Comment:
    """
    Fully update a comment.
    """
    comment_data = comment.dict()
    return await CommentService.update_comment(db=db, comment_id=comment_id, comment_data=comment_data, user=current_user)


@router.patch("/{comment_id}", response_model=CommentReadSchema)
async def partial_update_comment(
    comment_id: int,
    comment: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> Comment:
    """
    Partially update a comment.
    """
    comment_data = comment.dict()
    return await CommentService.partial_update_comment(db=db, comment_id=comment_id, comment_data=comment_data, user=current_user)
