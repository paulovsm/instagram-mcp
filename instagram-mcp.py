"""
Instagram MCP Server with SSE Transport
Provides Instagram operations as MCP tools over SSE transport instead of stdio.
"""
import requests
import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server for Instagram tools (SSE)
mcp = FastMCP("Instagram MCP Server")

# Instagram API Configuration
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
HOST_URL = os.getenv("HOST_URL", "graph.facebook.com")
LATEST_API_VERSION = os.getenv("LATEST_API_VERSION", "v21.0")

# Bearer token for API authentication
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Validate required environment variables
if not INSTAGRAM_ACCESS_TOKEN:
    raise ValueError("INSTAGRAM_ACCESS_TOKEN environment variable is required")
if not INSTAGRAM_ACCOUNT_ID:
    raise ValueError("INSTAGRAM_ACCOUNT_ID environment variable is required")
if not BEARER_TOKEN:
    raise ValueError("BEARER_TOKEN environment variable is required")

async def make_instagram_request(url: str, method: str = "GET", data: dict = None, json_data: dict = None) -> dict[str, Any] | None:
    """Make a request to the Instagram API with proper error handling."""
    headers = {
        "User-Agent": "Instagram-MCP-Server/1.0",
        "Accept": "application/json"
    }
    
    if json_data:
        headers["Content-Type"] = "application/json"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method == "POST":
                if json_data:
                    response = await client.post(url, headers=headers, json=json_data, timeout=30.0)
                else:
                    response = await client.post(url, headers=headers, data=data, timeout=30.0)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

@mcp.tool()
async def refresh_instagram_access_token() -> str:
    """Refresh the long-lived Instagram access token.
    
    This tool requests a new long-lived access token for the Instagram account, 
    extending its validity period. No parameters are required.
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/refresh_access_token?grant_type=ig_refresh_token&access_token={INSTAGRAM_ACCESS_TOKEN}"
    
    result = await make_instagram_request(url)
    
    if result and "error" not in result:
        return f"Access token refreshed successfully: {result}"
    else:
        return f"Failed to refresh access token: {result}"

@mcp.tool()
async def upload_image_without_caption(image_url: str) -> str:
    """Upload an image to Instagram without caption and return the media container ID.
    
    Args:
        image_url: The publicly accessible URL of the image to upload
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    
    json_data = {
        "image_url": image_url,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    result = await make_instagram_request(url, method="POST", json_data=json_data)
    
    if result and "id" in result:
        return f"Image uploaded successfully. Media ID: {result['id']}"
    else:
        return f"Failed to upload image: {result}"

@mcp.tool()
async def upload_image_with_caption(image_url: str, caption: str) -> str:
    """Upload an image to Instagram with a caption and return the media container ID.
    
    Args:
        image_url: The publicly accessible URL of the image to upload
        caption: The caption to attach to the image
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    result = await make_instagram_request(url, method="POST", data=data)
    
    if result and "id" in result:
        return f"Image with caption uploaded successfully. Media ID: {result['id']}"
    else:
        return f"Failed to upload image with caption: {result}"

@mcp.tool()
async def upload_carousel_post(caption: str, children_ids: list[str]) -> str:
    """Upload a carousel post (multiple images) to Instagram with a caption.
    
    Args:
        caption: The caption for the carousel post
        children_ids: List of media container IDs to include in the carousel
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    
    json_data = {
        "caption": caption,
        "media_type": "CAROUSEL",
        "children": children_ids,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    result = await make_instagram_request(url, method="POST", json_data=json_data)
    
    if result and "id" in result:
        return f"Carousel post uploaded successfully. Media ID: {result['id']}"
    else:
        return f"Failed to upload carousel post: {result}"

@mcp.tool()
async def publish_media_container(media_id: str) -> str:
    """Publish a previously uploaded Instagram media container.
    
    Args:
        media_id: The media container ID to publish
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    
    data = {
        "creation_id": media_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    result = await make_instagram_request(url, method="POST", data=data)
    
    if result and "id" in result:
        return f"Media published successfully. Post ID: {result['id']}"
    else:
        return f"Failed to publish media: {result}"

@mcp.tool()
async def get_instagram_account_info() -> str:
    """Get Instagram account information including follower count and media count."""
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}?fields=account_type,media_count,followers_count&access_token={INSTAGRAM_ACCESS_TOKEN}"
    
    result = await make_instagram_request(url)
    
    if result and "error" not in result:
        return f"Account Info: {result}"
    else:
        return f"Failed to get account info: {result}"

@mcp.tool()
async def get_recent_media(limit: int = 10) -> str:
    """Get recent Instagram media posts.
    
    Args:
        limit: Number of recent posts to retrieve (default: 10)
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media?fields=id,caption,media_type,media_url,timestamp,permalink&limit={limit}&access_token={INSTAGRAM_ACCESS_TOKEN}"
    
    result = await make_instagram_request(url)
    
    if result and "data" in result:
        return f"Recent Media: {result['data']}"
    else:
        return f"Failed to get recent media: {result}"

class BearerTokenMiddleware(BaseHTTPMiddleware):
    """Middleware to validate Bearer token authentication."""
    
    def __init__(self, app, bearer_token: str):
        super().__init__(app)
        self.bearer_token = bearer_token
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for health check endpoints (if any)
        if request.url.path in ["/health", "/ping"]:
            return await call_next(request)
        
        # Get Authorization header
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"error": "Missing Authorization header"}
            )
        
        # Check if it's a Bearer token
        if not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid authorization format. Use 'Bearer <token>'"}
            )
        
        # Extract and validate token
        token = authorization[7:]  # Remove "Bearer " prefix
        if token != self.bearer_token:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid Bearer token"}
            )
        
        # Token is valid, continue with the request
        return await call_next(request)

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the provided MCP server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    # Create Starlette app with routes
    app = Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )
    
    # Add Bearer token authentication middleware
    app.add_middleware(BearerTokenMiddleware, bearer_token=BEARER_TOKEN)
    
    return app

if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse
    
    parser = argparse.ArgumentParser(description='Run Instagram MCP SSE-based server')
    parser.add_argument('--host', default=os.getenv('HOST', '0.0.0.0'), help='Host to bind to')
    parser.add_argument('--port', type=int, default=int(os.getenv('PORT', '8080')), help='Port to listen on')
    args = parser.parse_args()

    print(f"Starting Instagram MCP Server with SSE transport on {args.host}:{args.port}")
    print("Environment variables loaded from .env file")
    print("🔒 Bearer token authentication enabled")
    print("Available tools:")
    print("- refresh_instagram_access_token")
    print("- upload_image_without_caption")
    print("- upload_image_with_caption") 
    print("- upload_carousel_post")
    print("- publish_media_container")
    print("- get_instagram_account_info")
    print("- get_recent_media")
    print()
    print("SSE endpoint: /sse")
    print("Messages endpoint: /messages/")
    print()
    print("⚠️  Authentication required: Include 'Authorization: Bearer <your-token>' header")

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    # Add Bearer token middleware
    starlette_app.add_middleware(BearerTokenMiddleware, bearer_token=BEARER_TOKEN)

    uvicorn.run(starlette_app, host=args.host, port=args.port)