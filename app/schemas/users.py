from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    roles: Optional[list] = []
    # 猪场管理字段
    sow_number: Optional[str] = None
    ear_tag: Optional[str] = None
    pig_breed: Optional[str] = None
    backfat_thickness: Optional[float] = None
    parity: Optional[int] = None
    gestation_days: Optional[int] = None
    pen_number: Optional[str] = None
    feed_intake: Optional[float] = None
    feeder_number: Optional[str] = None
    predicted_feed: Optional[float] = None
    set_feed: Optional[float] = None
    actual_feed: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    set_feed_amount: Optional[float] = None
    current_feed_amount: Optional[float] = None
    last_feed_time: Optional[datetime] = None
    control_switch: Optional[bool] = None
    feeder_status: Optional[str] = None
    date: Optional[date] = None
    feeding_status: Optional[str] = None
    feeding_date: Optional[date] = None
    is_normal: Optional[bool] = None
    last_set_time: Optional[datetime] = None
    status: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr = Field(example="admin@qq.com")
    username: str = Field(example="admin")
    password: str = Field(example="123456")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    role_ids: Optional[List[int]] = []
    dept_id: Optional[int] = Field(0, description="部门ID")
    # 猪场管理字段
    sow_number: Optional[str] = None
    ear_tag: Optional[str] = None
    pig_breed: Optional[str] = None
    backfat_thickness: Optional[float] = None
    parity: Optional[int] = None
    gestation_days: Optional[int] = None
    pen_number: Optional[str] = None
    feed_intake: Optional[float] = None
    feeder_number: Optional[str] = None
    predicted_feed: Optional[float] = None
    set_feed: Optional[float] = None
    actual_feed: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    set_feed_amount: Optional[float] = None
    current_feed_amount: Optional[float] = None
    last_feed_time: Optional[datetime] = None
    control_switch: Optional[bool] = None
    feeder_status: Optional[str] = None
    date: Optional[date] = None
    feeding_status: Optional[str] = None
    feeding_date: Optional[date] = None
    is_normal: Optional[bool] = None
    last_set_time: Optional[datetime] = None
    status: Optional[str] = None

    def create_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"role_ids"})


class UserUpdate(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    role_ids: Optional[List[int]] = []
    dept_id: Optional[int] = 0
    # 猪场管理字段
    sow_number: Optional[str] = None
    ear_tag: Optional[str] = None
    pig_breed: Optional[str] = None
    backfat_thickness: Optional[float] = None
    parity: Optional[int] = None
    gestation_days: Optional[int] = None
    pen_number: Optional[str] = None
    feed_intake: Optional[float] = None
    feeder_number: Optional[str] = None
    predicted_feed: Optional[float] = None
    set_feed: Optional[float] = None
    actual_feed: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    set_feed_amount: Optional[float] = None
    current_feed_amount: Optional[float] = None
    last_feed_time: Optional[datetime] = None
    control_switch: Optional[bool] = None
    feeder_status: Optional[str] = None
    date: Optional[date] = None
    feeding_status: Optional[str] = None
    feeding_date: Optional[date] = None
    is_normal: Optional[bool] = None
    last_set_time: Optional[datetime] = None
    status: Optional[str] = None


class UpdatePassword(BaseModel):
    old_password: str = Field(description="旧密码")
    new_password: str = Field(description="新密码")
