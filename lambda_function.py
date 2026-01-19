import urllib.parse
import os
import logging
from exif import Image
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
DEST_BUCKET = os.environ['DEST_BUCKET']

def lambda_handler(event: dict[str, Any], context: Any) -> None:
    """
    AWS Lambda handler to strip EXIF data from uploaded JPEG files.
    """
    records: list[dict[str, Any]] = event.get('Records', [])

    for record in records:
        src_bucket = record['s3']['bucket']['name']

        # ===== Decode the URL-encoded key =====
        obj_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        if not obj_key.lower().endswith('.jpg'):
            logger.info(f"Skipping non-JPG file: {obj_key}")
            continue

        try:
            obj = s3.get_object(Bucket=src_bucket, Key=obj_key)
            img_data = obj['Body'].read()

            image = Image(img_data)

            # ===== Removes EXIF metadata =====
            if image.has_exif:
                image.delete_all()
                logger.info(f"Stripped EXIF from {obj_key}")
            cleaned_image = image.get_file()

        except Exception as e:
            logger.info(f"Failed to strip EXIF from {obj_key}: {e}")
            continue

        # ===== Upload to destination bucket =====
        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=obj_key,
            Body=cleaned_image,
            ContentType='image/jpeg'
        )

        logger.info(f"Cleaned file written to {DEST_BUCKET}/{obj_key}")
