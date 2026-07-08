from src.models.order import Order, OrderStatus, PaymentMethod
from faker import Faker

PAYMENT_WEIGHTS: dict[PaymentMethod, float] = {
    PaymentMethod.CARD: 70,
    PaymentMethod.PAYPAL: 15,
    PaymentMethod.APPLE_PAY: 10,
    PaymentMethod.GOOGLE_PAY: 5,
}

STATUS_MAP: dict[str, OrderStatus] = {
    "PENDING": OrderStatus.PENDING,
    "PROCESSING": OrderStatus.PROCESSING,
    "SHIPPED": OrderStatus.SHIPPED,
    "DELIVERED": OrderStatus.DELIVERED,
    "CANCELLED": OrderStatus.CANCELLED,
}


COUNTRIES: dict[str, str] = {
    "United Kingdom": "en_GB",
    "United States": "en_US",
    "Australia": "en_AU",
    "New Zealand": "en_NZ",
    "Canada": "en_CA",
    "Ireland": "en_IE",
    "Germany": "de_DE",
}

_FAKERS: dict[str, Faker] = {locale: Faker(locale) for locale in COUNTRIES.values()}

VIP_RATE = 0.15

CATEGORY_CONFIG = {
    "Electronics": {
        "items": [
            "Smartphone", "Laptop", "Wireless Headphones", "Smart Watch", 
            "Tablet", "Bluetooth Speaker", "Gaming Console", "4K Monitor"
        ],
        "price_range": (15, 2500)
    },
    "Apparel": {
        "items": [
            "Cotton T-Shirt", "Slim Fit Jeans", "Leather Jacket", "Running Shoes", 
            "Hoodie", "Sun Hat", "Wool Socks", "Winter Coat"
        ],
        "price_range": (5, 500)
    },
    "Groceries": {
        "items": [
            "Organic Bananas", "Whole Milk", "Sourdough Bread", "Dark Chocolate", 
            "Greek Yogurt", "Olive Oil", "Fresh Salmon", "Avocados"
        ],
        "price_range": (1, 50)
    },
    "Home & Kitchen": {
        "items": [
            "Blender", "Air Fryer", "Coffee Maker", "Ceramic Frying Pan", 
            "Toaster", "Electric Kettle", "Slow Cooker", "Knife Set"
        ],
        "price_range": (10, 600)
    },
    "Beauty & Personal Care": {
        "items": [
            "Moisturizer", "Sunscreen", "Shampoo", "Electric Toothbrush", 
            "Perfume", "Beard Oil", "Face Mask"
        ],
        "price_range": (5, 200)
    },
    "Sports & Outdoors": {
        "items": [
            "Yoga Mat", "Dumbbells", "Water Bottle", "Camping Tent", 
            "Sleeping Bag", "Bicycle", "Resistance Bands"
        ],
        "price_range": (8, 1200)
    },
    "Books & Stationery": {
        "items": [
            "Sci-Fi Novel", "Notebook", "Gel Pens", "Desk Organizer", 
            "Biography", "Sketchbook", "Highlighters"
        ],
        "price_range": (2, 80)
    },
    "Toys & Hobbies": {
        "items": [
            "Lego Set", "Board Game", "Puzzle", "Remote Control Car", 
            "Action Figure", "Plush Toy", "Art Paint Kit"
        ],
        "price_range": (5, 350)
    },
    "Automotive": {
        "items": [
            "Car Phone Mount", "Floor Mats", "Dash Cam", "Car Shampoo", 
            "Portable Air Compressor", "Microfiber Towels"
        ],
        "price_range": (5, 250)
    },
    "Office Supplies": {
        "items": [
            "Ergonomic Chair", "Standing Desk", "Paper Shredder", "Wireless Mouse", 
            "Keyboard", "Filing Cabinet"
        ],
        "price_range": (10, 800)
    }
}