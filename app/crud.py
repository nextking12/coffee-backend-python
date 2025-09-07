from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from typing import List, Optional

class CoffeeRepository:
    """
    This class combines your CoffeeRepository and CoffeeService from Java
    In Python, we often combine these layers for simpler APIs
    """
    
    def get_coffee_by_id(self, db: Session, coffee_id: int) -> Optional[models.Coffee]:
        """
        Like: Optional<CoffeeEntity> findById(Long id)
        """
        return db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    
    def get_coffee_by_name(self, db: Session, name: str) -> Optional[models.Coffee]:
        """
        Like: Optional<CoffeeEntity> findByName(String name)
        """
        return db.query(models.Coffee).filter(models.Coffee.name == name).first()
    
    def get_all_coffees(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Coffee]:
        """
        Like: List<CoffeeEntity> findAll()
        Added pagination with skip/limit (like Spring Data's Pageable)
        """
        return db.query(models.Coffee).offset(skip).limit(limit).all()
    
    def search_coffees_by_name(self, db: Session, name: str) -> List[models.Coffee]:
        """
        Like: List<CoffeeEntity> findByNameContaining(String name)
        """
        return db.query(models.Coffee).filter(
            models.Coffee.name.ilike(f"%{name}%")
        ).all()
    
    def coffee_exists_by_name(self, db: Session, name: str) -> bool:
        """
        Like: boolean existsByName(String name)
        """
        return db.query(models.Coffee).filter(models.Coffee.name == name).first() is not None
    
    def create_coffee(self, db: Session, coffee: schemas.CoffeeCreate) -> models.Coffee:
        """
        Like your createCoffee method in CoffeeService
        """
        # Check if coffee already exists
        if self.coffee_exists_by_name(db, coffee.name):
            raise ValueError(f"Coffee with name '{coffee.name}' already exists")
        
        # Create new coffee object
        # In Java: new CoffeeEntity(name, type, origin, grindSize, weight)
        db_coffee = models.Coffee(
            name=coffee.name,
            type=coffee.type,
            origin=coffee.origin,
            grind_size=coffee.grind_size,
            weight_in_grams=coffee.weight_in_grams
        )
        
        # Save to database
        # Like: coffeeRepository.save(coffee)
        db.add(db_coffee)
        db.commit()
        db.refresh(db_coffee)  # Get the generated ID
        
        return db_coffee
    
    def update_coffee(self, db: Session, coffee_id: int, coffee_update: schemas.CoffeeUpdate) -> Optional[models.Coffee]:
        """
        Like your updateCoffee method
        """
        db_coffee = self.get_coffee_by_id(db, coffee_id)
        if not db_coffee:
            return None
        
        # Update only provided fields
        # Like your setter methods in the .map() operation
        update_data = coffee_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_coffee, field, value)
        
        db.commit()
        db.refresh(db_coffee)
        return db_coffee
    
    def delete_coffee(self, db: Session, coffee_id: int) -> bool:
        """
        Like: void deleteUser(Long id)
        """
        db_coffee = self.get_coffee_by_id(db, coffee_id)
        if not db_coffee:
            return False
        
        db.delete(db_coffee)
        db.commit()
        return True

# Create instance to use in routes
coffee_repo = CoffeeRepository()