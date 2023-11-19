from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from homework_shop.models import Customer, Weapon, WeapOrder, Order, db, weapon_schema, weapons_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods=['GET', 'POST'])
def token():
    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id) 
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again.'
        }
    
@api.route('/shop')
@jwt_required()
def get_shop():
    allweaps = Weapon.query.all()
    response = weapons_schema.dump(allweaps)
    return jsonify(response)

@api.route('/order/<cust_id>', methods = ['POST'])
@jwt_required()
def create_order(cust_id):

    data = request.json

    customer_order = data['order']

    customer = Customer.query.filter(Customer.cust_id == cust_id).first()
    if not customer:
        customer = Customer(cust_id)
        db.session.add(customer)

    
    order = Order()
    db.session.add(order)

    for weapon in customer_order:

        #def __init__(self, weap_id, quantity, price, order_id, cust_id):

        weaporder = WeapOrder(weapon['weap_id'], weapon['quantity'], weapon['price'], order.order_id, customer.cust_id)
        db.session.add(weaporder)

        order.increment_ordertotal(weaporder.price)

        current_weapon = Weapon.query.get(weapon['weap_id'])
        current_weapon.decrement_quantity(weapon['quantity'])

    db.session.commit()

    return {
        'status' : 200,
        'message' : 'New Order was Created.'
    }

@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):

    weaporder = WeapOrder.query.filter(WeapOrder.cust_id == cust_id).all()

    data = []

    for order in weaporder:
        weapon = Weapon.query.filter(Weapon.weap_id == order.weap_id).first()

        weapon_dict = weapon_schema.dump(weapon)

        weapon_dict['quantity'] = order.quantity
        weapon_dict['order_id'] = order.order_id
        weapon_dict['id'] = order.weaporder_id

        data.append(weapon_dict)

    return jsonify(data)

@api.route('/order/update/<order_id>', methods = ['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.json
    new_quantity = int(data['quantity'])
    weap_id = data['weap_id']

    weaporder = WeapOrder.query.filter(WeapOrder.order_id == order_id, WeapOrder.weap_id == weap_id).first()
    order = Order.query.get(order_id)
    weapon = Weapon.query.get(weap_id)

    weaporder.set_price(weapon.price, new_quantity)

    diff = abs(new_quantity - weaporder.quantity)

    if weaporder.quantity > new_quantity:
        weapon.increment_quantity(diff)
        order.decrement_ordertotal(weaporder.price)

    elif weaporder.quantity < new_quantity:
        weapon.decrement_quantity(diff)
        order.increment_ordertotal(weaporder.price)

    weaporder.update_quantity(new_quantity)

    db.session.commit()

    return {
        'status': 200,
        'message': 'Order was Update Successfully'
    }

@api.route('/order/delete/<order_id>', methods = ['DELETE'])
@jwt_required()
def delete_order(order_id):
    data = request.json
    weap_id = data['weap_id']

    weaporder = WeapOrder.query.filter(WeapOrder.order_id == order_id, WeapOrder.weap_id == weap_id).first()
    order = Order.query.get(order_id)
    weapon = Weapon.query.get(weap_id)

    order.decrement_ordertotal(weaporder.price)
    weapon.increment_quantity(weaporder.quantity)

    db.session.delete(weaporder)
    db.session.commit()

    return {
        'status': 200,
        'message': 'Order was Deleted Successfully'
    }