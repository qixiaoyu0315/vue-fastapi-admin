from tortoise import fields

from app.schemas.menus import MenuType

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class User(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=20, unique=True, description="用户名称", index=True)
    alias = fields.CharField(max_length=30, null=True, description="姓名", index=True)
    email = fields.CharField(max_length=255, unique=True, description="邮箱", index=True)
    phone = fields.CharField(max_length=20, null=True, description="电话", index=True)
    password = fields.CharField(max_length=128, null=True, description="密码")
    is_active = fields.BooleanField(default=True, description="是否激活", index=True)
    is_superuser = fields.BooleanField(default=False, description="是否为超级管理员", index=True)
    last_login = fields.DatetimeField(null=True, description="最后登录时间", index=True)
    roles = fields.ManyToManyField("models.Role", related_name="user_roles")
    dept_id = fields.IntField(null=True, description="部门ID", index=True)
    
    # 猪场管理相关字段
    sow_number = fields.CharField(max_length=50, null=True, description="母猪号")
    ear_tag = fields.CharField(max_length=50, null=True, description="电子耳标号")
    pig_breed = fields.CharField(max_length=50, null=True, description="猪种")
    backfat_thickness = fields.FloatField(null=True, description="背膘厚度")
    parity = fields.IntField(null=True, description="胎次")
    gestation_days = fields.IntField(null=True, description="妊娠天数")
    pen_number = fields.CharField(max_length=50, null=True, description="栏号")
    feed_intake = fields.FloatField(null=True, description="采食量")
    feeder_number = fields.CharField(max_length=50, null=True, description="下料器号")
    predicted_feed = fields.FloatField(null=True, description="预测采食量")
    set_feed = fields.FloatField(null=True, description="设置采食量")
    actual_feed = fields.FloatField(null=True, description="实际采食量")
    start_time = fields.DatetimeField(null=True, description="开始时间")
    end_time = fields.DatetimeField(null=True, description="结束时间")
    set_feed_amount = fields.FloatField(null=True, description="设置饲料量")
    current_feed_amount = fields.FloatField(null=True, description="当前饲料量")
    last_feed_time = fields.DatetimeField(null=True, description="上次下料时间")
    control_switch = fields.BooleanField(null=True, description="控制开关")
    feeder_status = fields.CharField(max_length=20, null=True, description="下料器状态")
    date = fields.DateField(null=True, description="日期")
    feeding_status = fields.CharField(max_length=20, null=True, description="采食状态")
    feeding_date = fields.DateField(null=True, description="采食日期")
    is_normal = fields.BooleanField(null=True, description="正常")
    last_set_time = fields.DatetimeField(null=True, description="上次设置时间")
    status = fields.CharField(max_length=20, null=True, description="状态")

    class Meta:
        table = "user"


class Role(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="角色名称", index=True)
    desc = fields.CharField(max_length=500, null=True, description="角色描述")
    menus = fields.ManyToManyField("models.Menu", related_name="role_menus")
    apis = fields.ManyToManyField("models.Api", related_name="role_apis")

    class Meta:
        table = "role"


class Api(BaseModel, TimestampMixin):
    path = fields.CharField(max_length=100, description="API路径", index=True)
    method = fields.CharEnumField(MethodType, description="请求方法", index=True)
    summary = fields.CharField(max_length=500, description="请求简介", index=True)
    tags = fields.CharField(max_length=100, description="API标签", index=True)

    class Meta:
        table = "api"


class Menu(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, description="菜单名称", index=True)
    remark = fields.JSONField(null=True, description="保留字段")
    menu_type = fields.CharEnumField(MenuType, null=True, description="菜单类型")
    icon = fields.CharField(max_length=100, null=True, description="菜单图标")
    path = fields.CharField(max_length=100, description="菜单路径", index=True)
    order = fields.IntField(default=0, description="排序", index=True)
    parent_id = fields.IntField(default=0, description="父菜单ID", index=True)
    is_hidden = fields.BooleanField(default=False, description="是否隐藏")
    component = fields.CharField(max_length=100, description="组件")
    keepalive = fields.BooleanField(default=True, description="存活")
    redirect = fields.CharField(max_length=100, null=True, description="重定向")

    class Meta:
        table = "menu"


class Dept(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="部门名称", index=True)
    desc = fields.CharField(max_length=500, null=True, description="备注")
    is_deleted = fields.BooleanField(default=False, description="软删除标记", index=True)
    order = fields.IntField(default=0, description="排序", index=True)
    parent_id = fields.IntField(default=0, max_length=10, description="父部门ID", index=True)

    class Meta:
        table = "dept"


class DeptClosure(BaseModel, TimestampMixin):
    ancestor = fields.IntField(description="父代", index=True)
    descendant = fields.IntField(description="子代", index=True)
    level = fields.IntField(default=0, description="深度", index=True)


class AuditLog(BaseModel, TimestampMixin):
    user_id = fields.IntField(description="用户ID", index=True)
    username = fields.CharField(max_length=64, default="", description="用户名称", index=True)
    module = fields.CharField(max_length=64, default="", description="功能模块", index=True)
    summary = fields.CharField(max_length=128, default="", description="请求描述", index=True)
    method = fields.CharField(max_length=10, default="", description="请求方法", index=True)
    path = fields.CharField(max_length=255, default="", description="请求路径", index=True)
    status = fields.IntField(default=-1, description="状态码", index=True)
    response_time = fields.IntField(default=0, description="响应时间(单位ms)", index=True)
    request_args = fields.JSONField(null=True, description="请求参数")
    response_body = fields.JSONField(null=True, description="返回数据")
