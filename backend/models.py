from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    stock_quantity = db.Column(db.Integer, default=0)
    cost = db.Column(db.Float)
    price = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Пример связи с категорией (если модель ProductCategory определена)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category = db.relationship('ProductCategory', back_populates='products')

    def __repr__(self):
        return f"<Product {self.name}>"

class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    # Обратная связь: список изделий, принадлежащих данной категории
    products = db.relationship('Product', back_populates='category')

    def __repr__(self):
        return f"<ProductCategory {self.name}>"

class Detail(db.Model):
    __tablename__ = "detail"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    stock_quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(10), nullable=False)
    min_stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Пример связи с категорией (если модель DetailCategory определена)
    category_id = db.Column(db.Integer, db.ForeignKey('detail_category.id'))
    category = db.relationship('DetailCategory', back_populates='details')
    
    def __repr__(self):
        return f"<Detail {self.name}>"

class DetailCategory(db.Model):
    __tablename__ = 'detail_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    # Обратная связь: список деталей, принадлежащих данной категории
    details = db.relationship('Detail', back_populates='category')
    
     def __repr__(self):
        return f"<DetailCategory {self.name}>"

from datetime import datetime
from app import db

# 1. Поставщик (Supplier)
class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))  # Можно также использовать db.String(15) для номера телефона
    contact_person = db.Column(db.String(100))

    # Связь с деталями (если поставщик поставляет несколько деталей)
    details = db.relationship('Detail', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.name}>"

# 2. Заказчик (Customer)
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    contact_person = db.Column(db.String(100))

    # Связь с заказами (у одного заказчика может быть несколько заказов)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"

# 3. История операций (OperationHistory)
class OperationHistory(db.Model):
    __tablename__ = 'operation_history'
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(50), nullable=False)  # "приход", "расход", "возврат", "корректировка"
    changed_quantity = db.Column(db.Integer, nullable=False)
    operation_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Связи: операция может относиться либо к изделию, либо к детали
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('detail.id'), nullable=True)

    def __repr__(self):
        return f"<OperationHistory {self.operation_type} - {self.changed_quantity}>"

# 4. Связь изделие-деталь (ProductDetail)
class ProductDetail(db.Model):
    __tablename__ = 'product_detail'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey('detail.id'), nullable=False)
    required_quantity = db.Column(db.Integer, nullable=False)

    # Связи
    product = db.relationship('Product', backref='product_details')
    detail = db.relationship('Detail', backref='product_details')

    def __repr__(self):
        return f"<ProductDetail Product {self.product_id} - Detail {self.detail_id}>"

# 5. Заказ (Order)
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_status = db.Column(db.String(50), nullable=False)  # "новый", "в производстве", "завершён"

    # Связи
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return f"<Order {self.id} - {self.order_status}>"