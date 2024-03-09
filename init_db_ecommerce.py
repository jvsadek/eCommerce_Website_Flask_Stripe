from datetime import date
from main import db, Product, app

def create_app():
    with app.app_context():
        e1 = Product( product_name='Laptop',
                      product_image='./static/img/product01.png',
                      product_category = 'Laptop',
                      product_price=560,
                      product_old_price=590,
                      product_currency = '$',
                      product_rating=5,
                      )

        e2 = Product( product_name='Headset',
                      product_image='./static/img/product02.png',
                      product_category='Laptop',
                      product_price=120,
                      product_old_price=150,
                      product_currency='$',
                      product_rating=4,
                      )

        e3 = Product( product_name='Laptop',
                      product_image='./static/img/product03.png',
                      product_category='Laptop',
                      product_price=1200,
                      product_old_price=1500,
                      product_currency='$',
                      product_rating=3,
                      )

        e4 = Product( product_name='Tablet',
                      product_image='./static/img/product04.png',
                      product_category='Laptop',
                      product_price=550,
                      product_old_price=600,
                      product_currency='$',
                      product_rating=5,
                      )

        e5 = Product( product_name='Headset',
                      product_image='./static/img/product05.png',
                      product_category='Headset',
                      product_price=80,
                      product_old_price=90,
                      product_currency='$',
                      product_rating=4,
                      )

        e6 = Product( product_name='Laptop',
                      product_image='./static/img/product06.png',
                      product_category='Laptop',
                      product_price=670,
                      product_old_price=720,
                      product_currency='$',
                      product_rating=5,
                      )

        e7 = Product( product_name='Mobile',
                      product_image='./static/img/product07.png',
                      product_category='Mobile',
                      product_price=800,
                      product_old_price=920,
                      product_currency='$',
                      product_rating=5,
                      )

        e8 = Product( product_name='Laptop',
                      product_image='./static/img/product08.png',
                      product_category='Mobile',
                      product_price=670,
                      product_old_price=770,
                      product_currency='$',
                      product_rating=5,
                      )

        e9 = Product( product_name='Camera',
                      product_image='./static/img/product09.png',
                      product_category='Mobile',
                      product_price=450,
                      product_old_price=550,
                      product_currency='$',
                      product_rating=3,
                      )
        db.drop_all()
        db.create_all()
        db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9])
        db.session.commit()

    return app

create_app()