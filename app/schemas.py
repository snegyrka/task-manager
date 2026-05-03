"""Pydantic-беҐ¬л ¤«п ў «Ё¤ жЁЁ ¤ ­­ле API."""

import re

from datetime import datetime

from typing import Optional



from pydantic import BaseModel, EmailStr, field_validator



from app.models import TaskStatus, TaskPriority





class UserCreate(BaseModel):

    """‘еҐ¬  ¤«п аҐЈЁбва жЁЁ ­®ў®Ј® Ї®«м§®ў вҐ«п."""

    username: str

    email: EmailStr

    password: str



    @field_validator('username')

    @classmethod

    def username_must_be_valid(cls, val: str) -> str:

        if len(val) < 3:

            raise ValueError('€¬п Ї®«м§®ў вҐ«п ¤®«¦­® Ўлвм ­Ґ ¬Ґ­ҐҐ 3 бЁ¬ў®«®ў')

        if len(val) > 30:

            raise ValueError('€¬п Ї®«м§®ў вҐ«п ¤®«¦­® Ўлвм ­Ґ Ў®«ҐҐ 30 бЁ¬ў®«®ў')

        if not val.isalnum():

            raise ValueError('€¬п Ї®«м§®ў вҐ«п ¤®«¦­® б®¤Ґа¦ вм в®«мЄ® ЎгЄўл Ё жЁдал')

        return val



    @field_validator('password')

    @classmethod

    def password_must_be_strong(cls, val: str) -> str:

        if len(val) < 8:

            raise ValueError('Џ а®«м ¤®«¦Ґ­ Ўлвм ­Ґ ¬Ґ­ҐҐ 8 бЁ¬ў®«®ў')

        if not re.search(r'[A-Z]', val):

            raise ValueError('Џ а®«м ¤®«¦Ґ­ б®¤Ґа¦ вм е®вп Ўл ®¤­г § Ј« ў­го ЎгЄўг')

        if not re.search(r'[a-z]', val):

            raise ValueError('Џ а®«м ¤®«¦Ґ­ б®¤Ґа¦ вм е®вп Ўл ®¤­г бва®з­го ЎгЄўг')

        if not re.search(r'\d', val):

            raise ValueError('Џ а®«м ¤®«¦Ґ­ б®¤Ґа¦ вм е®вп Ўл ®¤­г жЁдаг')

        return val





class UserResponse(BaseModel):

    """‘еҐ¬  ¤«п ®вўҐв  б ¤ ­­л¬Ё Ї®«м§®ў вҐ«п."""

    id: int

    username: str

    email: str

    class Config:

        from_attributes = True





class Token(BaseModel):

    """‘еҐ¬  ¤«п JWT-в®ЄҐ­ ."""

    access_token: str

    token_type: str





class ProjectCreate(BaseModel):

    """‘еҐ¬  ¤«п б®§¤ ­Ёп Їа®ҐЄв ."""

    name: str

    description: str = ""

    @field_validator('name')

    @classmethod

    def name_must_not_be_empty(cls, val: str) -> str:

        if not val.strip():

            raise ValueError('Ќ §ў ­ЁҐ Їа®ҐЄв  ­Ґ ¬®¦Ґв Ўлвм Їгбвл¬')

        return val.strip()





class ProjectResponse(BaseModel):

    """‘еҐ¬  ¤«п ®вўҐв  б ¤ ­­л¬Ё Їа®ҐЄв ."""

    id: int

    name: str

    description: str

    owner_id: int

    class Config:

        from_attributes = True





class TaskCreate(BaseModel):

    """‘еҐ¬  ¤«п б®§¤ ­Ёп § ¤ зЁ."""

    title: str

    description: str = ""

    status: TaskStatus = TaskStatus.TODO

    priority: TaskPriority = TaskPriority.MEDIUM

    estimated_hours: int = 0

    deadline: Optional[datetime] = None

    project_id: int

    assignee_id: Optional[int] = None

    @field_validator('title')

    @classmethod

    def title_must_not_be_empty(cls, val: str) -> str:

        if not val.strip():

            raise ValueError('Ќ §ў ­ЁҐ § ¤ зЁ ­Ґ ¬®¦Ґв Ўлвм Їгбвл¬')

        return val.strip()

    @field_validator('estimated_hours')

    @classmethod

    def hours_must_be_positive(cls, val: int) -> int:

        if val < 0:

            raise ValueError('ЋжҐ­Є  ўаҐ¬Ґ­Ё ­Ґ ¬®¦Ґв Ўлвм ®ваЁж вҐ«м­®©')

        return val





class TaskResponse(BaseModel):

    """‘еҐ¬  ¤«п ®вўҐв  б ¤ ­­л¬Ё § ¤ зЁ."""

    id: int

    title: str

    description: str

    status: TaskStatus

    priority: TaskPriority

    estimated_hours: int

    deadline: Optional[datetime]

    created_at: datetime

    project_id: int

    assignee_id: Optional[int]

    class Config:

        from_attributes = True





class WorkloadResponse(BaseModel):

    """‘еҐ¬  ¤«п ®вўҐв  ® § Јаг§ЄҐ ЁбЇ®«­ЁвҐ«п."""

    user_id: int

    username: str

    total_hours: int

    task_count: int





class DeadlineTask(BaseModel):

    """‘еҐ¬  ¤«п § ¤ з б ЇаЁЎ«Ё¦ ойЁ¬бп ¤Ґ¤« ©­®¬."""

    task_id: int

    title: str

    days_until_deadline: int

