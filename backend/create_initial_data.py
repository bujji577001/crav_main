from app import app
from backend.extensions import db
from backend.security import user_datastore
from backend.models import Restaurant, Category, MenuItem, User, Role

def create_data():
    """Function to create initial roles, users, and sample data."""
    with app.app_context():
        db.create_all()
        
        # --- 1. Find or create roles ---
        admin_role = user_datastore.find_or_create_role(name='admin', description='Superuser')
        customer_role = user_datastore.find_or_create_role(name='customer', description='General customer')
        owner_role = user_datastore.find_or_create_role(name='owner', description='Restaurant owner')

        # --- 2. Commit the roles to the database FIRST ---
        db.session.commit()

        # --- 3. Find/Create users and THEN add roles (CORRECTED LOGIC) ---
        
        # Admin User
        admin_user = user_datastore.find_user(email='admin@email.com')
        if not admin_user:
            # Create user *without* roles first
            admin_user = user_datastore.create_user(email='admin@email.com', password='admin123')
            db.session.commit() # Commit the new user
            
            # Now, find the user we just created and add the role
            admin_user_to_update = user_datastore.find_user(email='admin@email.com')
            user_datastore.add_role_to_user(admin_user_to_update, admin_role)
            
        elif not admin_user.has_role('admin'):
            user_datastore.add_role_to_user(admin_user, admin_role)

        # Customer User
        customer_user = user_datastore.find_user(email='customer1@email.com')
        if not customer_user:
            customer_user = user_datastore.create_user(email='customer1@email.com', password='cust123')
            db.session.commit() # Commit the new user
            
            customer_user_to_update = user_datastore.find_user(email='customer1@email.com')
            user_datastore.add_role_to_user(customer_user_to_update, customer_role)
        elif not customer_user.has_role('customer'):
            user_datastore.add_role_to_user(customer_user, customer_role)

        # Owner User
        owner_user = user_datastore.find_user(email='owner1@email.com')
        if not owner_user:
            owner_user = user_datastore.create_user(email='owner1@email.com', password='owner123')
            db.session.commit() # Commit the new user
            
            owner_user_to_update = user_datastore.find_user(email='owner1@email.com')
            user_datastore.add_role_to_user(owner_user_to_update, owner_role)
        elif not owner_user.has_role('owner'):
             user_datastore.add_role_to_user(owner_user, owner_role)
        
        # --- This commit saves all the user/role changes ---
        db.session.commit()

        # --- The rest of your script for creating restaurant data ---
        owner_user_from_db = user_datastore.find_user(email='owner1@email.com')
        if owner_user_from_db and not Restaurant.query.filter_by(owner_id=owner_user_from_db.id).first():
            new_resto = Restaurant(
                owner_id=owner_user_from_db.id,
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
