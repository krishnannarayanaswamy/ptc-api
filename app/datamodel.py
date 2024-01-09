class Product:
    def __init__(self, product_id: int, item_sku: str, item_name: str, product_url: str, brand: str, category: str, unit_price: float, image: str, description: str):
        self.product_id = product_id
        self.item_sku = item_sku
        self.item_name = item_name
        self.product_url = product_url
        self.brand = brand
        self.category = category
        self.unit_price = unit_price
        self.image = image
        self.description = description

    def __dict__(self):
        return {
            "product_id": self.product_id,
            "item_sku": self.item_sku,
            "item_name": self.item_name,
            "product_url": self.product_url,
            "brand": self.brand,
            "category": self.category,
            "unit_price": self.unit_price,
            "image": self.image,
            "description": self.description,
        }

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "item_sku": self.item_sku,
            "item_name": self.item_name,
            "product_url": self.product_url,
            "brand": self.brand,
            "category": self.category,
            "unit_price": self.unit_price,
            "image": self.image,
            "description": self.description,
        }
