from store import Store
from models import Product, User

s = Store()
p = Product(name="something", price=12, category="thing")
s.add_product('something', 2)
print(s.get_total_asset())