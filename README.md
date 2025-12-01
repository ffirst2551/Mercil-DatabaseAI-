# 🏥 Mercil - AI-Powered Community Resource Discovery Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent full-stack application that helps users discover community resources (hospitals, schools, temples, markets) using AI-powered semantic search and geospatial queries.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Team](#-team)

---

## 🎯 Overview

Mercil is a modern web application that combines:
- **AI Semantic Search**: Find resources using natural language queries
- **Geospatial Intelligence**: Location-aware search with PostGIS
- **Conversational AI**: Chat interface powered by Ollama LLM
- **Thai Language Support**: Full support for Thai NLP with pythainlp

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 15+ with extensions:
  - `pgvector` - Vector similarity search
  - `PostGIS` - Geospatial queries
- **AI/ML**:
  - `sentence-transformers` - Text embeddings (384-dim vectors)
  - `Ollama` - Local LLM (Llama 2)
  - `LangChain` - LLM orchestration
- **NLP**:
  - `spaCy` - English NLP
  - `pythainlp` - Thai language processing

### Geocoding
- `geopy` with Nominatim geocoder

### Infrastructure
- Docker & Docker Compose
- Async operations with SQLAlchemy 2.0

---

## ✨ Features

### Module 1: Data Foundation ✅
- [x] PostgreSQL setup with pgvector & PostGIS
- [x] Automatic data loading from JSON
- [x] Text embedding generation (384-dim)
- [x] Address geocoding to lat/lon
- [x] Vector similarity search
- [x] Spatial indexing for fast geo-queries

### Module 2: API Development (Coming Soon)
- [ ] RESTful API endpoints
- [ ] Semantic search API
- [ ] Geospatial query API
- [ ] Authentication & authorization
- [ ] Rate limiting

### Module 3: AI Integration (Coming Soon)
- [ ] Chat interface with Ollama
- [ ] Context-aware responses
- [ ] Thai language processing
- [ ] Multi-turn conversations

### Module 4: Frontend (Coming Soon)
- [ ] React-based web interface
- [ ] Interactive map visualization
- [ ] Real-time chat UI
- [ ] Mobile-responsive design

---

## 🏗 Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│      FastAPI Backend        │
│  ┌─────────┬─────────────┐  │
│  │ REST    │  WebSocket  │  │
│  │ API     │  Chat       │  │
│  └────┬────┴──────┬──────┘  │
│       │           │          │
│  ┌────▼───────────▼──────┐  │
│  │   Business Logic      │  │
│  │  - Search Engine      │  │
│  │  - NLP Processing     │  │
│  │  - Geo Calculator     │  │
│  └────┬──────────┬────────┘ │
└───────┼──────────┼──────────┘
        │          │
   ┌────▼────┐ ┌──▼────────┐
   │ PostGIS │ │  Ollama   │
   │ +Vector │ │   LLM     │
   │   DB    │ │  (Local)  │
   └─────────┘ └───────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://www.docker.com/products/docker-desktop))
