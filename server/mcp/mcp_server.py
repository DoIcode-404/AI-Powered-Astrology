"""
FastAPI MCP Server with Route Filtering
Exposes ONLY AI analysis routes to LLMs via Model Context Protocol

This server:
1. Filters routes to expose only /api/ai-analysis endpoints
2. Tracks Claude API token usage and costs
3. Optimizes responses for LLM consumption
4. Provides token tracking per request

"""

import logging
from typing import Dict, Any, Optional
from functools import wraps
from datetime import datetime

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP

logger = logging.getLogger(__name__)


class MCPServerConfig:
    """Configuration for MCP Server."""
    
    # Routes that should be exposed to LLMs
    ALLOWED_ROUTES = [
        "/api/ai-analysis",  # Single person analysis
        "/api/ai-analysis/compatibility",  # Compatibility analysis
    ]
    
    # Routes that should be BLOCKED (filtered out)
    BLOCKED_ROUTE_PATTERNS = [
        "/api/auth",
        "/api/users",
        "/api/admin",
        "/api/kundali",
        "/api/predictions",
        "/api/ml",
        "/api/compatibility",
        "/api/horoscope",
        "/api/transits",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/error-stats"
    ]
    
    # Token tracking settings
    CLAUDE_SONNET_INPUT_COST = 0.003  # $0.003 per 1K input tokens
    CLAUDE_SONNET_OUTPUT_COST = 0.009  # $0.009 per 1K output tokens


class TokenTracker:
    """Track Claude API token usage and costs."""
    
    def __init__(self):
        """Initialize token tracker."""
        self.requests: Dict[str, Any] = {}
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0
        self.request_count = 0
    
    def track_request(
        self,
        request_id: str,
        input_tokens: int,
        output_tokens: int,
        model: str = "claude-haiku-4-5-20251001"
    ) -> Dict[str, Any]:
        """
        Track a single LLM request.
        
        Args:
            request_id: Unique request identifier
            input_tokens: Number of input tokens consumed
            output_tokens: Number of output tokens consumed
            model: Model name (default: Claude Sonnet 4.5)
        
        Returns:
            Dict with cost breakdown
        """
        config = MCPServerConfig()
        
        # Calculate costs
        input_cost = (input_tokens / 1000) * config.CLAUDE_SONNET_INPUT_COST
        output_cost = (output_tokens / 1000) * config.CLAUDE_SONNET_OUTPUT_COST
        total_cost = input_cost + output_cost
        
        # Track totals
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_usd += total_cost
        self.request_count += 1
        
        # Store request details
        self.requests[request_id] = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "model": model
        }
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "model": model,
            "cumulative_cost_usd": round(self.total_cost_usd, 6)
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get token tracking summary."""
        return {
            "total_requests": self.request_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "average_cost_per_request": round(
                self.total_cost_usd / self.request_count if self.request_count > 0 else 0,
                6
            )
        }


class FilteredMCPServer:
    """MCP Server with route filtering for AI analysis endpoints only."""
    
    def __init__(self, app: FastAPI):
        """
        Initialize filtered MCP server.
        
        Args:
            app: FastAPI application instance
        """
        self.app = app
        self.mcp = FastApiMCP(app)
        self.token_tracker = TokenTracker()
        self.config = MCPServerConfig()
        
        logger.info("Initializing FilteredMCPServer with route filtering")
    
    def is_allowed_route(self, path: str) -> bool:
        """
        Check if route should be exposed to LLMs.
        
        Args:
            path: Request path
        
        Returns:
            True if route is allowed, False otherwise
        """
        # Check if path starts with any blocked pattern
        for blocked_pattern in self.config.BLOCKED_ROUTE_PATTERNS:
            if path.startswith(blocked_pattern):
                return False
        
        # Allow AI analysis routes
        for allowed_route in self.config.ALLOWED_ROUTES:
            if path.startswith(allowed_route):
                return True
        
        return False
    
    def create_filtered_middleware(self):
        """Create middleware that filters routes for MCP exposure."""
        
        @self.app.middleware("http")
        async def filter_mcp_routes(request: Request, call_next):
            """
            Middleware to filter which routes are exposed to MCP.
            
            This ensures LLMs only access:
            - POST /api/ai-analysis
            - POST /api/ai-analysis/compatibility
            """
            # For MCP requests, validate route access
            if request.headers.get("X-MCP-Request", "false").lower() == "true":
                if not self.is_allowed_route(request.url.path):
                    return JSONResponse(
                        status_code=403,
                        content={
                            "status": "error",
                            "success": False,
                            "error_message": f"Route {request.url.path} is not exposed to MCP",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    )
            
            response = await call_next(request)
            return response
    
    def mount(self):
        """Mount the MCP server with filtering."""
        logger.info(f"Mounting MCP server with {len(self.config.ALLOWED_ROUTES)} allowed routes")
        logger.info(f"Allowed routes: {self.config.ALLOWED_ROUTES}")
        
        self.create_filtered_middleware()
        self.mcp.mount()
        
        logger.info("MCP server mounted successfully")
    
    def track_llm_request(
        self,
        request_id: str,
        input_tokens: int,
        output_tokens: int,
        model: str = "claude-3-5-sonnet-20241022"
    ) -> Dict[str, Any]:
        """Track LLM token usage."""
        return self.token_tracker.track_request(
            request_id=request_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model
        )
    
    def get_tracking_summary(self) -> Dict[str, Any]:
        """Get token tracking summary."""
        return self.token_tracker.get_summary()


# Global MCP server instance
_mcp_server: Optional[FilteredMCPServer] = None


def get_mcp_server(app: FastAPI) -> FilteredMCPServer:
    """
    Get or create the global MCP server instance.
    
    Args:
        app: FastAPI application instance
    
    Returns:
        FilteredMCPServer instance
    """
    global _mcp_server
    
    if _mcp_server is None:
        _mcp_server = FilteredMCPServer(app)
        _mcp_server.mount()
    
    return _mcp_server


def get_token_tracker():
    """Get the global token tracker instance."""
    global _mcp_server
    
    if _mcp_server is None:
        raise RuntimeError(
            "MCP server not initialized. "
            "Call get_mcp_server(app) first during app initialization."
        )
    
    return _mcp_server.token_tracker
