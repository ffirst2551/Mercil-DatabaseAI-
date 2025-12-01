"""
Image Management API
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List
import os
import json
import uuid
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
import sys
sys.path.append('..')

from ai.image_tagger import ImageTagger
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/images", tags=["images"])

# Initialize
image_tagger = ImageTagger()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DB_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    """Get database connection"""
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn


@router.post("/upload/{asset_id}")
async def upload_image(
    asset_id: int,
    file: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    auto_tag: bool = Form(True)
):
    """
    อัพโหลดรูปภาพสำหรับ asset
    
    Args:
        asset_id: ID ของ asset
        file: ไฟล์รูปภาพ
        caption: คำอธิบายรูป (optional)
        auto_tag: สร้าง tags อัตโนมัติหรือไม่
    """
    try:
        # 1. ตรวจสอบว่า asset มีอยู่จริง
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT id FROM assets WHERE id = %s", (asset_id,))
        asset = cur.fetchone()
        
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # 2. บันทึกไฟล์
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{asset_id}_{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 3. สร้าง tags อัตโนมัติ (ถ้าต้องการ)
        tags = []
        image_embedding = None
        
        if auto_tag:
            tags = image_tagger.generate_tags(file_path)
            image_embedding = image_tagger.get_image_embedding(file_path)
        
        # 4. สร้าง image object
        image_data = {
            "url": f"/uploads/{unique_filename}",
            "filename": file.filename,
            "caption": caption,
            "uploaded_at": datetime.now().isoformat(),
            "size": len(content),
            "content_type": file.content_type
        }
        
        # 5. อัพเดท database
        cur.execute("""
            UPDATE assets 
            SET 
                images = COALESCE(images, '[]'::jsonb) || %s::jsonb,
                tags = COALESCE(tags, ARRAY[]::text[]) || %s::text[],
                image_embeddings = COALESCE(%s::vector, image_embeddings)
            WHERE id = %s
            RETURNING id, images, tags
        """, (
            json.dumps([image_data]),
            tags,
            image_embedding,
            asset_id
        ))
        
        updated = cur.fetchone()
        conn.commit()
        
        cur.close()
        conn.close()
        
        return {
            "message": "Image uploaded successfully",
            "asset_id": asset_id,
            "image": image_data,
            "generated_tags": tags,
            "total_images": len(updated['images']) if updated else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search-by-image")
async def search_by_image(
    file: UploadFile = File(...),
    limit: int = 10
):
    """
    ค้นหา assets ด้วยรูปภาพ (Image similarity search)
    
    1. อัพโหลดรูป
    2. สร้าง embedding
    3. ค้นหา assets ที่มีรูปคล้ายกัน
    """
    try:
        # 1. บันทึกไฟล์ชั่วคราว
        temp_path = os.path.join(UPLOAD_DIR, f"temp_{uuid.uuid4()}.jpg")
        
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 2. สร้าง embedding
        query_embedding = image_tagger.get_image_embedding(temp_path)
        
        # 3. สร้าง tags จากรูป
        query_tags = image_tagger.generate_tags(temp_path)
        
        # 4. ค้นหาด้วย vector similarity
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                id,
                name,
                location_type,
                district,
                province,
                tags,
                images,
                ST_AsText(location) as coordinates,
                1 - (image_embeddings <=> %s::vector) as similarity
            FROM assets
            WHERE image_embeddings IS NOT NULL
            ORDER BY similarity DESC
            LIMIT %s
        """, (query_embedding, limit))
        
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # 5. ลบไฟล์ชั่วคราว
        os.remove(temp_path)
        
        return {
            "results": [dict(row) for row in results],
            "detected_tags": query_tags,
            "total": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/asset/{asset_id}")
async def get_asset_images(asset_id: int):
    """
    ดูรูปภาพทั้งหมดของ asset
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT id, name, images, tags
            FROM assets
            WHERE id = %s
        """, (asset_id,))
        
        asset = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        return {
            "asset_id": asset['id'],
            "name": asset['name'],
            "images": asset['images'] or [],
            "tags": asset['tags'] or [],
            "total_images": len(asset['images']) if asset['images'] else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{asset_id}/image/{image_index}")
async def delete_image(asset_id: int, image_index: int):
    """
    ลบรูปภาพ
    
    Args:
        asset_id: ID ของ asset
        image_index: ลำดับของรูปใน array (0-based)
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. ดึงข้อมูล images ปัจจุบัน
        cur.execute("SELECT images FROM assets WHERE id = %s", (asset_id,))
        asset = cur.fetchone()
        
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        images = asset['images'] or []
        
        if image_index >= len(images):
            raise HTTPException(status_code=404, detail="Image not found")
        
        # 2. ลบไฟล์จริง
        image_to_delete = images[image_index]
        file_path = image_to_delete['url'].replace('/uploads/', 'uploads/')
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 3. ลบจาก database
        images.pop(image_index)
        
        cur.execute("""
            UPDATE assets 
            SET images = %s::jsonb
            WHERE id = %s
        """, (json.dumps(images), asset_id))
        
        conn.commit()
        
        cur.close()
        conn.close()
        
        return {
            "message": "Image deleted successfully",
            "remaining_images": len(images)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/serve/{filename}")
async def serve_image(filename: str):
    """
    ให้บริการไฟล์รูปภาพ
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)
