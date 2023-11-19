from flask import Blueprint, flash, redirect, render_template, request


#internal import
from homework_shop.models import Weapon, Customer, Order, db
from homework_shop.forms import WeaponForm


#need to instantiate our Blueprint class
site = Blueprint('site', __name__, template_folder='site_templates' )


#use site object to create our routes
@site.route('/')
def shop():
    
    allweaps = Weapon.query.all()
    allcustomers = Customer.query.all()
    allorders= Order.query.all()

    shop_stats = {
        'weapons' : len(allweaps),
        'sales' : sum([order.order_total for order in allorders]),
        'customers' : len(allcustomers)
    }
    return render_template('shop.html', shop=allweaps, stats=shop_stats) #looking inside our template_folder (site_template) to find the shop.html file


@site.route('/shop/create', methods=['GET', 'POST'])
def create():

    createform = WeaponForm()

    if request.method == 'POST' and createform.validate_on_submit():
        name = createform.name.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data


        weapon = Weapon(name, price, quantity, image, description)

        db.session.add(weapon)
        db.session.commit()

        flash(f"You have successfully added weapon {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your requets", category='warning')
        return redirect('/shop/create')
    
    return render_template('create.html', form=createform)

@site.route('/shop/update/<id>', methods=['GET', 'POST'])
def update(id):

    weapon = Weapon.query.get(id)
    updateform = WeaponForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        weapon.name = updateform.name.data
        weapon.image = updateform.image.data
        weapon.description = updateform.description.data
        weapon.price = updateform.price.data
        weapon.quantity - updateform.quantity.data

        db.session.commit()

        flash(f"You have successfully updated weapon {weapon.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/')
    
    return render_template('update.html', form=updateform, weapon=weapon)


@site.route('/shop/delete/<id>')
def delete(id):

    weapon = Weapon.query.get(id)

    db.session.delete(weapon)
    db.session.commit()

    return redirect('/')



