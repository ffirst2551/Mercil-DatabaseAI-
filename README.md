# Mercil Backend - Module 1: Data Foundation

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### 2. Clone & Setup
```bash
# Clone repository
git clone https://github.com/trio-krittapas/Mercil-backend.git
cd Mercil-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Thai NLP model
python -m spacy download en_core_web_sm
python -m pythainlp download-data

# Setup environment
cp .env.example .env
```

### 3. Start Database
```bash
# Start PostgreSQL with pgvector & PostGIS
docker-compose up -d

# Verify database is running
docker-compose ps
```

### 4. Load Data
```bash
# Run data loader
python data_loader.py
```

## 📊 Database Schema
```sql
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    category TEXT,
    location GEOGRAPHY(POINT, 4326),
    embedding vector(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Features

✅ PostgreSQL with pgvector & PostGIS  
✅ Sentence transformers for embeddings  
✅ Geocoding with geopy  
✅ Vector similarity search  
✅ Async operations  

## 🐛 Troubleshooting

**Database connection error:**
```bash
docker-compose logs postgres
docker-compose restart postgres
```

## 📄 License

MIT License

---

Built with ❤️ by Trio Team
