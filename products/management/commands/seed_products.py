from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):

    help = "Create realistic motorcycle spare-part products"


    def handle(self, *args, **options):

        products = [

            # ==================================================
            # BRAKE SYSTEM
            # ==================================================

            {
                "category": "Brake System",
                "name": "Front Disc Brake Pad Set",
                "brand": "TVS",
                "part_number": "TVS-BRK-001",
                "description": "High-quality front disc brake pad set for reliable braking performance.",
                "price": 450,
                "stock": 25,
                "compatibility": "TVS Apache, Raider",
            },

            {
                "category": "Brake System",
                "name": "Rear Disc Brake Pad",
                "brand": "Bajaj",
                "part_number": "BAJ-BRK-002",
                "description": "Durable rear disc brake pads designed for consistent stopping performance.",
                "price": 520,
                "stock": 18,
                "compatibility": "Bajaj Pulsar, NS200",
            },

            {
                "category": "Brake System",
                "name": "Front Disc Brake Plate",
                "brand": "Hero",
                "part_number": "HER-BRK-003",
                "description": "Precision-machined front brake disc with excellent heat resistance.",
                "price": 1250,
                "stock": 12,
                "compatibility": "Hero Splendor, Xtreme",
            },

            {
                "category": "Brake System",
                "name": "Rear Brake Shoe Set",
                "brand": "Honda",
                "part_number": "HON-BRK-004",
                "description": "Reliable rear drum brake shoe set for smooth braking.",
                "price": 380,
                "stock": 30,
                "compatibility": "Honda Shine, Unicorn",
            },


            # ==================================================
            # CHAIN & SPROCKET
            # ==================================================

            {
                "category": "Chain & Sprocket",
                "name": "Chain Sprocket Kit",
                "brand": "Hero",
                "part_number": "HER-CHN-001",
                "description": "Complete chain and sprocket kit for smooth power transmission.",
                "price": 950,
                "stock": 20,
                "compatibility": "Hero Splendor, HF Deluxe",
            },

            {
                "category": "Chain & Sprocket",
                "name": "Heavy Duty Drive Chain",
                "brand": "Rolon",
                "part_number": "ROL-CHN-002",
                "description": "Heavy-duty motorcycle drive chain with long service life.",
                "price": 650,
                "stock": 22,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Chain & Sprocket",
                "name": "Rear Sprocket",
                "brand": "Rolon",
                "part_number": "ROL-SPR-003",
                "description": "Precision-cut rear sprocket for efficient drivetrain performance.",
                "price": 550,
                "stock": 16,
                "compatibility": "Bajaj Pulsar",
            },


            # ==================================================
            # ELECTRICAL PARTS
            # ==================================================

            {
                "category": "Electrical Parts",
                "name": "12V Motorcycle Battery",
                "brand": "Exide",
                "part_number": "EXI-BAT-001",
                "description": "Maintenance-free 12V battery designed for reliable starting power.",
                "price": 1850,
                "stock": 14,
                "compatibility": "Honda, Yamaha, TVS",
            },

            {
                "category": "Electrical Parts",
                "name": "Motorcycle Horn 12V",
                "brand": "Bosch",
                "part_number": "BOS-HRN-002",
                "description": "High-quality 12V motorcycle horn with clear sound output.",
                "price": 220,
                "stock": 35,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Electrical Parts",
                "name": "Ignition Coil",
                "brand": "Bosch",
                "part_number": "BOS-IGN-003",
                "description": "Reliable ignition coil for consistent engine starting.",
                "price": 680,
                "stock": 15,
                "compatibility": "Honda, Hero",
            },

            {
                "category": "Electrical Parts",
                "name": "Regulator Rectifier",
                "brand": "TVS",
                "part_number": "TVS-REG-004",
                "description": "Voltage regulator rectifier for stable motorcycle electrical systems.",
                "price": 780,
                "stock": 11,
                "compatibility": "TVS Apache",
            },


            # ==================================================
            # CLUTCH PARTS
            # ==================================================

            {
                "category": "Clutch Parts",
                "name": "Clutch Plate Set",
                "brand": "Yamaha",
                "part_number": "YAM-CLT-001",
                "description": "Complete clutch plate set for smooth gear shifting.",
                "price": 750,
                "stock": 19,
                "compatibility": "Yamaha FZ, MT-15",
            },

            {
                "category": "Clutch Parts",
                "name": "Clutch Cable",
                "brand": "Honda",
                "part_number": "HON-CLT-002",
                "description": "Flexible and durable clutch cable for smooth clutch operation.",
                "price": 180,
                "stock": 40,
                "compatibility": "Honda Shine",
            },

            {
                "category": "Clutch Parts",
                "name": "Clutch Spring Set",
                "brand": "Bajaj",
                "part_number": "BAJ-CLT-003",
                "description": "Heavy-duty clutch springs for consistent clutch engagement.",
                "price": 260,
                "stock": 25,
                "compatibility": "Bajaj Pulsar",
            },


            # ==================================================
            # ENGINE PARTS
            # ==================================================

            {
                "category": "Engine Parts",
                "name": "Air Filter",
                "brand": "Honda",
                "part_number": "HON-AIR-001",
                "description": "High-efficiency engine air filter for improved airflow.",
                "price": 280,
                "stock": 32,
                "compatibility": "Honda Shine, Unicorn",
            },

            {
                "category": "Engine Parts",
                "name": "Engine Oil Filter",
                "brand": "Bosch",
                "part_number": "BOS-OIL-002",
                "description": "Engine oil filter designed to remove contaminants effectively.",
                "price": 320,
                "stock": 28,
                "compatibility": "Honda, Yamaha, TVS",
            },

            {
                "category": "Engine Parts",
                "name": "Spark Plug",
                "brand": "NGK",
                "part_number": "NGK-SPK-003",
                "description": "Reliable spark plug for efficient ignition and engine performance.",
                "price": 160,
                "stock": 50,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Engine Parts",
                "name": "Engine Oil 10W-30",
                "brand": "Motul",
                "part_number": "MOT-OIL-004",
                "description": "Premium motorcycle engine oil providing excellent engine protection.",
                "price": 520,
                "stock": 24,
                "compatibility": "Honda, Yamaha, TVS",
            },


            # ==================================================
            # LIGHTING
            # ==================================================

            {
                "category": "Lighting",
                "name": "LED Headlight Bulb H4",
                "brand": "HJG",
                "part_number": "HJG-LED-001",
                "description": "Bright LED H4 headlight bulb with improved night visibility.",
                "price": 950,
                "stock": 17,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Lighting",
                "name": "LED Indicator Set",
                "brand": "Universal",
                "part_number": "UNI-LED-002",
                "description": "Modern LED indicator set for improved visibility and styling.",
                "price": 450,
                "stock": 23,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Lighting",
                "name": "LED Tail Light",
                "brand": "TVS",
                "part_number": "TVS-TAL-003",
                "description": "Bright LED tail light for improved rear visibility.",
                "price": 380,
                "stock": 20,
                "compatibility": "TVS Apache",
            },


            # ==================================================
            # BODY PARTS
            # ==================================================

            {
                "category": "Body Parts",
                "name": "Rear Shock Absorber",
                "brand": "TVS",
                "part_number": "TVS-SHO-001",
                "description": "Durable rear shock absorber providing comfortable suspension performance.",
                "price": 2450,
                "stock": 8,
                "compatibility": "TVS Apache",
            },

            {
                "category": "Body Parts",
                "name": "Side Mirror Pair",
                "brand": "Universal",
                "part_number": "UNI-MIR-002",
                "description": "Universal motorcycle side mirror pair with clear rear visibility.",
                "price": 350,
                "stock": 35,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Body Parts",
                "name": "Passenger Footrest",
                "brand": "Bajaj",
                "part_number": "BAJ-FTR-003",
                "description": "Strong replacement passenger footrest for comfortable riding.",
                "price": 420,
                "stock": 18,
                "compatibility": "Bajaj Pulsar",
            },


            # ==================================================
            # ACCESSORIES
            # ==================================================

            {
                "category": "Accessories",
                "name": "Motorcycle Mobile Holder",
                "brand": "Generic",
                "part_number": "GEN-MOB-001",
                "description": "Secure handlebar-mounted mobile holder for motorcycles.",
                "price": 499,
                "stock": 45,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Accessories",
                "name": "USB Motorcycle Charger",
                "brand": "Generic",
                "part_number": "GEN-USB-002",
                "description": "12V USB charger for convenient mobile charging while riding.",
                "price": 399,
                "stock": 30,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Accessories",
                "name": "Waterproof Bike Cover",
                "brand": "Generic",
                "part_number": "GEN-CVR-003",
                "description": "Water-resistant motorcycle cover for outdoor protection.",
                "price": 650,
                "stock": 20,
                "compatibility": "Universal Motorcycle",
            },


            # ==================================================
            # SERVICE PARTS
            # ==================================================

            {
                "category": "Service Parts",
                "name": "Chain Lubricant",
                "brand": "Motul",
                "part_number": "MOT-CHL-001",
                "description": "Premium chain lubricant for smoother and quieter chain operation.",
                "price": 480,
                "stock": 26,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Service Parts",
                "name": "Brake Cleaner",
                "brand": "Motul",
                "part_number": "MOT-BCL-002",
                "description": "Fast-drying brake cleaner for motorcycle brake components.",
                "price": 350,
                "stock": 20,
                "compatibility": "Universal Motorcycle",
            },

            {
                "category": "Service Parts",
                "name": "Engine Oil 20W-40",
                "brand": "Castrol",
                "part_number": "CAS-OIL-003",
                "description": "Motorcycle engine oil for everyday riding and engine protection.",
                "price": 420,
                "stock": 32,
                "compatibility": "Hero, Bajaj, Honda",
            },

        ]


        created_count = 0


        for item in products:

            category, created = Category.objects.get_or_create(
                name=item["category"],
                defaults={
                    "description":
                        f"Motorcycle {item['category']} spare parts."
                }
            )


            product, created = Product.objects.update_or_create(

                part_number=item["part_number"],

                defaults={

                    "category": category,

                    "name": item["name"],

                    "brand": item["brand"],

                    "description": item["description"],

                    "price": item["price"],

                    "stock": item["stock"],

                    "compatibility": item["compatibility"],

                    "is_active": True,

                }

            )


            if created:

                created_count += 1


        self.stdout.write(
            self.style.SUCCESS(
                f"Product catalog completed. "
                f"{created_count} new products created."
            )
        )