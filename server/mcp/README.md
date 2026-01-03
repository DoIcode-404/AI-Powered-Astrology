# MCP Tools for Vedic Astrology AI Analysis

Model Context Protocol (MCP) tool definitions for integrating Vedic astrology AI analysis with Claude and other AI assistants.

## Tools

### 1. get_compatibility_analysis

Analyzes compatibility between two people using their birth chart data.

**Input:**
- `user_kundali`: Birth data (date, time, location) for person 1
- `partner_kundali`: Birth data for person 2 (optional)
- `context`: Analysis type (default: "compatibility")

**Output:**
- `summary`: AI-generated summary text
- `detailed_insights`: List of specific insights
- `recommendations`: Actionable recommendations
- `ml_scores`: ML model predictions with confidence
- `astrology_scores`: Traditional Vedic scores

### 2. get_personal_analysis

Analyzes a single person's chart for career, wealth, health prospects.

**Input:**
- `user_kundali`: Birth data
- `context`: Focus area (general, career, health, wealth)

**Output:**
- `summary`: Analysis summary
- `detailed_insights`: Key insights
- `recommendations`: Personalized advice

## Usage Examples

### Example 1: Compatibility Analysis

```json
{
  "tool": "get_compatibility_analysis",
  "input": {
    "user_kundali": {
      "birthDate": "1990-05-15",
      "birthTime": "14:30",
      "latitude": 19.076,
      "longitude": 72.8777,
      "timezone": "Asia/Kolkata"
    },
    "partner_kundali": {
      "birthDate": "1992-08-20",
      "birthTime": "10:15",
      "latitude": 28.6139,
      "longitude": 77.209,
      "timezone": "Asia/Kolkata"
    },
    "context": "compatibility"
  }
}
```

**Response:**
```json
{
  "summary": "Compatibility score: 24/36 points. ML analysis indicates 68% overall harmony.",
  "detailed_insights": [
    "Strong career indicators (confidence: 88%)",
    "Good emotional compatibility",
    "Moderate challenges in communication area"
  ],
  "recommendations": [
    "Focus on joint financial planning",
    "Support each other's career goals"
  ],
  "ml_scores": {
    "wealth": {
      "score": 0.75,
      "confidence": 0.92,
      "model_version": "v1.0"
    },
    "career": {
      "score": 0.68,
      "confidence": 0.88,
      "model_version": "v1.0"
    }
  },
  "astrology_scores": {
    "guna_milan_total": 24,
    "koota_varna": 1,
    "koota_vashya": 2
  }
}
```

### Example 2: Personal Career Analysis

```json
{
  "tool": "get_personal_analysis",
  "input": {
    "user_kundali": {
      "birthDate": "1990-05-15",
      "birthTime": "14:30",
      "latitude": 19.076,
      "longitude": 72.8777,
      "timezone": "Asia/Kolkata"
    },
    "context": "career"
  }
}
```

**Response:**
```json
{
  "summary": "Overall analysis shows 72% positive indicators across life areas.",
  "detailed_insights": [
    "Strong career indicators (confidence: 90%)",
    "Good leadership potential",
    "Favorable for entrepreneurship"
  ],
  "recommendations": [
    "Consider leadership roles",
    "Focus on building professional network"
  ]
}
```

## Integration with Claude

### Python MCP Client Example

```python
import requests

def get_compatibility_analysis(user_birth, partner_birth):
    """
    Call MCP tool via API endpoint.

    Args:
        user_birth: Dict with birthDate, birthTime, latitude, longitude, timezone
        partner_birth: Dict with same fields

    Returns:
        Dict with summary, insights, recommendations
    """
    url = "http://localhost:8000/api/ai-analysis"

    payload = {
        "user_kundali": user_birth,
        "partner_kundali": partner_birth,
        "context": "compatibility"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()["data"]
        return {
            "summary": data["ai_analysis"]["summary"],
            "detailed_insights": data["ai_analysis"]["detailed_insights"],
            "recommendations": data["ai_analysis"]["recommendations"],
            "ml_scores": data["ml_scores"],
            "astrology_scores": data["astrology_scores"]
        }
    elif response.status_code == 503:
        return {"error": "ML service unavailable, please retry"}
    else:
        return {"error": f"Analysis failed: {response.text}"}

# Usage
user = {
    "birthDate": "1990-05-15",
    "birthTime": "14:30",
    "latitude": 19.076,
    "longitude": 72.8777,
    "timezone": "Asia/Kolkata"
}

partner = {
    "birthDate": "1992-08-20",
    "birthTime": "10:15",
    "latitude": 28.6139,
    "longitude": 77.209,
    "timezone": "Asia/Kolkata"
}

result = get_compatibility_analysis(user, partner)
print(result["summary"])
```

### JavaScript/TypeScript Example

```typescript
interface KundaliData {
  birthDate: string;
  birthTime: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

interface CompatibilityResult {
  summary: string;
  detailed_insights: string[];
  recommendations: string[];
  ml_scores: Record<string, {score: number, confidence: number, model_version: string}>;
  astrology_scores: Record<string, number>;
}

async function getCompatibilityAnalysis(
  user: KundaliData,
  partner: KundaliData
): Promise<CompatibilityResult> {
  const response = await fetch('http://localhost:8000/api/ai-analysis', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_kundali: user,
      partner_kundali: partner,
      context: 'compatibility'
    })
  });

  if (!response.ok) {
    throw new Error(`Analysis failed: ${response.statusText}`);
  }

  const data = await response.json();
  return {
    summary: data.data.ai_analysis.summary,
    detailed_insights: data.data.ai_analysis.detailed_insights,
    recommendations: data.data.ai_analysis.recommendations,
    ml_scores: data.data.ml_scores,
    astrology_scores: data.data.astrology_scores
  };
}

// Usage
const user = {
  birthDate: "1990-05-15",
  birthTime: "14:30",
  latitude: 19.076,
  longitude: 72.8777,
  timezone: "Asia/Kolkata"
};

const partner = {
  birthDate: "1992-08-20",
  birthTime: "10:15",
  latitude: 28.6139,
  longitude: 77.209,
  timezone: "Asia/Kolkata"
};

const result = await getCompatibilityAnalysis(user, partner);
console.log(result.summary);
```

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success - Analysis completed
- **422**: Validation Error - Invalid birth data
- **500**: Server Error - Internal processing error
- **503**: Service Unavailable - ML models not loaded

### Error Response Format

```json
{
  "status": "error",
  "success": false,
  "error_message": "ML service is currently unavailable",
  "error_code": "ML_SERVICE_UNAVAILABLE",
  "timestamp": "2025-12-08T10:30:00Z"
}
```

## Response Schema Validation

All successful responses are validated against strict Pydantic schemas:

- `ml_scores`: Always Dict[str, MLScoreBox], never List
- `astrology_scores`: Always Dict[str, Union[int, float]], never List
- `ai_analysis`: Fixed structure with summary, insights, recommendations

This prevents runtime type errors (Map vs List) in client applications.

## Configuration

Set environment variables:

```bash
# API base URL
export ASTROLOGY_API_BASE_URL=http://localhost:8000

# Optional authentication token
export ASTROLOGY_API_TOKEN=your-token-here
```

## Rate Limits

- 10 requests per minute
- 100 requests per hour
- Estimated response time: ~2000ms

## Support

For issues or questions:
- GitHub Issues: [repository-url]
- API Documentation: http://localhost:8000/docs
