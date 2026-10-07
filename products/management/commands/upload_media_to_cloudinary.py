import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from products.models import Product


class Command(BaseCommand):
    help = "Upload existing product images to Cloudinary."

    def handle(self, *args, **options):

        # Make sure CLOUDINARY_URL is available
        if not os.getenv("CLOUDINARY_URL"):
            self.stdout.write(
                self.style.ERROR(
                    "CLOUDINARY_URL is not set in the environment."
                )
            )
            return

        media_products = Path(settings.BASE_DIR) / "media" / "products"

        if not media_products.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"Product media folder not found: {media_products}"
                )
            )
            return

        products = Product.objects.exclude(image="").order_by("id")

        total = products.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Found {total} products with images."
            )
        )

        uploaded = 0
        failed = 0

        for product in products:

            image_name = Path(product.image.name).name
            local_path = media_products / image_name

            if not local_path.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"SKIPPED: {product.name} -> "
                        f"{local_path.name} not found"
                    )
                )
                failed += 1
                continue

            try:
                with local_path.open("rb") as image_file:

                    # Force Django's Cloudinary storage to upload
                    # the existing local image.
                    saved_name = product.image.storage.save(
                        product.image.name,
                        File(image_file),
                    )

                # Update the database with the Cloudinary storage name.
                product.image.name = saved_name
                product.save(update_fields=["image"])

                uploaded += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"UPLOADED: {product.name} -> {saved_name}"
                    )
                )

            except Exception as exc:

                failed += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"FAILED: {product.name} -> {exc}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished. Uploaded: {uploaded}, Failed/Skipped: {failed}"
            )
        )