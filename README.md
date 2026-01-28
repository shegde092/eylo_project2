# Eylo - Share Sheet Recipe Import

> Import recipes from Instagram directly into Eylo using iOS and Android Share Sheets

## 🎯 Project Overview

This project enables Eylo users to save Instagram recipes (Reels, Posts, Pictures) without leaving the Instagram app. Simply tap "Share" → Select "Eylo" → The recipe is automatically extracted and saved using AI.

### Key Features

- ✅ **Seamless UX**: Share from Instagram → Recipe ready in ~30 seconds
- ✅ **AI-Powered**: Gemini 1.5 Pro extracts ingredients from video + text
- ✅ **Cross-Platform**: Works on both iOS and Android
- ✅ **Async Processing**: "Fire and Forget" - user doesn't wait
- ✅ **Push Notifications**: Alerts when recipe is ready

## 🏗️ Architecture

```
Instagram App → Share Sheet → Eylo Extension → API Gateway → Queue
                                                              ↓
                                                         Worker Process
                                                              ↓
                                              ┌─────────────────────────┐
                                              │ 1. Scrape (Apify)       │
                                              │ 2. Extract AI (Gemini)  │
                                              │ 3. Upload (S3)          │
                                              │ 4. Save (PostgreSQL)    │
                                              │ 5. Notify (FCM)         │
                                              └─────────────────────────┘
                                                              ↓
                                              Push Notification → User's Phone
```

## 📁 Project Structure

```
eylo_project2/
├── infra/                    # Backend (FastAPI + Worker)
│   ├── app/
│   │   ├── main.py          # API endpoints
│   │   ├── worker.py        # Background processor
│   │   └── services/        # Apify, Gemini, S3, FCM
│   ├── docker-compose.yml   # Local development
│   └── README.md            # Backend setup guide
│
├── mobile/
│   ├── ios/                 # iOS Share Extension
│   │   ├── EyloShare/       # Share Extension code
│   │   └── README.md        # iOS setup guide
│   │
│   └── android/             # Android Share Intent
│       ├── app/src/main/    # Share Activity + Worker
│       └── README.md        # Android setup guide
│
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Docker, Python 3.11+
- **iOS**: Xcode 15+, macOS
- **Android**: Android Studio, JDK 17+
- **API Keys**: Apify, Google Gemini AI, AWS S3, Firebase

### 1. Start the Backend

```bash
cd infra

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Verify
curl http://localhost:8000/health
```

See [infra/README.md](infra/README.md) for detailed backend setup.

### 2. Setup iOS (Optional)

```bash
# Open in Xcode
open mobile/ios/Eylo.xcodeproj

# Add Share Extension target (see iOS README)
# Configure App Groups and Keychain Sharing
# Build and run on Simulator or iPhone
```

See [mobile/ios/README.md](mobile/ios/README.md) for detailed iOS setup.

### 3. Setup Android

```bash
# Open in Android Studio
# File → Open → mobile/android

# Download google-services.json from Firebase
# Place in: mobile/android/app/

# Build and run on Emulator or physical device
```

See [mobile/android/README.md](mobile/android/README.md) for detailed Android setup.

## 📱 How It Works

### User Flow

1. **User is in Instagram** viewing a cooking Reel
2. **Taps Share button** → Selects "Eylo" from share sheet
3. **Share Extension opens** → Extracts Instagram URL
4. **Sends to API** → Receives "Recipe importing!" message
5. **Extension closes** → User back in Instagram (~2 seconds total)
6. **Backend processes** (30-40 seconds):
   - Scrapes video + caption from Instagram
   - AI extracts recipe (ingredients, steps, times)
   - Uploads media to S3
   - Saves to database
7. **Push notification arrives** → "Recipe Ready! 🍝"
8. **User taps notification** → Eylo app opens to recipe detail

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API** | FastAPI | HTTP endpoints |
| **Queue** | Redis | Job queue |
| **Worker** | Python asyncio | Background processing |
| **Scraper** | Apify | Instagram content extraction |
| **AI** | Gemini 1.5 Pro | Recipe extraction from video |
| **Storage** | AWS S3 | Media files |
| **Database** | PostgreSQL (JSONB) | Recipe data |
| **Notifications** | Firebase FCM | Push alerts |
| **iOS** | Swift, Share Extension | Share Sheet integration |
| **Android** | Kotlin, WorkManager | Share Intent handling |

## 🧪 Testing

### Backend

```bash
cd infra

# Start services
docker-compose up -d

