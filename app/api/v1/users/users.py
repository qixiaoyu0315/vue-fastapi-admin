import logging

from fastapi import APIRouter, Body, Query
from tortoise.expressions import Q

from app.controllers.dept import dept_controller
from app.controllers.user import user_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.users import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看用户列表")
async def list_user(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    username: str = Query("", description="用户名称，用于搜索"),
    email: str = Query("", description="邮箱地址"),
    dept_id: int = Query(None, description="部门ID"),
    # 猪场管理相关字段
    sow_number: str = Query("", description="母猪号"),
    ear_tag: str = Query("", description="电子耳标号"),
    pen_number: str = Query("", description="栏号"),
    feeder_number: str = Query("", description="下料器号"),
    pig_breed: str = Query("", description="猪种"),
    feeding_status: str = Query("", description="采食状态"),
    feeder_status: str = Query("", description="下料器状态"),
):
    q = Q()
    if username:
        q &= Q(username__contains=username)
    if email:
        q &= Q(email__contains=email)
    if dept_id is not None:
        q &= Q(dept_id=dept_id)
    # 添加猪场管理相关字段的搜索条件
    if sow_number:
        q &= Q(sow_number__contains=sow_number)
    if ear_tag:
        q &= Q(ear_tag__contains=ear_tag)
    if pen_number:
        q &= Q(pen_number__contains=pen_number)
    if feeder_number:
        q &= Q(feeder_number__contains=feeder_number)
    if pig_breed:
        q &= Q(pig_breed__contains=pig_breed)
    if feeding_status:
        q &= Q(feeding_status__contains=feeding_status)
    if feeder_status:
        q &= Q(feeder_status__contains=feeder_status)
    
    total, user_objs = await user_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict(m2m=True, exclude_fields=["password"]) for obj in user_objs]
    for item in data:
        dept_id = item.pop("dept_id", None)
        item["dept"] = await (await dept_controller.get(id=dept_id)).to_dict() if dept_id else {}

    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看用户")
async def get_user(
    user_id: int = Query(..., description="用户ID"),
):
    user_obj = await user_controller.get(id=user_id)
    user_dict = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=user_dict)


@router.post("/create", summary="创建用户")
async def create_user(
    user_in: UserCreate,
):
    user = await user_controller.get_by_email(user_in.email)
    if user:
        return Fail(code=400, msg="The user with this email already exists in the system.")
    new_user = await user_controller.create_user(obj_in=user_in)
    await user_controller.update_roles(new_user, user_in.role_ids)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新用户")
async def update_user(
    user_in: UserUpdate,
):
    user = await user_controller.update(id=user_in.id, obj_in=user_in)
    await user_controller.update_roles(user, user_in.role_ids)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除用户")
async def delete_user(
    user_id: int = Query(..., description="用户ID"),
):
    await user_controller.remove(id=user_id)
    return Success(msg="Deleted Successfully")


@router.post("/reset_password", summary="重置密码")
async def reset_password(user_id: int = Body(..., description="用户ID", embed=True)):
    await user_controller.reset_password(user_id)
    return Success(msg="密码已重置为123456")
