"""Module for file upload tasks."""

from datetime import datetime

from src.services.cloudinary import upload_image
from src.apps.core.utilities.messages import FILE_ERRORS
from src.apps.core.utilities.response_utils import ResponseHandler


class FileUpload(object):
    """Class to handle all file uploads."""

    @staticmethod
    def validate_image_file(file_obj):
        """
        Image file validations.

        Args:
            file_obj (file): The file object

        Returns:
            file_obj (file): The file object

        """

        image_formats = ('png', 'jpg', 'jpeg', 'JPEG')

        if file_obj is None:
            return ResponseHandler.raise_error(FILE_ERRORS['FILE_01'])

        if file_obj.size > 2000000:
            return ResponseHandler.raise_error(FILE_ERRORS['FILE_02'])

        content_type = file_obj.content_type.split('/')

        if content_type[0] is not 'image' and content_type[1] not in \
                image_formats:
            return ResponseHandler.raise_error(FILE_ERRORS['FILE_03'])

        return file_obj

    @classmethod
    def image(cls, file_obj, qs):
        """
        Method to asynchronously upload image file.

        Args:
            file_obj (file): The file object
            qs (queryset): The user profile queryset.

        Returns:
            None
        """

        file_obj = cls.validate_image_file(file_obj)
        file_path = file_obj.temporary_file_path()
        time_stamp = int(datetime.timestamp(datetime.now()))
        profile_id = qs.id
        photo_public_id = qs.photo_public_id

        upload_image.delay(file_path, profile_id, photo_public_id, time_stamp)
