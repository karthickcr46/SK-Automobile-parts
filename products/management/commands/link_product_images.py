import os

from django.conf import settings
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):

    help = "Automatically link product images to products"


    IMAGE_MAP = {

        "TVS-BRK-001":
            "front_disc_brake_pad_set.jpg",

        "BAJ-BRK-002":
            "rear_disc_brake_pad.jpg",

        "HER-BRK-003":
            "front_disc_brake_plate.jpg",

        "HON-BRK-004":
            "rear_brake_shoe_set.jpg",

        "HER-CHN-001":
            "chain_sprocket_kit.jpg",

        "ROL-CHN-002":
            "heavy_duty_drive_chain.jpg",

        "ROL-SPR-003":
            "rear_sprocket.jpg",

        "EXI-BAT-001":
            "motorcycle_battery.jpg",

        "BOS-HRN-002":
            "motorcycle_horn_12v.jpg",

        "BOS-IGN-003":
            "ignition_coil.jpg",

        "TVS-REG-004":
            "regulator_rectifier.jpg",

        "YAM-CLT-001":
            "clutch_plate_set.jpg",

        "HON-CLT-002":
            "clutch_cable.jpg",

        "BAJ-CLT-003":
            "clutch_spring_set.jpg",

        "HON-AIR-001":
            "air_filter.jpg",

        "BOS-OIL-002":
            "engine_oil_filter.jpg",

        "NGK-SPK-003":
            "spark_plug.jpg",

        "MOT-OIL-004":
            "engine_oil_10w30.jpg",

        "HJG-LED-001":
            "led_headlight_bulb_h4.jpg",

        "UNI-LED-002":
            "led_indicator_set.jpg",

        "TVS-TAL-003":
            "led_tail_light.jpg",

        "TVS-SHO-001":
            "rear_shock_absorber.jpg",

        "UNI-MIR-002":
            "side_mirror_pair.jpg",

        "BAJ-FTR-003":
            "passenger_footrest.jpg",

        "GEN-MOB-001":
            "motorcycle_mobile_holder.jpg",

        "GEN-USB-002":
            "usb_motorcycle_charger.jpg",

        "GEN-CVR-003":
            "waterproof_bike_cover.jpg",

        "MOT-CHL-001":
            "chain_lubricant.jpg",

        "MOT-BCL-002":
            "brake_cleaner.jpg",

        "CAS-OIL-003":
            "engine_oil_20w40.jpg",
    }


    def handle(self, *args, **options):

        media_products_path = os.path.join(
            settings.MEDIA_ROOT,
            "products"
        )


        if not os.path.exists(media_products_path):

            self.stdout.write(
                self.style.ERROR(
                    "Media products folder does not exist: "
                    f"{media_products_path}"
                )
            )

            return


        linked_count = 0
        missing_count = 0
        product_missing_count = 0


        for part_number, filename in self.IMAGE_MAP.items():

            image_path = os.path.join(
                media_products_path,
                filename
            )


            if not os.path.exists(image_path):

                self.stdout.write(
                    self.style.WARNING(
                        f"Image not found: {filename}"
                    )
                )

                missing_count += 1

                continue


            try:

                product = Product.objects.get(
                    part_number=part_number
                )

            except Product.DoesNotExist:

                self.stdout.write(
                    self.style.WARNING(
                        f"Product not found: {part_number}"
                    )
                )

                product_missing_count += 1

                continue


            product.image = f"products/{filename}"

            product.save(
                update_fields=["image"]
            )


            linked_count += 1


            self.stdout.write(
                self.style.SUCCESS(
                    f"Linked image: "
                    f"{product.name} -> {filename}"
                )
            )


        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Completed. "
                f"{linked_count} images linked."
            )
        )


        if missing_count > 0:

            self.stdout.write(
                self.style.WARNING(
                    f"{missing_count} image files were missing."
                )
            )


        if product_missing_count > 0:

            self.stdout.write(
                self.style.WARNING(
                    f"{product_missing_count} products were not found."
                )
            )