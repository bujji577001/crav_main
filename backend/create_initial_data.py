# --- DO NOT IMPORT APP HERE ---
from .models import db, User, Role, Restaurant, Category, MenuItem
from .security import user_datastore
import sys

def create_roles(ds):
    """Finds or creates the 'admin', 'owner', and 'customer' roles."""
    print("Finding or creating roles...")
    roles_to_create = {
        "admin": "Full administrative access",
        "owner": "Restaurant owner access",
        "customer": "Customer access"
    }
    
    role_objects = {}
    for role_name, role_desc in roles_to_create.items():
        role = ds.find_role(role_name)
        if not role:
            role = ds.create_role(name=role_name, description=role_desc)
            print(f"Role '{role_name}' created.")
        role_objects[role_name] = role
        
    db.session.commit()
    print("Roles check/creation complete.")
    return role_objects

def create_users_and_data(ds, roles):
    """Finds or creates default users and sample restaurant data."""
    
    print("Finding or creating users...")
    
    # Admin User
    admin_email = "admin@crav.com"
    if not ds.find_user(email=admin_email):
        ds.create_user(
            email=admin_email,
            password="admin123",
            name="Admin User",
            roles=[roles["admin"]] # Pass the role object directly
        )
        print(f"Admin user '{admin_email}' created.")

    # Owner User
    owner_email = "owner1@email.com"
    owner_user = ds.find_user(email=owner_email)
    if not owner_user:
        owner_user = ds.create_user(
            email=owner_email,
            password="owner123",
            name="Owner One",
            roles=[roles["owner"]]
        )
        print(f"Owner user '{owner_email}' created.")
    
    # Customer User
    cust_email = "customer1@email.com"
    if not ds.find_user(email=cust_email):
        ds.create_user(
            email=cust_email,
            password="cust123",
            name="Customer One",
            roles=[roles["customer"]]
        )
        print(f"Customer user '{cust_email}' created.")
    
    db.session.commit()
    print("Users check/creation complete.")

    # --- Create Restaurant Data ---
    # Re-fetch owner_user to ensure we have the ID, even if just created
    owner_user = ds.find_user(email=owner_email) 

    print("Finding or creating sample restaurant data...")
    if owner_user and not Restaurant.query.filter_by(owner_id=owner_user.id).first():
        new_resto = Restaurant(
            owner_id=owner_user.id,
            name="Owner One's Eatery",
            description="A default restaurant for testing.",
            address="123 Food St",
            city="Flavor Town",
            latitude=40.7128,
            longitude=-74.0060,
            is_verified=True,
            is_active=True
        )
        db.session.add(new_resto)
        db.session.commit()
        print(f"Restaurant '{new_resto.name}' created.")

        # Create Categories
        cat1 = Category(name="Appetizers", restaurant_id=new_resto.id)
        cat2 = Category(name="Main Courses", restaurant_id=new_resto.id)
        db.session.add_all([cat1, cat2])
        db.session.commit()
        print("Sample categories created.")

        # Create Menu Items
        item1 = MenuItem(name="Spring Rolls", description="Crispy fried rolls with vegetable filling.", price=5.99, category_id=cat1.id, restaurant_id=new_resto.id, food_type='Veg')
        item2 = MenuItem(name="House Burger", description="Juicy beef patty with cheese and fresh vegetables.", price=12.99, category_id=cat2.id, restaurant_id=new_resto.id, food_type='Non-Veg')
        item3 = MenuItem(name="Pasta Carbonara", description="Creamy pasta with bacon and parmesan.", price=15.50, category_id=cat2.id, restaurant_id=new_resto.id, food_type='Non-Veg')
        db.session.add_all([item1, item2, item3])
        db.session.commit()
        print("Sample menu items created.")
    else:
        print("Sample restaurant data already exists or owner not found.")

def init_app(app):
    """
    Main function to initialize data. 
    This is called by our temporary route.
    """
    with app.app_context():
        try:
            print("--- Starting Initial Data Setup ---")
            # Ensure all tables are created
            db.create_all() 
            roles = create_roles(user_datastore)
            create_users_and_data(user_datastore, roles)
            print("--- Data Setup Complete ---")
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            db.session.rollback()
