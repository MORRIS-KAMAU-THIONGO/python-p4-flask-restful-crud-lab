from app import app, db, Plant

with app.app_context():
    # Delete all existing plants
    Plant.query.delete()
    
    # Add some sample plants
    plants = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.5, is_in_stock=True),
        Plant(name="Ficus", image="./images/ficus.jpg", price=25.0, is_in_stock=True),
        Plant(name="Monstera", image="./images/monstera.jpg", price=45.0, is_in_stock=True)
    ]
    
    db.session.bulk_save_objects(plants)
    db.session.commit()
    print("Database seeded successfully!")