# Test API endpoint
curl -X POST http://localhost:8000/import/recipe \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/ABC123/"}'

# Check worker logs
docker-compose logs -f worker
```

### iOS (Requires physical device for full test)

1. Build app in Xcode
2. Open Safari → Navigate to Instagram Reel URL
3. Tap Share → Select "Eylo"
4. Verify Toast message appears
5. Wait for push notification (physical device only)

### Android

1. Build app in Android Studio
2. Install on emulator/device
3. Open Instagram app
4. Share a Reel → Select "Save to Eylo"
5. Verify Toast message
6. Check WorkManager status (see Android README)
7. Wait for push notification

## 📊 Current Status

### ✅ Completed

- [x] Backend API Gateway
- [x] Background Worker with retry logic
- [x] Apify Instagram scraper integration
- [x] Gemini 1.5 Pro AI extraction
- [x] S3 media upload
- [x] PostgreSQL JSONB schema
- [x] Redis job queue
- [x] Firebase Cloud Messaging
- [x] iOS Share Extension
- [x] Android Share Intent
- [x] Android WorkManager
- [x] Comprehensive documentation

### 🚧 TODO (Integration with Main App)

- [ ] Implement authentication (save tokens)
- [ ] Register for push notifications
- [ ] Handle deep links (`eylo://recipe/{id}`)
- [ ] Create Recipe Detail View
- [ ] Add recipe list/search UI
- [ ] Deploy backend to production
- [ ] Submit to App Store / Play Store

## 💰 Cost Estimates

**Monthly costs** (at 1,000 recipes/month):

- Apify Instagram Scraper: ~$10
- Gemini 1.5 Pro API: ~$40
- AWS S3 Storage: ~$1
- AWS EC2/RDS: ~$30
- Firebase FCM: Free
- **Total: ~$81/month**

At 10,000 recipes/month: **~$500/month**

## 📚 Documentation

- [Implementation Plan](/.gemini/antigravity/brain/295434be-6385-464e-84a1-cdcea3292d19/implementation_plan.md) - Detailed architecture and design decisions
- [Walkthrough](/.gemini/antigravity/brain/295434be-6385-464e-84a1-cdcea3292d19/walkthrough.md) - Implementation summary and next steps
- [Task Breakdown](/.gemini/antigravity/brain/295434be-6385-464e-84a1-cdcea3292d19/task.md) - Development checklist

Component-specific:
- [Backend README](infra/README.md)
- [iOS README](mobile/ios/README.md)
- [Android README](mobile/android/README.md)

## 🔧 Configuration

### Required API Keys

1. **Apify**: [console.apify.com](https://console.apify.com/)
2. **Google Gemini AI**: [aistudio.google.com](https://aistudio.google.com/app/apikey)
3. **AWS S3**: Configure via AWS Console
4. **Firebase**: [console.firebase.google.com](https://console.firebase.google.com/)

### Environment Variables

Copy `infra/.env.example` to `infra/.env` and fill in:

```env
APIFY_API_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
AWS_S3_BUCKET=your_bucket_name
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
FCM_SERVER_KEY=your_fcm_key
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## 🤝 Contributing

### Development Workflow

1. **Backend changes**: Edit files in `infra/app/`
   - Restart services: `docker-compose restart api worker`
   - View logs: `docker-compose logs -f`

2. **iOS changes**: Edit in Xcode
   - Hot reload supported in Simulator
   - Rebuild for physical device testing

3. **Android changes**: Edit in Android Studio
   - Instant Run supported
   - Use `adb logcat` for debugging

## 🐛 Troubleshooting

### Backend

**Worker not processing jobs?**
```bash
docker exec -it eylo_redis redis-cli
> LLEN eylo:recipe_import
```

**Apify scraping fails?**
- Check API token validity
- Instagram layout may have changed
- Review Apify actor logs

### iOS

**Share Extension not appearing?**
- Check Info.plist configuration
- Ensure extension is in build phases
- Restart device

**"Please log in" error?**
- Main app must save auth token to Keychain
- Verify App Group configuration

### Android

**WorkManager not running?**
- Check device battery settings
- Review network constraints
- Use: `adb logcat | grep RecipeImportWorker`

**No push notification?**
- Verify FCM token saved
- Check Firebase Console logs
- Ensure notification permission granted

## 📞 Support

For implementation questions, see the call agenda in [walkthrough.md](/.gemini/antigravity/brain/295434be-6385-464e-84a1-cdcea3292d19/walkthrough.md).

## 📝 License

MIT

---

**Built with ❤️ for Eylo**
