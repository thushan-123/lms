from fastapi import APIRouter , Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Function.function import db_dependency
from Authorization.auth import oauth2_scheme, decode_token_access_role
from Loggers.log import app_log, err_log
from Schemas.BranchManagement.branchManagementSchema import BranchRequestSchema, DeleteBranchSchema, UpdateActiveField, BranchUpdateRequestSchema
from .manageBranchFunction import create_branch, delete_branch_cascade, update_branch_active_field, update_branch, retrieve_branch

router = APIRouter()

@router.post("/createBranch")
async def create_new_branch(request: BranchRequestSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin'])
        if payload is not None:
            result = await create_branch(db,request.branch[0].branch_id,dict(request.branch[0]),request.branch_halls,request.branch_images_urls)
            if result:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status": True, "detail":"branch is created successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "Failed to insert branch data. Possible duplicate entry"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageBranch - create_new_branch | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.delete("/deleteBranch")
async def deleting_branch(request: DeleteBranchSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin'])
        if payload:
            result = await delete_branch_cascade(db, request.branch_id)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "delete successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "not found branches"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageBranch - deleting_branch | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.put("/updateActiveDeactivate")
async def update_branch_active(request: UpdateActiveField, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials, ['admin'])
        if payload:
            result = await update_branch_active_field(db,request.branch_id,request.active)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "update active field"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "branch not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageBranch - deleting_branch | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.put("/updateBranch")
async def update_branch_data(request: BranchUpdateRequestSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager'])
        if payload:
            result = await update_branch(db,str(request.branch[0].branch_id),dict(request.branch[0]),request.branch_halls,request.branch_images_urls)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "branch update successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "update fail"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageBranch - update_branch_data | error {e} branch_id: {str(request.branch[0].branch_id)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.get("/getBranchDetail/{branch_id}")
async def selecting_branch_details(branch_id: str, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic'])
        if payload:
            result = await retrieve_branch(db,branch_id)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": jsonable_encoder(result)})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageBranch - update_branch_data | error {e} branch_id: {str(branch_id)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})