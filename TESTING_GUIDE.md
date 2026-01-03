# Complete Testing Guide - AI Analysis Endpoint

**Status**: ✅ All 422 Validation Errors Fixed  
**Date**: December 2025

---

## Quick Test (2 Minutes)

### Start Server
```bash
cd c:\Users\ACER\Desktop\FInalProject
python -m uvicorn server.main:app --reload
```

### Test Single Person Analysis
```bash
curl -X POST http://localhost:8000/api/ai-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "user_kundali": {
      "name": "John Doe",
      "birth_date": "1990-01-15",
      "birth_time": "10:30:00",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timezone": "America/New_York"
    },
    "context": "general"
  }'
```

### Expected Response
You should get a **200 OK** with JSON containing:
- ✅ `ml_scores` - ML predictions
- ✅ `astrology_scores` - Vedic calculations
- ✅ `ai_analysis` - AI-generated insights (optional; rule-based fallback available)
- ✅ `metadata` - Token tracking and costs

---

## PowerShell Test Script

Save as `test_api.ps1`:

```powershell
# Test AI Analysis Endpoint
$apiUrl = "http://localhost:8000/api/ai-analysis"

# Create request body
$body = @{
    user_kundali = @{
        name = "Test Person"
        birth_date = "1990-01-15"
        birth_time = "10:30:00"
        latitude = 40.7128
        longitude = -74.0060
        timezone = "America/New_York"
    }
    context = "general"
} | ConvertTo-Json

Write-Host "Sending request to $apiUrl" -ForegroundColor Cyan
Write-Host "Request body:" -ForegroundColor Yellow
Write-Host $body

try {
    $response = Invoke-WebRequest -Uri $apiUrl `
        -Method POST `
        -Headers @{"Content-Type" = "application/json"} `
        -Body $body
    
    Write-Host "`nResponse Status: $($response.StatusCode) " -ForegroundColor Green
    Write-Host "Response Body:" -ForegroundColor Cyan
    
    $content = $response.Content | ConvertFrom-Json
    $content | ConvertTo-Json -Depth 10 | Write-Host
    
    # Check for token tracking
    if ($content.data.metadata.llm_tokens) {
        Write-Host "`n✓ Token Tracking Enabled" -ForegroundColor Green
        Write-Host "Input tokens: $($content.data.metadata.llm_tokens.input_tokens)" -ForegroundColor Green
        Write-Host "Output tokens: $($content.data.metadata.llm_tokens.output_tokens)" -ForegroundColor Green
        Write-Host "Cost: $($content.data.metadata.llm_tokens.cost_usd) USD" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Token tracking not available" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "`nError: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.Value__)" -ForegroundColor Red
    Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
}
```

Run with:
```powershell
.\test_api.ps1
```

---

## Detailed Test Scenarios

### Test 1: Valid Request (should return 200)

**Request**:
```json
{
  "user_kundali": {
    "name": "Alice Smith",
    "birth_date": "1985-03-20",
    "birth_time": "14:30:00",
    "latitude": 51.5074,
    "longitude": -0.1278,
    "timezone": "Europe/London"
  },
  "context": "career"
}
```

**Expected**:
- Status: 200 OK
- Response includes analysis
- Token tracking visible

---

### Test 2: Minimal Required Fields (should return 200)

**Request**:
```json
{
  "user_kundali": {
    "birth_date": "1990-01-15",
    "birth_time": "10:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}
```

**Expected**:
- Status: 200 OK
- Uses default timezone: UTC
- Response includes analysis

---

### Test 3: Different Contexts

**Test 3a: Health Context**
```json
{
  "user_kundali": {
    "birth_date": "1990-01-15",
    "birth_time": "10:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York"
  },
  "context": "health"
}
```

**Test 3b: Finance Context**
```json
{
  "user_kundali": {
    "birth_date": "1990-01-15",
    "birth_time": "10:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York"
  },
  "context": "finance"
}
```

---

### Test 4: Compatibility Analysis

**Request**:
```json
{
  "user_kundali": {
    "name": "Person A",
    "birth_date": "1990-01-15",
    "birth_time": "10:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York"
  },
  "partner_kundali": {
    "name": "Person B",
    "birth_date": "1992-05-20",
    "birth_time": "14:15:00",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "timezone": "America/Los_Angeles"
  },
  "context": "marriage"
}
```

**Endpoint**: `POST /api/ai-analysis/compatibility`

---

## Troubleshooting Failed Tests

### Problem: 422 Validation Error

**Cause**: Request format doesn't match schema

**Solution**:
1. Check all required fields are present
2. Verify field names match (use snake_case)
3. Verify date format: YYYY-MM-DD
4. Verify time format: HH:MM:SS
5. Verify timezone is valid

**Check with**:
```bash
# This should pass
curl -X POST http://localhost:8000/api/ai-analysis \
  -H "Content-Type: application/json" \
  -d '{"user_kundali":{"birth_date":"1990-01-15","birth_time":"10:30:00","latitude":40.7128,"longitude":-74.0060,"timezone":"UTC"}}'
```

---

### Problem: 503 Service Unavailable

**Cause**: ML models not loaded or Claude API not configured

**Solution**:
1. (Optional) If you require AI-generated analysis, ensure `ANTHROPIC_API_KEY` is set in `.env`. Otherwise the service will use rule-based fallback.
2. Restart server after adding .env
3. Check server logs for errors

---

### Problem: 500 Internal Server Error

**Cause**: Server error during processing

**Solution**:
1. Check server logs for detailed error
2. Verify birth coordinates are valid
3. Try with different birth date/time

---

## Interactive Testing with Swagger UI

### Access Swagger Documentation
```
http://localhost:8000/docs
```

**Benefits**:
- ✅ See request/response schemas
- ✅ Try requests directly in browser
- ✅ See automatic validation
- ✅ Copy-paste curl commands

### Steps:
1. Navigate to http://localhost:8000/docs
2. Find "POST /api/ai-analysis"
3. Click "Try it out"
4. Fill in request body
5. Click "Execute"
6. See response

---

## Monitoring Response Quality

### Check ML Scores
```json
{
  "ml_scores": {
    "wealth": {
      "score": 72.5,          // Should be 0-100
      "confidence": 0.88,     // Should be 0-1
      "model_version": "v1.2"
    }
  }
}
```

### Check Token Tracking
```json
{
  "metadata": {
    "llm_tokens": {
      "input_tokens": 450,        // Tokens sent to LLM (if enabled)
      "output_tokens": 280,       // Tokens generated by LLM (if enabled)
      "total_tokens": 730,        // Should equal input + output
      "cost_usd": 0.00387,        // Input cost + output cost (LLM, optional)
      "model": "<LLM_MODEL_OPTIONAL>"
    }
  }
}
```

### Check Processing Times
```json
{
  "metadata": {
    "astrology_calculation_time_ms": 250,  // Vedic calc time
    "ml_inference_time_ms": 1200,          // ML model time
    "llm_api_request_time_ms": 2500,       // LLM request time (if enabled)
    "total_processing_time_ms": 3950       // Total
  }
}
```

---

## Performance Expectations

| Metric | Expected | Notes |
|--------|----------|-------|
| Astrology calc | 200-300 ms | PySwissEph calculations |
| ML inference | 1000-2000 ms | XGBoost predictions |
| LLM (optional) | 2000-4000 ms | LLM generation (if enabled) |
| **Total** | **3500-6000 ms** | ~5 seconds typical |

---

## Cost Verification

**Typical request costs**:
- Input tokens: 400-500 tokens = $0.0012-0.0015
- Output tokens: 250-350 tokens = $0.0022-0.0031
- Total: **$0.003-0.005 per request**

**If costs are high**:
1. Check input_tokens count
2. Verify you're not sending duplicate data
3. Monitor in your LLM provider console (if you enabled an external LLM)

---

## Test Success Criteria

Your implementation is working correctly when:

- ✅ Server starts without errors
- ✅ Endpoint returns 200 status
- ✅ Response includes ml_scores (dict with numeric values)
- ✅ Response includes astrology_scores (dict)
- ✅ Response includes ai_analysis (with text insights)
- ✅ Response includes metadata with llm_tokens
- ✅ Token counts are reasonable (400-500 input, 250-350 output)
- ✅ Cost is ~$0.003-0.005 per request
- ✅ Processing takes ~5 seconds
- ✅ Multiple requests work consistently

---

## Debugging Tools

### VS Code REST Client
Create file: `test.http`
```http
POST http://localhost:8000/api/ai-analysis
Content-Type: application/json

{
  "user_kundali": {
    "birth_date": "1990-01-15",
    "birth_time": "10:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York"
  }
}
```

### Postman
1. New Request
2. Method: POST
3. URL: http://localhost:8000/api/ai-analysis
4. Headers: Content-Type: application/json
5. Body (raw JSON): Your request
6. Send

### Python Test Script
```python
import requests
import json

url = "http://localhost:8000/api/ai-analysis"
payload = {
    "user_kundali": {
        "birth_date": "1990-01-15",
        "birth_time": "10:30:00",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York"
    }
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start server | `python -m uvicorn server.main:app --reload` |
| Run PowerShell test | `.\test_api.ps1` |
| Access Swagger | `http://localhost:8000/docs` |
| Test endpoint | See curl commands above |
| Check logs | Server output in terminal |

---

**Status**: ✅ Ready for Testing  
**All 422 Errors**: Fixed  
**Test Success Rate**: Should be 100%
