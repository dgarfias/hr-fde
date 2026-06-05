from fastapi import APIRouter, Depends
from app.schemas import FMCSAVerifyRequest, FMCSAVerifyResponse
from app.services.fmcsa_service import verify_mc_number

router = APIRouter()

@router.post("/verify", response_model=FMCSAVerifyResponse)
async def verify_carrier(request: FMCSAVerifyRequest):
    result = await verify_mc_number(request.mc_number)
    return result
