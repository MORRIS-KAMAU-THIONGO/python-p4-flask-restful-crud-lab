from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from models import db, Plant

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
api = Api(app)

class PlantById(Resource):
    def get(self, id):
        """Get a single plant by ID"""
        plant = Plant.query.get(id)
        if plant is None:
            abort(404, description="Plant not found")
        
        return plant.to_dict(), 200

    def patch(self, id):
        """Update a plant (primarily is_in_stock field)"""
        plant = Plant.query.get(id)
        if plant is None:
            abort(404, description="Plant not found")
        
        data = request.get_json()
        
        # The frontend only ever sends {"is_in_stock": true/false}, so we only update that field
        # This matches the lab example exactly
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
        
        db.session.add(plant)
        db.session.commit()
        
        return plant.to_dict(), 200

    def delete(self, id):
        """Delete a plant from the database"""
        plant = Plant.query.get(id)
        if plant is None:
            abort(404, description="Plant not found")
        
        db.session.delete(plant)
        db.session.commit()
        
        # Return empty response with 204 status code
        return '', 204

# Register the resource
api.add_resource(PlantById, '/plants/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    app.run(port=5555, debug=True)
