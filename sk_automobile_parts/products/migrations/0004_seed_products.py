
from django.db import migrations


SAMPLE_PRODUCTS = [

    # ======================================================
    # HONDA
    # ======================================================

    {
        "name": "Front Brake Pad Set",
        "bike_model": "Honda Activa 6G",
        "price": "450",
        "stock": 50,
    },
    {
        "name": "Rear Brake Shoe",
        "bike_model": "Honda Activa 6G",
        "price": "350",
        "stock": 40,
    },
    {
        "name": "Air Filter",
        "bike_model": "Honda Activa 6G",
        "price": "250",
        "stock": 60,
    },
    {
        "name": "Spark Plug",
        "bike_model": "Honda Activa 6G",
        "price": "180",
        "stock": 80,
    },
    {
        "name": "Drive Belt",
        "bike_model": "Honda Activa 6G",
        "price": "850",
        "stock": 25,
    },
    {
        "name": "Clutch Shoe Set",
        "bike_model": "Honda Activa 6G",
        "price": "700",
        "stock": 30,
    },

    # ======================================================
    # YAMAHA
    # ======================================================

    {
        "name": "Front Brake Pad",
        "bike_model": "Yamaha FZ",
        "price": "500",
        "stock": 45,
    },
    {
        "name": "Clutch Cable",
        "bike_model": "Yamaha FZ",
        "price": "220",
        "stock": 50,
    },
    {
        "name": "Air Filter",
        "bike_model": "Yamaha FZ",
        "price": "300",
        "stock": 55,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "Yamaha FZ",
        "price": "1400",
        "stock": 20,
    },
    {
        "name": "Rear Brake Pad",
        "bike_model": "Yamaha FZ",
        "price": "400",
        "stock": 35,
    },
    {
        "name": "Headlight Bulb",
        "bike_model": "Yamaha FZ",
        "price": "450",
        "stock": 30,
    },

    # ======================================================
    # ROYAL ENFIELD
    # ======================================================

    {
        "name": "Front Brake Pad Set",
        "bike_model": "Royal Enfield Classic 350",
        "price": "650",
        "stock": 40,
    },
    {
        "name": "Rear Brake Pad Set",
        "bike_model": "Royal Enfield Classic 350",
        "price": "550",
        "stock": 35,
    },
    {
        "name": "Spark Plug",
        "bike_model": "Royal Enfield Classic 350",
        "price": "250",
        "stock": 70,
    },
    {
        "name": "Engine Oil Filter",
        "bike_model": "Royal Enfield Classic 350",
        "price": "300",
        "stock": 50,
    },
    {
        "name": "Clutch Cable",
        "bike_model": "Royal Enfield Classic 350",
        "price": "280",
        "stock": 45,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "Royal Enfield Classic 350",
        "price": "1800",
        "stock": 20,
    },

    # ======================================================
    # BAJAJ
    # ======================================================

    {
        "name": "Front Brake Pad",
        "bike_model": "Bajaj Pulsar 150",
        "price": "450",
        "stock": 50,
    },
    {
        "name": "Clutch Plate Set",
        "bike_model": "Bajaj Pulsar 150",
        "price": "950",
        "stock": 25,
    },
    {
        "name": "Air Filter",
        "bike_model": "Bajaj Pulsar 150",
        "price": "280",
        "stock": 55,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "Bajaj Pulsar 150",
        "price": "1200",
        "stock": 30,
    },
    {
        "name": "Spark Plug",
        "bike_model": "Bajaj Pulsar 150",
        "price": "160",
        "stock": 80,
    },
    {
        "name": "Clutch Cable",
        "bike_model": "Bajaj Pulsar 150",
        "price": "200",
        "stock": 45,
    },

    # ======================================================
    # TVS
    # ======================================================

    {
        "name": "Front Brake Pad",
        "bike_model": "TVS Apache RTR 160",
        "price": "500",
        "stock": 40,
    },
    {
        "name": "Rear Brake Shoe",
        "bike_model": "TVS Apache RTR 160",
        "price": "400",
        "stock": 45,
    },
    {
        "name": "Air Filter",
        "bike_model": "TVS Apache RTR 160",
        "price": "300",
        "stock": 50,
    },
    {
        "name": "Spark Plug",
        "bike_model": "TVS Apache RTR 160",
        "price": "180",
        "stock": 75,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "TVS Apache RTR 160",
        "price": "1350",
        "stock": 25,
    },
    {
        "name": "Headlight Bulb",
        "bike_model": "TVS Apache RTR 160",
        "price": "400",
        "stock": 35,
    },

    # ======================================================
    # HERO
    # ======================================================

    {
        "name": "Front Brake Shoe",
        "bike_model": "Hero Splendor Plus",
        "price": "300",
        "stock": 60,
    },
    {
        "name": "Rear Brake Shoe",
        "bike_model": "Hero Splendor Plus",
        "price": "280",
        "stock": 60,
    },
    {
        "name": "Clutch Cable",
        "bike_model": "Hero Splendor Plus",
        "price": "180",
        "stock": 55,
    },
    {
        "name": "Air Filter",
        "bike_model": "Hero Splendor Plus",
        "price": "220",
        "stock": 65,
    },
    {
        "name": "Spark Plug",
        "bike_model": "Hero Splendor Plus",
        "price": "150",
        "stock": 90,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "Hero Splendor Plus",
        "price": "950",
        "stock": 30,
    },

    # ======================================================
    # KTM
    # ======================================================

    {
        "name": "Front Brake Pad",
        "bike_model": "KTM Duke 200",
        "price": "750",
        "stock": 30,
    },
    {
        "name": "Rear Brake Pad",
        "bike_model": "KTM Duke 200",
        "price": "600",
        "stock": 30,
    },
    {
        "name": "Air Filter",
        "bike_model": "KTM Duke 200",
        "price": "450",
        "stock": 40,
    },
    {
        "name": "Spark Plug",
        "bike_model": "KTM Duke 200",
        "price": "350",
        "stock": 50,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "KTM Duke 200",
        "price": "2200",
        "stock": 15,
    },
    {
        "name": "Clutch Cable",
        "bike_model": "KTM Duke 200",
        "price": "350",
        "stock": 25,
    },

    # ======================================================
    # SUZUKI
    # ======================================================

    {
        "name": "Front Brake Pad",
        "bike_model": "Suzuki Gixxer",
        "price": "550",
        "stock": 35,
    },
    {
        "name": "Rear Brake Pad",
        "bike_model": "Suzuki Gixxer",
        "price": "450",
        "stock": 35,
    },
    {
        "name": "Air Filter",
        "bike_model": "Suzuki Gixxer",
        "price": "320",
        "stock": 45,
    },
    {
        "name": "Spark Plug",
        "bike_model": "Suzuki Gixxer",
        "price": "200",
        "stock": 70,
    },
    {
        "name": "Chain Sprocket Kit",
        "bike_model": "Suzuki Gixxer",
        "price": "1500",
        "stock": 20,
    },
    {
        "name": "Clutch Cable",
        "bike_model": "Suzuki Gixxer",
        "price": "250",
        "stock": 40,
    },
]


# ==========================================================
# ADD DEFAULT PRODUCTS
# ==========================================================

def seed_products(apps, schema_editor):

    Product = apps.get_model(
        "products",
        "Product"
    )

    for data in SAMPLE_PRODUCTS:

        Product.objects.get_or_create(
            name=data["name"],
            bike_model=data["bike_model"],
            defaults={
                "price": data["price"],
                "stock": data["stock"],
            }
        )


# ==========================================================
# REMOVE DEFAULT PRODUCTS
# ==========================================================

def remove_products(apps, schema_editor):

    Product = apps.get_model(
        "products",
        "Product"
    )

    for data in SAMPLE_PRODUCTS:

        Product.objects.filter(
            name=data["name"],
            bike_model=data["bike_model"]
        ).delete()


# ==========================================================
# MIGRATION
# ==========================================================

class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_remove_product_brand_remove_product_category_and_more"),
    ]

    operations = [

        migrations.RunPython(
            seed_products,
            remove_products
        ),

    ]

