# SnapWave Architecture

```
┌───────────────┐     ┌─────────────┐     ┌─────────────────┐
│  Client Apps  │────▶│ API Gateway │────▶│ Auth Service    │
└───────────────┘     │ (Nginx)     │     └─────────────────┘
                      │             │     ┌─────────────────┐
                      │             │────▶│ Media Service   │
                      │             │     └─────┬───────────┘
                      │             │           │
                      │             │     ┌─────▼───────────┐
                      │             │────▶│ Feed Service    │
                      │             │     └─────────────────┘
                      │             │     ┌─────────────────┐
                      │             │────▶│ Social Service  │
                      └─────────────┘     └─────────────────┘
                            │
                  ┌─────────┴──────────┐
                  │                    │
         ┌────────▼─────────┐  ┌───────▼────────┐
         │ Database Layer   │  │ Storage Layer  │
         │ ┌─────────────┐  │  │ ┌───────────┐  │
         │ │ PostgreSQL  │  │  │ │  MinIO    │  │
         │ │ (Users)     │  │  │ │ (Media)   │  │
         │ └─────────────┘  │  │ └───────────┘  │
         │ ┌─────────────┐  │  └────────────────┘
         │ │ MongoDB     │  │
         │ │ (Social)    │  │
         │ └─────────────┘  │
         │ ┌─────────────┐  │
         │ │ Redis       │  │
         │ │ (Cache)     │  │
         │ └─────────────┘  │
         └──────────────────┘
```

## Service Descriptions

- **API Gateway**: Routes requests to appropriate services
- **Auth Service**: Handles user registration, login, JWT
- **Media Service**: Manages uploads, processing, and delivery
- **Feed Service**: Generates and retrieves user feeds
- **Social Service**: Handles follows, likes, comments
- **Database Layer**: Multiple databases for different data types
- **Storage Layer**: Object storage for media files
