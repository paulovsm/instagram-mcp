# Instagram MCP Server

An MCP (Model Context Protocol) server for interacting with the Instagram Business API, providing tools for image uploads, post management, and account information.

## 📋 Features

- **Image uploads**: Upload images to Instagram with or without captions
- **Carousel posts**: Create posts with multiple images
- **Media publishing**: Publish previously uploaded media containers
- **Account information**: Get account data like followers and media count
- **Recent media**: Retrieve recent posts from the account
- **Token refresh**: Update long-lived access tokens

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/paulovsm/instagram-mcp
cd instagram-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit the `.env` file with your Instagram credentials:
```properties
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id_here
BEARER_TOKEN=your_secure_bearer_token_here
HOST_URL=graph.facebook.com
LATEST_API_VERSION=v22.0
```

**⚠️ Security Note**: The `BEARER_TOKEN` is required for API authentication. Generate a secure random token (minimum 32 characters).

## 🔧 Instagram Setup

To use this server, you need:

1. **Instagram Business Account**: Convert your personal account to a business account
2. **Facebook App**: Create an app in the Facebook Developer Portal
3. **Access Token**: Generate a long-lived access token
4. **Account ID**: Get your Instagram Business account ID

### Detailed steps:

1. Go to the [Facebook Developer Portal](https://developers.facebook.com/)
2. Create a new app
3. Add the "Instagram Basic Display" or "Instagram Graph API" product
4. Configure the necessary permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`

## 🏃‍♂️ Usage

### Starting the server

```bash
python instagram-mcp.py --host 0.0.0.0 --port 8080
```

Optional parameters:
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`: Port to listen on (default: 8080)

### Available endpoints

- **SSE Endpoint**: `http://localhost:8080/sse`
- **Messages Endpoint**: `http://localhost:8080/messages/`

### 🔐 Authentication

All requests to the server require Bearer token authentication. Include the authorization header:

```bash
Authorization: Bearer your_secure_bearer_token_here
```

Example with curl:
```bash
curl -H "Authorization: Bearer your_secure_bearer_token_here" \
     -H "Content-Type: application/json" \
     http://localhost:8080/sse
```

### 🔐 Generating Secure Bearer Tokens

Use the included token generator to create a secure Bearer token:

```bash
python generate_token.py
```

This will generate three different types of secure tokens. Copy one to your `.env` file.

### 🧪 Testing Authentication

Test your Bearer token authentication:

```bash
python test_auth.py
```

This script will test authentication with invalid and valid tokens.

## 🛠️ Available Tools

### 1. `refresh_instagram_access_token()`
Refreshes the Instagram long-lived access token.

### 2. `upload_image_without_caption(image_url: str)`
Uploads an image without caption.
- **image_url**: Publicly accessible URL of the image

### 3. `upload_image_with_caption(image_url: str, caption: str)`
Uploads an image with caption.
- **image_url**: Publicly accessible URL of the image
- **caption**: Caption for the image

### 4. `upload_carousel_post(caption: str, children_ids: list[str])`
Creates a carousel post with multiple images.
- **caption**: Caption for the carousel
- **children_ids**: List of media container IDs

### 5. `publish_media_container(media_id: str)`
Publishes a previously uploaded media container.
- **media_id**: Media container ID

### 6. `get_instagram_account_info()`
Gets Instagram account information (type, media count, followers).

### 7. `get_recent_media(limit: int = 10)`
Retrieves recent posts from the account.
- **limit**: Number of posts to retrieve (default: 10)

## 📝 Usage Example

```python
# Example workflow for posting an image
# 1. Upload the image
upload_image_with_caption("https://example.com/image.jpg", "My new photo!")

# 2. Publish the container (using the returned media_id)
publish_media_container("123456789")

# 3. Check account information
get_instagram_account_info()
```

## 🔍 Project Structure

```
instagram-mcp/
├── instagram-mcp.py      # Main MCP server
├── requirements.txt      # Python dependencies
├── generate_token.py     # Bearer token generator
├── test_auth.py         # Authentication test script
├── .env                 # Environment variables
├── .env.example         # Environment variables template
└── README.md           # Documentation
```

## 📦 Dependencies

- **mcp[sse]**: MCP framework with SSE support
- **fastapi**: Web framework for APIs
- **uvicorn**: ASGI server
- **starlette**: Lightweight web framework
- **httpx**: Asynchronous HTTP client
- **python-dotenv**: Environment variable loading

## ⚠️ Limitations and Considerations

1. **Security**: Bearer token authentication is required for all API endpoints
2. **Rate Limits**: Instagram API has rate limits. Monitor your usage
3. **Tokens**: Access tokens have expiration dates. Use the refresh tool
4. **Image Formats**: Only supported formats (JPEG, PNG)
5. **File Size**: Respect Instagram API size limits
6. **Public URLs**: Images must be hosted on publicly accessible URLs

## 🐛 Troubleshooting

### Authentication Error
```bash
# Check if the Bearer token is correct in .env
# Ensure all requests include the Authorization header
curl -H "Authorization: Bearer your_token" http://localhost:8080/sse
```

### Invalid Token Error
```bash
# Check if the Instagram token is correct in .env
# Use the refresh tool if necessary
refresh_instagram_access_token()
```

### Image Upload Error
- Check if the image URL is publicly accessible
- Confirm the image format (JPEG/PNG)
- Verify the image size

### Connection Error
- Check your internet connection
- Confirm if Instagram API is working

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions, open an issue in the project repository.