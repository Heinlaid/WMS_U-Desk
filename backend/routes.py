from flask import render_template, request, redirect, url_for
from app import app
from models import db, Product, Detail, ProductCategory, DetailCategory, OperationHistory, Order, Supplier, Customer

# 📦 Товары
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        stock_quantity = request.form['stock_quantity']
        cost = request.form['cost']
        price = request.form['price']

        product = Product(name=name, description=description,
                          stock_quantity=int(stock_quantity),
                          cost=float(cost), price=float(price))
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products'))

    return render_template('new_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.stock_quantity = int(request.form['stock_quantity'])
        product.cost = float(request.form['cost'])
        product.price = float(request.form['price'])

        db.session.commit()
        return redirect(url_for('products'))

    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))

# 🔧 Детали
@app.route('/details')
def details():
    details = Detail.query.all()
    return render_template('details.html', details=details)

@app.route('/details/new', methods=['GET', 'POST'])
def new_detail():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        stock_quantity = int(request.form['stock_quantity'])
        unit = request.form['unit']  # Добавляем получение unit
        price = float(request.form['price'])

        detail = Detail(name=name, description=description, stock_quantity=stock_quantity, unit=unit, price=price)
        db.session.add(detail)
        db.session.commit()
        return redirect(url_for('details'))

    return render_template('new_detail.html')


@app.route('/details/edit/<int:id>', methods=['GET', 'POST'])
def edit_detail(id):
    detail = Detail.query.get(id)
    if request.method == 'POST':
        detail.name = request.form['name']
        detail.description = request.form['description']
        detail.stock_quantity = int(request.form['stock_quantity'])
        detail.price = float(request.form['price'])

        db.session.commit()
        return redirect(url_for('details'))

    return render_template('edit_detail.html', detail=detail)

@app.route('/details/delete/<int:id>', methods=['POST'])
def delete_detail(id):
    detail = Detail.query.get(id)
    db.session.delete(detail)
    db.session.commit()
    return redirect(url_for('details'))

# 📖 Категории (Справочники)
@app.route('/categories')
def categories():
    product_categories = ProductCategory.query.all()
    detail_categories = DetailCategory.query.all()
    return render_template('categories.html', product_categories=product_categories, detail_categories=detail_categories)

@app.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_type = request.form['category_type']

        if category_type == "product":
            category = ProductCategory(name=name, description=description)
        else:
            category = DetailCategory(name=name, description=description)

        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))

    return render_template('new_category.html')

# 🛠 Операции
@app.route('/operations')
def operations():
    operations = OperationHistory.query.all()
    return render_template('operations.html', operations=operations)

@app.route('/operations/new', methods=['GET', 'POST'])
def new_operation():
    if request.method == 'POST':
        operation_type = request.form['operation_type']
        changed_quantity = int(request.form['changed_quantity'])
        product_id = request.form.get('product_id')
        detail_id = request.form.get('detail_id')

        operation = OperationHistory(operation_type=operation_type, changed_quantity=changed_quantity,
                                     product_id=product_id, detail_id=detail_id)

        # Автоматическое обновление количества товара или детали
        if product_id:
            product = Product.query.get(product_id)
            if operation_type == "приход":
                product.stock_quantity += changed_quantity
            elif operation_type == "расход":
                product.stock_quantity -= changed_quantity

        if detail_id:
            detail = Detail.query.get(detail_id)
            if operation_type == "приход":
                detail.stock_quantity += changed_quantity
            elif operation_type == "расход":
                detail.stock_quantity -= changed_quantity

        db.session.add(operation)
        db.session.commit()
        return redirect(url_for('operations'))

    return render_template('new_operation.html')

# 📑 Заказы
@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/orders/new', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        product_id = request.form['product_id']
        customer_id = request.form['customer_id']
        quantity = int(request.form['quantity'])

        product = Product.query.get(product_id)
        if product and product.stock_quantity >= quantity:
            product.stock_quantity -= quantity
            order = Order(product_id=product_id, customer_id=customer_id)
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('orders'))
        else:
            return "Ошибка: недостаточно товара на складе", 400

    return render_template('new_order.html')

# 👥 Клиенты
@app.route('/clients')
def clients():
    clients = Customer.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/clients/new', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        contact_person = request.form['contact_person']

        client = Customer(name=name, address=address, phone=phone, contact_person=contact_person)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients'))

    return render_template('new_client.html')

# 🚚 Поставщики
@app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/suppliers/new', methods=['GET', 'POST'])
def new_supplier():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        contact_person = request.form['contact_person']

        supplier = Supplier(name=name, address=address, phone=phone, contact_person=contact_person)
        db.session.add(supplier)
        db.session.commit()
        return redirect(url_for('suppliers'))

    return render_template('new_supplier.html')
