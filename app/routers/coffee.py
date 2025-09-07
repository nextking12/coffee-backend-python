from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, database

# Create router - like @RestController @RequestMapping("/api/coffee")
router = APIRouter(
    prefix="/api/coffee",
    tags=["coffee"]
)

@router.get("/", response_model=List[schemas.CoffeeResponse])
def get_all_coffees(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    """
    GET /api/coffee - Get all coffees
    Like: @GetMapping public ResponseEntity<List<CoffeeEntity>> getAllCoffees()
    """
    coffees = crud.coffee_repo.get_all_coffees(db, skip=skip, limit=limit)
    return coffees

@router.get("/{coffee_id}", response_model=schemas.CoffeeResponse)
def get_coffee_by_id(coffee_id: int, db: Session = Depends(database.get_db)):
    """
    GET /api/coffee/{id} - Get coffee by ID
    Like: @GetMapping("/{id}") public ResponseEntity<CoffeeEntity> getCoffeeById(@PathVariable Long id)
    """
    coffee = crud.coffee_repo.get_coffee_by_id(db, coffee_id)
    if not coffee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coffee with id {coffee_id} not found"
        )
    return coffee

@router.get("/search/{name}", response_model=List[schemas.CoffeeResponse])
def search_coffees(name: str, db: Session = Depends(database.get_db)):
    """
    GET /api/coffee/search/{name} - Search coffees by name
    Like: @GetMapping("/search") public ResponseEntity<List<CoffeeEntity>> searchUsers(@RequestParam String name)
    """
    coffees = crud.coffee_repo.search_coffees_by_name(db, name)
    return coffees

@router.post("/", response_model=schemas.CoffeeResponse, status_code=status.HTTP_201_CREATED)
def create_coffee(coffee: schemas.CoffeeCreate, db: Session = Depends(database.get_db)):
    """
    POST /api/coffee - Create new coffee
    Like: @PostMapping public ResponseEntity<CoffeeEntity> createCoffee(@Valid @RequestBody CoffeeEntity coffee)
    """
    try:
        created_coffee = crud.coffee_repo.create_coffee(db, coffee)
        return created_coffee
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.put("/{coffee_id}", response_model=schemas.CoffeeResponse)
def update_coffee(
    coffee_id: int, 
    coffee_update: schemas.CoffeeUpdate, 
    db: Session = Depends(database.get_db)
):
    """
    PUT /api/coffee/{id} - Update coffee
    Like: @PutMapping("/{id}") public ResponseEntity<CoffeeEntity> updateCoffee(@PathVariable Long id, @Valid @RequestBody CoffeeEntity coffeeDetails)
    """
    updated_coffee = crud.coffee_repo.update_coffee(db, coffee_id, coffee_update)
    if not updated_coffee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coffee with id {coffee_id} not found"
        )
    return updated_coffee

@router.delete("/{coffee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coffee(coffee_id: int, db: Session = Depends(database.get_db)):
    """
    DELETE /api/coffee/{id} - Delete coffee
    Like: @DeleteMapping("/{id}") public ResponseEntity<Void> deleteCoffee(@PathVariable Long id)
    """
    success = crud.coffee_repo.delete_coffee(db, coffee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coffee with id {coffee_id} not found"
        )
    # FastAPI automatically returns 204 No Content