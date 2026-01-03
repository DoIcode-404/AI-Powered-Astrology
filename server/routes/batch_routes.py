"""Batch processing routes for ML training"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from server.services.logic import generate_kundali_logic
from server.pydantic_schemas.kundali_schema import KundaliRequest
from server.services.geocoding import geocode_location

router = APIRouter()

class BatchRecord(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    location: str

class BatchRequest(BaseModel):
    records: List[BatchRecord]

@router.post('/batch/kundali')
async def batch_generate_kundali(request: BatchRequest):
    """Generate kundalis for multiple birth records (no DB save)"""
    results = []
    for record in request.records:
        try:
            geo = geocode_location(record.location)
            req = KundaliRequest(
                birthDate=record.birth_date,
                birthTime=record.birth_time,
                location=record.location,
                latitude=geo['latitude'],
                longitude=geo['longitude'],
                timezone=geo['timezone']
            )
            kundali = await generate_kundali_logic(req)
            results.append({
                'name': record.name,
                'success': True,
                'data': kundali.model_dump()
            })
        except Exception as e:
            results.append({
                'name': record.name,
                'success': False,
                'error': str(e)
            })

    return {'results': results}
