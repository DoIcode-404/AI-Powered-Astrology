"""
LLM-Based Analysis Service

Integrates Claude AI for intelligent text generation in astrology analysis.
Designed for minimal token usage through context optimization.

Provides:
- Intelligent analysis generation using Claude API
- Token tracking and cost monitoring
- Caching for repeated analysis contexts
- Fallback to rule-based generation if API fails

Author: LLM Integration Team
""" 

import logging
import time
import json
import hashlib
from typing import Dict, Optional, Tuple, Any
from anthropic import Anthropic, APIError, APIConnectionError
from server.pydantic_schemas.ml_response import AIAnalysisSection, MLScoreBox
from server.services.token_tracker import (
    TokenTracker,
    TokenUsage,
    TokenModel,
    get_token_tracker,
    record_token_usage
)

logger = logging.getLogger(__name__)


class LLMAnalysisService:
    """
    Claude AI-powered analysis service for astrology insights.

    Token optimization strategy:
    1. Compress numeric data to JSON (not prose)
    2. Only include significant findings
    3. Use structured output format
    4. Cache common interpretations
    """

    # System prompt (single, reusable across all requests)
    SYSTEM_PROMPT = """You are an expert Vedic astrology interpreter with deep knowledge of:
- Planetary strengths and weaknesses
- ML-based predictive analysis
- Guna Milan and compatibility
- Personalized remedies and recommendations

Provide concise, actionable insights based on numeric data provided.
Format your response ONLY as valid JSON with this exact structure:
{
    "summary": "2-3 sentence overview of the analysis",
    "detailed_insights": ["insight 1", "insight 2", "insight 3"],
    "recommendations": ["recommendation 1", "recommendation 2"]
}

Be specific to the scores provided. Do not add general astrology advice."""

    def __init__(self, api_key: Optional[str] = None, cache_enabled: bool = True):
        """
        Initialize LLM Analysis Service.

        Args:
            api_key: Claude API key (loads from ANTHROPIC_API_KEY env var if not provided)
            cache_enabled: Whether to cache analysis results
        """
        import os
        import httpx
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set - LLM analysis will be disabled")
            self.client = None
        else:
            try:
                # Create Anthropic client with explicit httpx configuration
                # Use httpx.Client directly to avoid socket_options incompatibility
                http_client = httpx.Client(
                    timeout=httpx.Timeout(30.0, connect=10.0)
                )
                self.client = Anthropic(api_key=self.api_key, http_client=http_client)
            except TypeError as e:
                if "socket_options" in str(e):
                    # If httpx version incompatibility occurs, use default initialization
                    logger.warning(f"HTTPTransport compatibility issue detected: {e}. Using default client.")
                    self.client = Anthropic(api_key=self.api_key)
                else:
                    raise

        self.cache_enabled = cache_enabled
        self.cache: Dict[str, AIAnalysisSection] = {} if cache_enabled else None
        self.model_name = "claude-haiku-4-5-20251001"  # Claude Haiku 4.5
        self.token_tracker = get_token_tracker()

    def _create_minimal_context(
        self,
        ml_scores: Dict[str, MLScoreBox],
        astrology_scores: Dict[str, float],
        partner_ml_scores: Optional[Dict[str, MLScoreBox]] = None,
        context: str = "general"
    ) -> Dict[str, Any]:
        """
        Create minimal context for LLM (optimized for token usage).

        Strategy:
        - Extract only top 3 scores (not all)
        - Use numeric format
        - Exclude raw chart data
        - Target: 150-300 tokens

        Args:
            ml_scores: ML predictions
            astrology_scores: Astrology scores
            partner_ml_scores: Partner scores (if compatibility)
            context: Analysis context (general, compatibility, etc.)

        Returns:
            Minimal context dictionary
        """
        # Extract top 3 ML scores
        ml_scores_sorted = sorted(
            ml_scores.items(),
            key=lambda x: x[1].score,
            reverse=True
        )
        top_ml = {name: box.score for name, box in ml_scores_sorted[:3]}

        # Extract top planetary strengths
        planetary_strengths = {
            k.replace("_strength", ""): v
            for k, v in astrology_scores.items()
            if k.endswith("_strength")
        }
        top_planetary = dict(
            sorted(planetary_strengths.items(), key=lambda x: x[1], reverse=True)[:3]
        )

        context_data = {
            "analysis_type": context,
            "top_ml_predictions": top_ml,
            "top_planetary_strengths": top_planetary,
            "chart_strength": astrology_scores.get("overall_strength", 50),
        }

        # Add compatibility-specific data
        if context == "compatibility":
            context_data["guna_milan_total"] = int(astrology_scores.get("guna_milan_total", 0))
            context_data["guna_milan_percentage"] = float(astrology_scores.get("guna_milan_percentage", 0))

            # Partner's top scores
            if partner_ml_scores:
                partner_ml_sorted = sorted(
                    partner_ml_scores.items(),
                    key=lambda x: x[1].score,
                    reverse=True
                )
                context_data["partner_top_predictions"] = {
                    name: box.score for name, box in partner_ml_sorted[:3]
                }

        return context_data

    def _hash_context(self, context_data: Dict[str, Any]) -> str:
        """
        Create hash of context for caching.

        Args:
            context_data: Context dictionary

        Returns:
            SHA256 hash of context
        """
        json_str = json.dumps(context_data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def _generate_analysis_fallback(
        self,
        ml_scores: Dict[str, MLScoreBox],
        astrology_scores: Dict[str, float],
        partner_ml_scores: Optional[Dict[str, MLScoreBox]] = None
    ) -> AIAnalysisSection:
        """
        Fallback rule-based analysis (if Claude API unavailable).

        Args:
            ml_scores: ML predictions
            astrology_scores: Astrology scores
            partner_ml_scores: Partner scores (if compatibility)

        Returns:
            AIAnalysisSection with rule-based text
        """
        logger.info("Using fallback rule-based analysis")

        avg_ml_score = round(sum(box.score for box in ml_scores.values()) / len(ml_scores), 1)
        overall_strength = round(astrology_scores.get("overall_strength", 50.0), 1)
        guna_milan = int(astrology_scores.get("guna_milan_total", 0))

        # Summary
        if partner_ml_scores:
            summary = f"Compatibility: {guna_milan}/36 points. ML predicts {avg_ml_score}/100 harmony."
        else:
            summary = f"Chart strength: {overall_strength}/100. ML predictions average {avg_ml_score}/100."

        # Insights
        insights = []
        for score_name, score_box in ml_scores.items():
            if score_box.score > 75:
                insights.append(f"Strong {score_name}: {score_box.score:.1f}/100")
            elif score_box.score < 50:
                insights.append(f"Attention needed in {score_name}: {score_box.score:.1f}/100")

        if astrology_scores.get("overall_strength", 0) > 70:
            insights.append(f"Strong planetary positions: {astrology_scores['overall_strength']:.1f}/100")

        # Recommendations
        recommendations = []
        if avg_ml_score < 60:
            recommendations.append("Focus on areas scoring below 60")
        if guna_milan < 18 and guna_milan > 0:
            recommendations.append("Guna Milan below 18 - consider consultation")
        if not recommendations:
            recommendations.append("Maintain current positive trajectory")

        return AIAnalysisSection(
            summary=summary,
            detailed_insights=insights if insights else ["Analysis complete"],
            recommendations=recommendations
        )

    def generate_analysis(
        self,
        ml_scores: Dict[str, MLScoreBox],
        astrology_scores: Dict[str, float],
        context: str = "general",
        partner_ml_scores: Optional[Dict[str, MLScoreBox]] = None
    ) -> Tuple[AIAnalysisSection, Dict[str, Any]]:
        """
        Generate AI analysis using Claude API.

        Token usage: ~500 tokens per request (optimized)

        Args:
            ml_scores: ML predictions
            astrology_scores: Astrology scores
            context: Analysis context
            partner_ml_scores: Partner scores (if compatibility)

        Returns:
            Tuple of (AIAnalysisSection, metadata)
            Metadata includes token counts and cache status
        """
        # Create minimal context
        context_data = self._create_minimal_context(
            ml_scores, astrology_scores, partner_ml_scores, context
        )
        context_json = json.dumps(context_data, indent=2)

        # Check cache
        cache_key = self._hash_context(context_data)
        if self.cache_enabled and cache_key in self.cache:
            logger.debug("Cache hit for analysis context")
            return self.cache[cache_key], {
                "cache_hit": True,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0,
                "model": self.model_name,
                "fallback": False
            }

        # If no Claude API, use fallback
        if not self.client:
            logger.warning("Claude API not configured - using fallback analysis")
            analysis = self._generate_analysis_fallback(
                ml_scores, astrology_scores, partner_ml_scores
            )
            if self.cache_enabled:
                self.cache[cache_key] = analysis
            return analysis, {
                "cache_hit": False,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0,
                "model": self.model_name,
                "fallback": True
            }

        start_time = time.time()

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                system=self.SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze this astrology/ML data and provide insights:

{context_json}

Provide response as JSON only, no markdown or extra text."""
                    }
                ]
            )

            # Extract tokens
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            request_duration_ms = (time.time() - start_time) * 1000

            # Parse response
            response_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            response_json = json.loads(response_text)

            # Create analysis section
            analysis = AIAnalysisSection(
                summary=response_json.get("summary", "Analysis complete"),
                detailed_insights=response_json.get("detailed_insights", []),
                recommendations=response_json.get("recommendations", [])
            )

            # Cache result
            if self.cache_enabled:
                self.cache[cache_key] = analysis

            # Record token usage
            record_token_usage(
                endpoint="/api/ai-analysis",
                model=TokenModel.CLAUDE_HAIKU_4_5,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_hit=False,
                request_duration_ms=request_duration_ms
            )

            logger.info(
                f"LLM analysis generated: {input_tokens} input tokens, "
                f"{output_tokens} output tokens, {request_duration_ms:.0f}ms"
            )

            return analysis, {
                "cache_hit": False,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost_usd": self._calculate_cost(input_tokens, output_tokens),
                "request_duration_ms": request_duration_ms,
                "model": self.model_name
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            analysis = self._generate_analysis_fallback(
                ml_scores, astrology_scores, partner_ml_scores
            )
            return analysis, {
                "cache_hit": False,
                "error": "JSON parse error",
                "fallback": True,
                "model": self.model_name
            }

        except (APIError, APIConnectionError) as e:
            logger.error(f"Claude API error: {e}")
            analysis = self._generate_analysis_fallback(
                ml_scores, astrology_scores, partner_ml_scores
            )
            return analysis, {
                "cache_hit": False,
                "error": str(e),
                "fallback": True,
                "model": self.model_name
            }

        except Exception as e:
            logger.error(f"Unexpected error in LLM analysis: {e}")
            analysis = self._generate_analysis_fallback(
                ml_scores, astrology_scores, partner_ml_scores
            )
            return analysis, {
                "cache_hit": False,
                "error": str(e),
                "fallback": True,
                "model": self.model_name
            }

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD for token usage."""
        # Claude 4.5 Haiku: $1 per 1M input, $5 per 1M output
        input_cost = (input_tokens / 1_000_000) * 1.0
        output_cost = (output_tokens / 1_000_000) * 5.0
        return round(input_cost + output_cost, 6)

# Global singleton instance
_llm_service_instance: Optional[LLMAnalysisService] = None


def get_llm_service(api_key: Optional[str] = None, force_new: bool = False) -> LLMAnalysisService:
    """Get or create the global LLM service instance."""
    global _llm_service_instance
    if _llm_service_instance is None or force_new:
        _llm_service_instance = LLMAnalysisService(api_key=api_key)
    return _llm_service_instance
