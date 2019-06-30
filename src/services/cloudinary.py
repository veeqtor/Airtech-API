"""Module for cloudinary operations"""

import cloudinary.uploader
from src.celery import celery_app
from src.apps.user_profile.models import UserProfile


@celery_app.task(name='upload-photo')
def upload_image(file, profile_id, photo_public_id, time_stamp):
    """Method to upload image file to cloudinary"""
    try:
        response = cloudinary.uploader.upload(file,
                                              folder=f"airtech/{profile_id}/",
                                              public_id=f"v{time_stamp}",
                                              allowed_formats=['jpg', 'png'],
                                              eager=[{
                                                  "width": 300,
                                                  "height": 300,
                                                  "crop": "mfit"
                                              }])

        if photo_public_id and response:
            # delete the old photo and save a new one.
            cloudinary.uploader.destroy(photo_public_id)
            photo_saved = UserProfile.objects.filter(pk=profile_id).update(
                photo_public_id=response['public_id'],
                photo_url=response['secure_url'])

            if photo_saved:
                print('SEND EMAIL')

    except Exception:
        print('SEND EXCEPTION EMAIL')
