from flask import render_template, request, redirect, url_for
from app import app
from models import db, Product  # Импортируем db из models, а не из app!

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Создание нового товара (CREATE)
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

# Обновление товара (UPDATE)
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

# Удаление товара (DELETE)
@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))
