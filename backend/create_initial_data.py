from app import app
from backend.extensions import db
from backend.security import user_datastore
from backend.models import Restaurant, Category, MenuItem

def create_data():
    """Function to create initial roles, users, and sample data."""
    with app.app_context():
        db.create_all()
        
        # --- FIX 1: Find or create roles and SAVE THEM to variables ---
        admin_role = user_datastore.find_or_create_role(name='admin', description='Superuser')
        customer_role = user_datastore.find_or_create_role(name='customer', description='General customer')
        owner_role = user_datastore.find_or_create_role(name='owner', description='Restaurant owner')

        # --- FIX 2: Commit the roles to the database FIRST ---
        db.session.commit()

        # --- FIX 3: Find users and ADD ROLES if they are missing ---
        
        # Admin User
        admin_user = user_datastore.find_user(email='admin@email.com')
        if not admin_user:
            admin_user = user_datastore.create_user(email='admin@email.com', password='admin123', roles=[admin_role])
        elif not user_datastore.has_role(admin_user, 'admin'):
            user_datastore.add_role_to_user(admin_user, admin_role)

        # Customer User
        customer_user = user_datastore.find_user(email='customer1@email.com')
        if not customer_user:
            customer_user = user_datastore.create_user(email='customer1@email.com', password='cust123', roles=[customer_role])
        elif not user_datastore.has_role(customer_user, 'customer'):
            user_datastore.add_role_to_user(customer_user, customer_role)

        # Owner User
        owner_user = user_datastore.find_user(email='owner1@email.com')
        if not owner_user:
            owner_user = user_datastore.create_user(email='owner1@email.com', password='owner123', roles=[owner_role])
        elif not user_datastore.has_role(owner_user, 'owner'):
            user_datastore.add_role_to_user(owner_user, owner_role)
        
        # --- This commit saves the user/role changes ---
        db.session.commit()

        # --- The rest of your script is perfectly fine ---
        if owner_user and not Restaurant.query.filter_by(owner_id=owner_user.id).first():
            new_resto = Restaurant(
                owner_id=owner_user.id,
                name="Owner One's Eatery",
                description="A default restaurant for testing.",
                address="123 Food St",
                city="Flavor Town",
                latitude=40.7128,
                longitude=-74.0060,
                is_verified=True 
            )
            db.session.add(new_resto)
            db.session.commit()

            if not Category.query.filter_by(restaurant_id=new_resto.id).first():
                cat1 = Category(name="Appetizers", restaurant_id=new_resto.id)
                cat2 = Category(name="Main Courses", restaurant_id=new_resto.id)
                db.session.add_all([cat1, cat2])
                db.session.commit()

                item1 = MenuItem(name="Spring Rolls", description="Crispy fried rolls with vegetable filling.", price=5.99, category_id=cat1.id, restaurant_id=new_resto.id)
                item2 = MenuItem(name="House Burger", description="Juicy beef patty with cheese and fresh vegetables.", price=12.99, category_id=cat2.id, restaurant_id=new_resto.id)
                item3 = MenuItem(name="Pasta Carbonara", description="Creamy pasta with bacon and parmesan.", price=15.50, category_id=cat2.id, restaurant_id=new_resto.id)
                db.session.add_all([item1, item2, item3])
        
        db.session.commit()
        print("Initial data created/updated successfully.")

if __name__ == '__main__':
    create_data()