- **Git** ([Download](https://git-scm.com/downloads))

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/ffirst2551/Mercil-DatabaseAI-.git
cd Mercil-DatabaseAI-
```

#### 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Download NLP Models

```bash
# English model
python -m spacy download en_core_web_sm

# Thai language data
python -m pythainlp download-data
```

#### 4. Setup Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your favorite editor
```

#### 5. Start Database

```bash
# Start PostgreSQL with pgvector & PostGIS
docker-compose up -d

# Verify database is running
docker-compose ps
```

Expected output:
```
NAME                IMAGE                    STATUS
mercil_postgres     ankane/pgvector:latest   Up 10 seconds (healthy)
```

#### 6. Load Sample Data

```bash
# The assets_rows.json file contains 15 sample locations
python data_loader.py
```

Expected output:
```
🚀 Starting Mercil Data Loader...
✅ Database initialized successfully!
📂 Loaded 15 assets from assets_rows.json
✅ [1/15] Inserted: โรงพยาบาลจุฬาลงกรณ์
✅ [2/15] Inserted: โรงพยาบาลรามาธิบดี
...
🎉 Successfully loaded 15 assets!

🔍 Testing similarity search...
Top 3 similar assets:
- โรงพยาบาลจุฬาลงกรณ์ (similarity: 0.842)
- โรงพยาบาลรามาธิบดี (similarity: 0.831)
- โรงพยาบาลศิริราช (similarity: 0.824)
```

---

## 📂 Project Structure

```
Mercil-DatabaseAI-/
│
├── 📄 data_loader.py          # Main data loading script
├── 📄 requirements.txt        # Python dependencies
├── 📄 docker-compose.yml      # Database setup
├── 📄 init.sql               # PostGIS initialization
├── 📄 .env.example           # Environment template
├── 📄 .env                   # Environment config (create from .env.example)
├── 📄 assets_rows.json       # Sample data (15 locations)
├── 📄 README.md              # This file
├── 📄 .gitignore             # Git ignore rules
│
├── 📁 api/                   # (Coming soon) FastAPI routes
│   ├── __init__.py
│   ├── search.py
│   ├── chat.py
│   └── geo.py
│
├── 📁 models/                # (Coming soon) Database models
│   ├── __init__.py
│   └── asset.py
│
├── 📁 services/              # (Coming soon) Business logic
│   ├── __init__.py
│   ├── search_service.py
│   ├── chat_service.py
│   └── geo_service.py
│
└── 📁 tests/                 # (Coming soon) Unit tests
    ├── __init__.py
    └── test_search.py
```

---

## 📊 Database Schema

### `assets` Table

```sql
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,                    -- Asset name (e.g., "โรงพยาบาลจุฬาฯ")
    description TEXT,                      -- Detailed description
    address TEXT,                          -- Full address
    category TEXT,                         -- hospital, school, temple, etc.
    location GEOGRAPHY(POINT, 4326),       -- PostGIS geography (lat/lon)
    embedding vector(384),                 -- pgvector for semantic search
    metadata JSONB,                        -- Additional data (phone, website, etc.)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX assets_embedding_idx ON assets 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX assets_location_idx ON assets USING GIST (location);
```

### Sample Data Categories

- `hospital` - โรงพยาบาล (3 samples)
- `school` - โรงเรียน (3 samples)
- `temple` - วัด (2 samples)
- `shopping_mall` - ห้างสรรพสินค้า (2 samples)
- `park` - สวนสาธารณะ (2 samples)
- `transit` - สถานีขนส่ง (2 samples)
- `market` - ตลาด (1 sample)

---

## 🔍 API Documentation

### Search API (Coming in Module 2)

#### Semantic Search
```http
GET /api/v1/search?query=โรงพยาบาลใกล้ฉัน&limit=5
```

Response:
```json
{
  "results": [
    {
      "id": 1,
      "name": "โรงพยาบาลจุฬาลงกรณ์",
      "description": "โรงพยาบาลมหาวิทยาลัย...",
      "address": "1873 ถนนพระรามที่ 4...",
      "category": "hospital",
      "location": {"lat": 13.7308, "lon": 100.5318},
      "similarity": 0.842,
      "distance_km": 2.5
    }
  ],
  "total": 5,
  "query_time_ms": 23
}
```

#### Geospatial Search
```http
GET /api/v1/search/nearby?lat=13.7563&lon=100.5018&radius_km=5
```

### Chat API (Coming in Module 3)

```http
POST /api/v1/chat
Content-Type: application/json

{
  "message": "หาโรงพยาบาลที่รักษาโรคหัวใจ",
  "conversation_id": "uuid-here"
}
```

---

## 💻 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Database Management

```bash
# Access PostgreSQL shell
docker exec -it mercil_postgres psql -U mercil_user -d mercil_db

# View all assets
SELECT name, category FROM assets;

# Test vector search
SELECT name, 
       1 - (embedding <=> '[0.1, 0.2, ...]'::vector) as similarity
FROM assets
ORDER BY similarity DESC
LIMIT 5;

# Test spatial query (find within 5km of point)
SELECT name, 
       ST_Distance(location, ST_GeogFromText('POINT(100.5 13.75)')) / 1000 as distance_km
FROM assets
WHERE ST_DWithin(location, ST_GeogFromText('POINT(100.5 13.75)'), 5000)
ORDER BY distance_km;
```

### Adding New Data

Edit `assets_rows.json` and add your data:

```json
{
  "name": "Your Location Name",
  "description": "Detailed description here",
  "address": "Full address with province",
  "category": "hospital|school|temple|park|etc",
  "phone": "02-xxx-xxxx",
  "website": "https://example.com"
}
```

Then reload:
```bash
python data_loader.py
```

---

## 🐛 Troubleshooting

### Database Connection Failed

```bash
# Check if container is running
docker-compose ps

# View logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# If port 5432 is in use, edit docker-compose.yml:
ports:
  - "5433:5432"  # Use different port

# Update DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://mercil_user:mercil_password@localhost:5433/mercil_db
```

### Geocoding Rate Limit

The script includes 1-second delays between requests. For large datasets:
- Use a paid geocoding service (Google Maps, Mapbox)
- Cache geocoded results
- Process in batches

### Python Package Installation Errors

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, install individually
pip install sentence-transformers==2.3.1
```

### Thai Language Model Download

```bash
# If pythainlp fails to download
python -c "import pythainlp; pythainlp.corpus.download('thai2fit_wv')"
python -c "import pythainlp; pythainlp.corpus.download('thai2vec')"
```

---

## 🚢 Deployment

### Docker Production Build

```bash
# Build production image
docker build -t mercil-backend:latest .

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/mercil_prod
DEBUG=False
SECRET_KEY=use-strong-random-key-here
OLLAMA_BASE_URL=http://ollama:11434
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints
- Write docstrings for functions
- Add tests for new features

---

## 👥 Team

**Trio Team - Full Stack Developers**

- **Project Lead**: [Your Name]
- **Backend**: [Backend Developer]
- **Frontend**: [Frontend Developer]
- **Database**: [Database Engineer]

### GitHub Repository
- Main: https://github.com/trio-krittapas/Mercil-backend
- Database AI: https://github.com/ffirst2551/Mercil-DatabaseAI-

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity search
- [PostGIS](https://postgis.net/) - Spatial database
- [Sentence Transformers](https://www.sbert.net/) - Text embeddings
- [Ollama](https://ollama.ai/) - Local LLM inference
- [pythainlp](https://github.com/PyThaiNLP/pythainlp) - Thai NLP

---

## 📞 Support

If you have any questions or issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search [existing issues](https://github.com/ffirst2551/Mercil-DatabaseAI-/issues)
3. Create a [new issue](https://github.com/ffirst2551/Mercil-DatabaseAI-/issues/new)

---

## 🗺 Roadmap

### Q1 2024
- [x] Module 1: Data Foundation
- [ ] Module 2: API Development
- [ ] Module 3: AI Integration

### Q2 2024
- [ ] Module 4: Frontend Development
- [ ] Production deployment
- [ ] Mobile app (React Native)

---

<div align="center">

**Built with ❤️ in Thailand**

[⬆ Back to Top](#-mercil---ai-powered-community-resource-discovery-platform)

</div>
