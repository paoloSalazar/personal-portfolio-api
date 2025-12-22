import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from src.services.supabase_storage_service import SupabaseStorageService, get_supabase_storage


class TestSupabaseStorageService:
    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_init(self):
        service = SupabaseStorageService()
        assert service.supabase_url == 'https://test.supabase.co'
        assert service.supabase_key == 'test-anon-key'
        assert service.service_role_key == 'test-service-key'
        assert service.bucket_name == 'test-bucket'

    @patch('src.services.supabase_storage_service.create_client')
    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key'
    })
    def test_supabase_property(self, mock_create_client):
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client

        service = SupabaseStorageService()
        client = service.supabase

        assert client == mock_client
        mock_create_client.assert_called_once_with('https://test.supabase.co', 'test-anon-key')

    @patch('src.services.supabase_storage_service.create_client')
    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key'
    })
    def test_supabase_service_property(self, mock_create_client):
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client

        service = SupabaseStorageService()
        client = service.supabase_service

        assert client == mock_client
        mock_create_client.assert_called_once_with('https://test.supabase.co', 'test-service-key')

    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_upload_profile_photo_success(self):
        with patch('src.services.supabase_storage_service.create_client') as mock_create_client:
            mock_storage = MagicMock()
            mock_client = MagicMock()
            mock_client.storage.from_.return_value.upload.return_value = None
            mock_client.storage.from_.return_value.get_public_url.return_value = 'https://test.supabase.co/storage/v1/object/public/test-bucket/test-path'
            mock_create_client.return_value = mock_client

            service = SupabaseStorageService()

            # Create a mock file
            mock_file = MagicMock()
            mock_file.filename = 'test.jpg'
            mock_file.read.return_value = b'fake image data'
            mock_file.seek = MagicMock()

            result = service.upload_profile_photo(mock_file, 1)

            assert result == 'https://test.supabase.co/storage/v1/object/public/test-bucket/test-path'
            mock_client.storage.from_.assert_called_with('test-bucket')
            mock_client.storage.from_().upload.assert_called_once()
            mock_client.storage.from_().get_public_url.assert_called_once()

    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_upload_profile_photo_invalid_file_type(self):
        service = SupabaseStorageService()

        mock_file = MagicMock()
        mock_file.filename = 'test.txt'

        with pytest.raises(ValueError, match="File type not allowed"):
            service.upload_profile_photo(mock_file, 1)

    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_upload_profile_photo_file_too_large(self):
        service = SupabaseStorageService()

        mock_file = MagicMock()
        mock_file.filename = 'test.jpg'
        mock_file.seek = MagicMock()
        mock_file.tell.return_value = 6 * 1024 * 1024  # 6MB

        with pytest.raises(ValueError, match="File size too large"):
            service.upload_profile_photo(mock_file, 1)

    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_upload_profile_photo_upload_error(self):
        with patch('src.services.supabase_storage_service.create_client') as mock_create_client:
            mock_client = MagicMock()
            mock_client.storage.from_.return_value.upload.return_value = {'statusCode': 403, 'error': 'Unauthorized', 'message': 'Test error'}
            mock_create_client.return_value = mock_client

            service = SupabaseStorageService()

            mock_file = MagicMock()
            mock_file.filename = 'test.jpg'
            mock_file.read.return_value = b'fake image data'
            mock_file.seek = MagicMock()

            with pytest.raises(Exception, match="Upload failed with status 403"):
                service.upload_profile_photo(mock_file, 1)

    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_delete_profile_photo_success(self):
        with patch('src.services.supabase_storage_service.create_client') as mock_create_client:
            mock_client = MagicMock()
            mock_client.storage.from_.return_value.remove.return_value.status_code = 200
            mock_create_client.return_value = mock_client

            service = SupabaseStorageService()

            result = service.delete_profile_photo('https://test.supabase.co/storage/v1/object/public/test-bucket/path/to/file.jpg')

            assert result is True
            mock_client.storage.from_().remove.assert_called_once_with(['path/to/file.jpg'])

    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'SUPABASE_BUCKET': 'test-bucket'
    })
    def test_delete_profile_photo_invalid_url(self):
        service = SupabaseStorageService()

        result = service.delete_profile_photo('https://invalid.url/file.jpg')

        assert result is False


@patch.dict('os.environ', {
    'SUPABASE_URL': 'https://test.supabase.co',
    'SUPABASE_ANON_KEY': 'test-anon-key',
    'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key'
})
def test_get_supabase_storage():
    with patch('src.services.supabase_storage_service.SupabaseStorageService') as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        service = get_supabase_storage()

        assert service == mock_service
        mock_service_class.assert_called_once()