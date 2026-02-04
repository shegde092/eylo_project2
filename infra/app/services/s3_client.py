import boto3
import logging
from pathlib import Path
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class S3Client:
    """Client for AWS S3 storage"""
    
    def __init__(self):
        self.bucket = settings.aws_s3_bucket
        
        if not settings.test_mode:
            self.s3 = boto3.client(
                's3',
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        else:
            self.s3 = None
            logger.info("S3Client initialized in TEST MODE (Mock S3)")
    
    async def upload_file(
        self,
        file_path: str,
        s3_key: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload file to S3
        
        Args:
            file_path: Local path to file
            s3_key: S3 object key (path in bucket)
            content_type: MIME type
            
        Returns:
            Public URL of uploaded file
        """
        if settings.test_mode:
            logger.info(f"MOCK Upload to S3: {file_path} -> {s3_key}")
            return f"https://mock-s3.local/{self.bucket}/{s3_key}"

        try:
            self.s3.upload_file(
                file_path,
                self.bucket,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'  # Make publicly accessible
                }
            )
            
            url = f"https://{self.bucket}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            logger.info(f"Uploaded to S3: {url}")
            return url
            
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise
    
    async def upload_from_url(
        self,
        url: str,
        s3_key: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Download from URL and upload to S3
        
        Args:
            url: Source URL
            s3_key: S3 object key
            content_type: MIME type
            
        Returns:
            Public URL of uploaded file
        """
        if settings.test_mode:
            logger.info(f"MOCK Upload from URL: {url} -> {s3_key}")
            return url  # Return original URL in test mode

        import httpx
        import tempfile
        
        try:
            # Download to temp file
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name
            
            # Upload to S3
            result = await self.upload_file(tmp_path, s3_key, content_type)
            
            # Clean up
            Path(tmp_path).unlink()
            
            return result
            
        except Exception as e:
            logger.error(f"S3 upload from URL failed: {str(e)}")
            raise


# Singleton instance
s3_client = S3Client()
