"""
MCP-Optimized Response Schemas
Response models specifically designed for LLM consumption via Model Context Protocol

These schemas are optimized for:
1. Clarity and brevity (LLM token efficiency)
2. Type safety (prevent parsing errors)
3. Claude API compatibility
4. Token tracking and cost visibility

"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from datetime import datetime
from enum import Enum


class LLMTokenMetadata(BaseModel):
    """Token usage metadata for Claude API calls."""
    
    input_tokens: int = Field(..., ge=0, description="Tokens consumed from input")
    output_tokens: int = Field(..., ge=0, description="Tokens generated in output")
    total_tokens: int = Field(..., ge=0, description="Total tokens used")
    model: str = Field(default="claude-3-5-sonnet-20241022", description="Claude model used")
    cost_usd: float = Field(..., ge=0, description="Cost of the API call in USD")
    cache_creation_input_tokens: Optional[int] = Field(None, ge=0, description="Cache creation tokens (if applicable)")
    cache_read_input_tokens: Optional[int] = Field(None, ge=0, description="Cache read tokens (if applicable)")


class MCPAnalysisMetadata(BaseModel):
    """Metadata optimized for MCP/LLM consumption."""
    
    request_timestamp: datetime = Field(..., description="When the request was received")
    processing_timestamp: datetime = Field(..., description="When processing completed")
    total_processing_time_ms: float = Field(..., ge=0, description="Total time in milliseconds")
    astrology_calculation_time_ms: Optional[float] = Field(None, ge=0, description="Astrology calc time")
    ml_inference_time_ms: Optional[float] = Field(None, ge=0, description="ML inference time")
    llm_api_request_time_ms: Optional[float] = Field(None, ge=0, description="LLM API request duration")
    llm_tokens: Optional[LLMTokenMetadata] = Field(None, description="Claude API token usage")
    data_source: str = Field(default="vedastro", description="Data source system")
    calculation_method: str = Field(default="composite", description="Analysis method: composite (ml+astro), ml_only, astro_only")


class MCPScore(BaseModel):
    """Score object optimized for LLM consumption."""
    
    value: float = Field(..., ge=0.0, le=100.0, description="Score value (0-100)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence (0-1)")
    category: str = Field(..., description="Score category (e.g., 'wealth', 'health', 'relationships')")
    interpretation: str = Field(..., description="Human-readable interpretation")
    model_version: Optional[str] = Field(None, description="Model version that generated this score")


class MCPAstroScore(BaseModel):
    """Astrology score object optimized for LLM consumption."""
    
    name: str = Field(..., description="Name of astrology metric (e.g., 'Guna Milan', 'Doshas')")
    value: Union[int, float] = Field(..., description="Numeric value")
    max_value: Optional[Union[int, float]] = Field(None, description="Maximum possible value")
    percentage: Optional[float] = Field(None, ge=0, le=100, description="Percentage score if applicable")
    interpretation: str = Field(..., description="Human-readable interpretation")
    significance: str = Field(..., description="Significance level: 'critical', 'high', 'medium', 'low'")


class MCPAIInsight(BaseModel):
    """Individual AI insight optimized for clarity."""
    
    title: str = Field(..., max_length=200, description="Insight title")
    content: str = Field(..., description="Detailed insight content")
    category: str = Field(..., description="Category: 'analysis', 'prediction', 'recommendation', 'warning'")
    confidence: float = Field(..., ge=0.0, le=1.0, description="LLM confidence in this insight")
    source: str = Field(..., description="Source: 'ml_model', 'astrology', 'llm_synthesis'")


class MCPAnalysisResponse(BaseModel):
    """
    Optimized AI analysis response for LLM consumption via MCP.
    
    This response is specifically designed to be consumed by Claude and other LLMs
    without unnecessary data or formatting that wastes tokens.
    """
    
    status: str = Field(default="success", description="Response status: 'success', 'partial', 'error'")
    request_type: str = Field(..., description="Type of analysis: 'personal', 'compatibility'")
    
    # Scores section (condensed but complete)
    ml_scores: Dict[str, MCPScore] = Field(
        ...,
        description="ML model predictions for various life aspects"
    )
    astrology_scores: List[MCPAstroScore] = Field(
        ...,
        description="Traditional Vedic astrology scores"
    )
    
    # Analysis section (AI-generated insights)
    summary: str = Field(
        ...,
        description="Brief summary of the complete analysis"
    )
    insights: List[MCPAIInsight] = Field(
        default_factory=list,
        description="Detailed insights from AI synthesis"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable recommendations"
    )
    
    # Compatibility-specific (optional)
    compatibility_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Overall compatibility percentage (for compatibility analysis)"
    )
    harmony_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Harmony score combining ML and astrology (for compatibility analysis)"
    )
    match_summary: Optional[str] = Field(
        None,
        description="Summary of compatibility match (for compatibility analysis)"
    )
    
    # Metadata
    metadata: MCPAnalysisMetadata = Field(..., description="Processing metadata")
    
    # Error handling
    error_message: Optional[str] = Field(None, description="Error message if status is 'error' or 'partial'")
    fallback_used: bool = Field(
        default=False,
        description="Whether rule-based fallback analysis was used instead of LLM"
    )


class MCPCompatibilityRequest(BaseModel):
    """Optimized request schema for compatibility analysis."""
    
    user_name: str = Field(..., description="User's name")
    user_birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    user_birth_time: str = Field(..., description="Birth time (HH:MM:SS)")
    user_birth_location: str = Field(..., description="Birth location (city, country)")
    
    partner_name: str = Field(..., description="Partner's name")
    partner_birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    partner_birth_time: str = Field(..., description="Birth time (HH:MM:SS)")
    partner_birth_location: str = Field(..., description="Birth location (city, country)")
    
    analysis_context: str = Field(
        default="marriage",
        description="Context: 'marriage', 'dating', 'business', 'friendship'"
    )
    include_doshas: bool = Field(default=True, description="Include dosha analysis")
    include_predictions: bool = Field(default=True, description="Include future predictions")


class MCPPersonalAnalysisRequest(BaseModel):
    """Optimized request schema for personal analysis."""
    
    name: str = Field(..., description="Person's name")
    birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    birth_time: str = Field(..., description="Birth time (HH:MM:SS)")
    birth_location: str = Field(..., description="Birth location (city, country)")
    
    analysis_context: str = Field(
        default="general",
        description="Context: 'general', 'career', 'health', 'relationships', 'finance'"
    )
    include_doshas: bool = Field(default=True, description="Include dosha analysis")
    include_predictions: bool = Field(default=True, description="Include future predictions")


class MCPErrorResponse(BaseModel):
    """Error response for MCP requests."""
    
    status: str = Field(default="error", description="Status: 'error'")
    error_code: str = Field(..., description="Error code (e.g., 'INVALID_INPUT', 'LLM_TIMEOUT')")
    error_message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, str]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class MCPBatchResponse(BaseModel):
    """Response for batch analysis requests."""
    
    status: str = Field(default="success", description="Overall status")
    total_requests: int = Field(..., ge=1, description="Total requests in batch")
    successful: int = Field(..., ge=0, description="Successful requests")
    failed: int = Field(..., ge=0, description="Failed requests")
    results: List[Union[MCPAnalysisResponse, MCPErrorResponse]] = Field(
        ...,
        description="Individual results for each request"
    )
    total_tokens_used: int = Field(..., ge=0, description="Total tokens used for entire batch")
    total_cost_usd: float = Field(..., ge=0, description="Total cost in USD for entire batch")
    processing_time_ms: float = Field(..., ge=0, description="Total processing time")
