#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2023-02-15 20:03:49
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 帮助中心视图

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from core.database import db_getter
from utils.response import SuccessResponse
from . import schemas, crud, params, models
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth

app = APIRouter()


###########################################################
#    类别管理
###########################################################
@app.get("/issue/categorys/", summary="获取类别列表")
async def get_issue_categorys(p: params.IssueCategoryParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    model = models.VadminIssueCategory
    options = [joinedload(model.user)]
    schema = schemas.IssueCategoryListOut
    datas = await crud.IssueCategoryDal(auth.db).get_datas(**p.dict(), v_options=options, v_schema=schema)
    count = await crud.IssueCategoryDal(auth.db).get_count(**p.to_count())
    return SuccessResponse(datas, count=count, refresh=auth.refresh)


@app.get("/issue/categorys/options/", summary="获取类别选择项")
async def get_issue_categorys_options(auth: Auth = Depends(AllUserAuth())):
    schema = schemas.IssueCategoryOptionsOut
    return SuccessResponse(
        await crud.IssueCategoryDal(auth.db).get_datas(limit=0, is_active=True, v_schema=schema),
        refresh=auth.refresh
    )


@app.post("/issue/categorys/", summary="创建类别")
async def create_issue_category(data: schemas.IssueCategory, auth: Auth = Depends(AllUserAuth())):
    data.user_id = auth.user.id
    return SuccessResponse(await crud.IssueCategoryDal(auth.db).create_data(data=data), refresh=auth.refresh)


@app.delete("/issue/categorys/", summary="批量删除类别", description="硬删除")
async def delete_issue_categorys(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.IssueCategoryDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功", refresh=auth.refresh)


@app.put("/issue/categorys/{data_id}/", summary="更新类别信息")
async def put_issue_category(data_id: int, data: schemas.IssueCategory, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.IssueCategoryDal(auth.db).put_data(data_id, data), refresh=auth.refresh)


@app.get("/issue/categorys/{data_id}/", summary="获取类别信息")
async def get_issue_category(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.IssueCategorySimpleOut
    return SuccessResponse(
        await crud.IssueCategoryDal(auth.db).get_data(data_id, v_schema=schema),
        refresh=auth.refresh
    )


@app.get("/issue/categorys/platform/{platform}/", summary="获取平台中的常见问题类别列表")
async def get_issue_category_platform(platform: str, db: AsyncSession = Depends(db_getter)):
    model = models.VadminIssueCategory
    options = [joinedload(model.issues)]
    schema = schemas.IssueCategoryPlatformOut
    result = await crud.IssueCategoryDal(db).\
        get_datas(platform=platform, is_active=True, v_schema=schema, v_options=options)
    return SuccessResponse(result)


###########################################################
#    问题管理
###########################################################
@app.get("/issues/", summary="获取问题列表")
async def get_issues(p: params.IssueParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    model = models.VadminIssue
    options = [joinedload(model.user), joinedload(model.category)]
    schema = schemas.IssueListOut
    datas = await crud.IssueDal(auth.db).get_datas(**p.dict(), v_options=options, v_schema=schema)
    count = await crud.IssueDal(auth.db).get_count(**p.to_count())
    return SuccessResponse(datas, count=count, refresh=auth.refresh)


@app.post("/issues/", summary="创建问题")
async def create_issue(data: schemas.Issue, auth: Auth = Depends(AllUserAuth())):
    data.user_id = auth.user.id
    return SuccessResponse(await crud.IssueDal(auth.db).create_data(data=data), refresh=auth.refresh)


@app.delete("/issues/", summary="批量删除问题", description="硬删除")
async def delete_issues(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.IssueDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功", refresh=auth.refresh)


@app.put("/issues/{data_id}/", summary="更新问题信息")
async def put_issue(data_id: int, data: schemas.Issue, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.IssueDal(auth.db).put_data(data_id, data), refresh=auth.refresh)


@app.get("/issues/{data_id}/", summary="获取问题信息")
async def get_issue(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.IssueSimpleOut
    return SuccessResponse(await crud.IssueDal(db).get_data(data_id, v_schema=schema))


@app.get("/issues/add/view/number/{data_id}/", summary="更新常见问题查看次数+1")
async def issue_add_view_number(data_id: int, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.IssueDal(db).add_view_number(data_id))
