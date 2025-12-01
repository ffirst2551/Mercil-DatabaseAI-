-- Mercil Database Schema
-- Version: 2.0
-- Description: Schema for disaster relief asset management with AI search

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Main assets table
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location_type VARCHAR(100),
    description TEXT,
    district VARCHAR(100),
    province VARCHAR(100),
    contact_info JSONB,
    location GEOGRAPHY(POINT, 4326),  -- PostGIS geography type
    embedding vector(768),  -- Sentence transformer embeddings
    
    -- New fields
    images JSONB DEFAULT '[]'::jsonb,  -- Array of image objects
    tags TEXT[] DEFAULT ARRAY[]::text[],  -- Searchable tags
    image_embeddings vector(768),  -- Image embeddings for similarity search
    search_vector tsvector,  -- Full-text search vector
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',  -- active, inactive, archived
    verified BOOLEAN DEFAULT false,
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'archived'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_location ON assets USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_embedding ON assets USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_location_type ON assets(location_type);
CREATE INDEX IF NOT EXISTS idx_district ON assets(district);
CREATE INDEX IF NOT EXISTS idx_province ON assets(province);
CREATE INDEX IF NOT EXISTS idx_status ON assets(status);

-- New indexes
CREATE INDEX IF NOT EXISTS idx_tags ON assets USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_images ON assets USING GIN(images);
CREATE INDEX IF NOT EXISTS idx_image_embeddings ON assets USING ivfflat (image_embeddings vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_search_vector ON assets USING GIN(search_vector);

-- Composite indexes
CREATE INDEX IF NOT EXISTS idx_location_district ON assets(location_type, district);
CREATE INDEX IF NOT EXISTS idx_status_type ON assets(status, location_type);

-- Function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for auto-update
CREATE TRIGGER update_assets_updated_at 
    BEFORE UPDATE ON assets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to update search_vector
CREATE OR REPLACE FUNCTION assets_search_vector_update() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('simple', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.district, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.province, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(array_to_string(NEW.tags, ' '), '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for search_vector
CREATE TRIGGER assets_search_vector_trigger
    BEFORE INSERT OR UPDATE ON assets
    FOR EACH ROW 
    EXECUTE FUNCTION assets_search_vector_update();

-- Comments for documentation
COMMENT ON TABLE assets IS 'Main table for disaster relief assets and locations';
COMMENT ON COLUMN assets.location IS 'Geographic coordinates (PostGIS POINT)';
COMMENT ON COLUMN assets.embedding IS 'Text embedding vector for semantic search (768 dimensions)';
COMMENT ON COLUMN assets.images IS 'JSONB array of image metadata: [{"url": "", "caption": "", "uploaded_at": ""}]';
COMMENT ON COLUMN assets.tags IS 'Array of searchable tags in Thai/English';
COMMENT ON COLUMN assets.image_embeddings IS 'Image embedding vector for visual similarity search';
COMMENT ON COLUMN assets.search_vector IS 'Full-text search vector (auto-updated)';

-- Insert sample data (optional)
-- INSERT INTO assets (name, location_type, district, province, location, embedding, tags) VALUES
-- ('โรงพยาบาลรามาธิบดี', 'โรงพยาบาล', 'ราชเทวี', 'กรุงเทพมหานคร', 
--  ST_GeographyFromText('POINT(100.5327 13.7649)'), 
--  array_fill(0, ARRAY[768])::vector,
--  ARRAY['โรงพยาบาล', 'ฉุกเฉิน', '24ชม']);
