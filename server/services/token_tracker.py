"""
Token Usage Tracking for Claude API Integration

Tracks and reports token usage across LLM API calls for cost monitoring
and optimization.

Author: LLM Integration Team
"""

import logging
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum

logger = logging.getLogger(__name__)


class TokenModel(str, Enum):
    """Supported token models for cost calculation."""
    CLAUDE_SONNET_4_5 = "claude-sonnet-4-5-20250929"
    CLAUDE_HAIKU_4_5 = "claude-haiku-4-5-20251001"
  
@dataclass
class TokenCosts:
    """Token costs for different models (per 1M tokens)."""
    input_cost_per_1m: float  # Cost per 1M input tokens
    output_cost_per_1m: float  # Cost per 1M output tokens

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate total cost in USD."""
        input_cost = (input_tokens / 1_000_000) * self.input_cost_per_1m
        output_cost = (output_tokens / 1_000_000) * self.output_cost_per_1m
        return input_cost + output_cost


# Token pricing (as of 2024-2025)
TOKEN_PRICING = {
    TokenModel.CLAUDE_SONNET_4_5: TokenCosts(
        input_cost_per_1m=3.0,      # $3 per 1M input tokens
        output_cost_per_1m=15.0     # $15 per 1M output tokens
    ),
    TokenModel.CLAUDE_HAIKU_4_5: TokenCosts(
        input_cost_per_1m=1.0,      # $1 per 1M input tokens
        output_cost_per_1m=5.0     # $5 per 1M output tokens
    ),
    
}

@dataclass
class TokenUsage:
    """Record of a single API call's token usage."""
    endpoint: str                    # Which endpoint used the tokens
    model: TokenModel               # Which model was used
    input_tokens: int               # Number of input tokens used
    output_tokens: int              # Number of output tokens used
    total_tokens: int               # Total tokens (sum)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    cache_hit: bool = False         # Whether result was cached
    request_duration_ms: float = 0  # API request duration

    @property
    def cost(self) -> float:
        """Calculate cost of this token usage."""
        pricing = TOKEN_PRICING.get(self.model)
        if not pricing:
            return 0.0
        return pricing.calculate_cost(self.input_tokens, self.output_tokens)

    def to_dict(self) -> Dict:
        """Convert to dictionary for logging/tracking."""
        return {
            "endpoint": self.endpoint,
            "model": self.model.value,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cost_usd": round(self.cost, 6),
            "cache_hit": self.cache_hit,
            "request_duration_ms": self.request_duration_ms,
            "timestamp": self.timestamp.isoformat()
        }


class TokenTracker:
    """
    Centralized token usage tracking for all LLM API calls.

    Maintains metrics for:
    - Total tokens used across all endpoints
    - Cost per endpoint and per model
    - Cache hit rates
    - Request latency
    - Token usage trends
    """

    def __init__(self):
        self.usage_history: List[TokenUsage] = []
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cost = 0.0
        self._cache_hits = 0
        self._cache_misses = 0
        self._endpoint_usage: Dict[str, Dict] = {}

    def record(self, usage: TokenUsage) -> None:
        """Record a token usage event."""
        self.usage_history.append(usage)

        # Update totals
        self._total_input_tokens += usage.input_tokens
        self._total_output_tokens += usage.output_tokens
        self._total_cost += usage.cost

        # Track cache hits
        if usage.cache_hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1

        # Track per-endpoint metrics
        endpoint = usage.endpoint
        if endpoint not in self._endpoint_usage:
            self._endpoint_usage[endpoint] = {
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cost": 0.0,
                "cache_hits": 0,
                "total_duration_ms": 0
            }

        stats = self._endpoint_usage[endpoint]
        stats["calls"] += 1
        stats["input_tokens"] += usage.input_tokens
        stats["output_tokens"] += usage.output_tokens
        stats["cost"] += usage.cost
        if usage.cache_hit:
            stats["cache_hits"] += 1
        stats["total_duration_ms"] += usage.request_duration_ms

        # Log usage
        logger.info(
            f"Token usage recorded: {endpoint} | "
            f"Input: {usage.input_tokens} | Output: {usage.output_tokens} | "
            f"Cost: ${usage.cost:.6f} | Cache: {usage.cache_hit}"
        )

    def get_summary(self) -> Dict:
        """Get overall token usage summary."""
        total_requests = len(self.usage_history)
        avg_input = self._total_input_tokens / total_requests if total_requests > 0 else 0
        avg_output = self._total_output_tokens / total_requests if total_requests > 0 else 0
        cache_hit_rate = self._cache_hits / (self._cache_hits + self._cache_misses) if (self._cache_hits + self._cache_misses) > 0 else 0

        return {
            "total_requests": total_requests,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens": self._total_input_tokens + self._total_output_tokens,
            "total_cost_usd": round(self._total_cost, 6),
            "average_input_tokens": round(avg_input, 1),
            "average_output_tokens": round(avg_output, 1),
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "cache_hit_rate": round(cache_hit_rate, 3),
            "endpoints": self._endpoint_usage
        }

    def get_endpoint_stats(self, endpoint: str) -> Optional[Dict]:
        """Get stats for a specific endpoint."""
        return self._endpoint_usage.get(endpoint)

    def get_cost_estimate(self, projected_requests: int) -> Dict:
        """Estimate cost for projected number of requests."""
        if len(self.usage_history) == 0:
            return {"estimated_cost": 0, "note": "No historical data"}

        avg_cost = self._total_cost / len(self.usage_history)
        estimated_total = avg_cost * projected_requests

        return {
            "average_cost_per_request": round(avg_cost, 6),
            "projected_requests": projected_requests,
            "estimated_total_cost": round(estimated_total, 6)
        }


# Global singleton instance
_tracker_instance: Optional[TokenTracker] = None


def get_token_tracker() -> TokenTracker:
    """Get or create the global token tracker instance."""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = TokenTracker()
    return _tracker_instance


def record_token_usage(
    endpoint: str,
    model: TokenModel,
    input_tokens: int,
    output_tokens: int,
    cache_hit: bool = False,
    request_duration_ms: float = 0
) -> None:
    """
    Convenience function to record token usage.

    Args:
        endpoint: API endpoint that used tokens
        model: Token model used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        cache_hit: Whether result was cached
        request_duration_ms: API request duration
    """
    tracker = get_token_tracker()
    usage = TokenUsage(
        endpoint=endpoint,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        cache_hit=cache_hit,
        request_duration_ms=request_duration_ms
    )
    tracker.record(usage)
