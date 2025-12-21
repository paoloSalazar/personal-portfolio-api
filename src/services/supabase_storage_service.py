import os
import uuid
from supabase import create_client, Client
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)

class SupabaseStorageService:
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_ANON_KEY')
        self.bucket_name = os.environ.get('SUPABASE_BUCKET', 'profile-photos')
        self._supabase = None

    @property
    def supabase(self):
        if self._supabase is None:
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
            self._supabase = create_client(self.supabase_url, self.supabase_key)
        return self._supabase

    def upload_profile_photo(self, file, user_id):
        """
        Upload a profile photo to Supabase Storage

        Args:
            file: FileStorage object from Flask request
            user_id: User ID for organizing files

        Returns:
            str: Public URL of the uploaded file

        Raises:
            ValueError: If file validation fails
            Exception: If upload fails
        """
        # Validate file
        if not file or not file.filename:
            raise ValueError("No file provided")

        # Check file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

        if file_ext not in allowed_extensions:
            raise ValueError(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")

        # Check file size (5MB limit)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > 5 * 1024 * 1024:  # 5MB
            raise ValueError("File size too large. Maximum size: 5MB")

        # Generate unique filename
        unique_filename = f"{user_id}_{uuid.uuid4()}.{file_ext}"
        file_path = f"profile-photos/{unique_filename}"

        try:
            # Upload file to Supabase
            file_content = file.read()
            response = self.supabase.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": f"image/{file_ext}"}
            )

            if response.status_code != 200:
                raise Exception(f"Upload failed with status {response.status_code}")

            # Get public URL
            public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)

            logger.info(f"Profile photo uploaded successfully for user {user_id}: {public_url}")
            return public_url

        except Exception as e:
            logger.error(f"Failed to upload profile photo for user {user_id}: {str(e)}")
            raise Exception(f"Failed to upload file: {str(e)}")

    def delete_profile_photo(self, photo_url):
        """
        Delete a profile photo from Supabase Storage

        Args:
            photo_url: The public URL of the photo to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            # Extract file path from URL
            # URL format: https://[project].supabase.co/storage/v1/object/public/[bucket]/[path]
            url_parts = photo_url.split('/storage/v1/object/public/')[1]
            bucket_and_path = url_parts.split('/', 1)
            if len(bucket_and_path) == 2:
                file_path = bucket_and_path[1]
                response = self.supabase.storage.from_(self.bucket_name).remove([file_path])
                return response.status_code == 200
            return False
        except Exception as e:
            logger.error(f"Failed to delete profile photo: {str(e)}")
            return False

# Global instance - created lazily
_supabase_storage_instance = None

def get_supabase_storage():
    global _supabase_storage_instance
    if _supabase_storage_instance is None:
        _supabase_storage_instance = SupabaseStorageService()
    return _supabase_storage_instance

# For backward compatibility
supabase_storage = None