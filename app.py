

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

DATABASE_URL = "sqlite:///./shop.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SupplierORM(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    country = Column(String(50), nullable=False)
    products = relationship("ProductORM", back_populates="supplier")


class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    supplier = relationship("SupplierORM", back_populates="products")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SupplierCreate(BaseModel):
    name: str = Field(..., example="TechSupply UA", description="Назва постачальника")
    contact_email: str = Field(..., example="contact@techsupply.ua", description="Email постачальника (унікальний)")
    phone: str = Field(..., example="+380501234567", description="Телефон")
    country: str = Field(..., example="Україна", description="Країна")


class SupplierResponse(SupplierCreate):
    id: int

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str = Field(..., example="Смартфон Galaxy S25", description="Назва товару")
    category: str = Field(..., example="Електроніка", description="Категорія товару")
    price: float = Field(..., gt=0, example=12999.99, description="Ціна (грн)")
    stock_quantity: int = Field(..., ge=0, example=50, description="Кількість на складі")
    supplier_id: int = Field(..., example=1, description="ID постачальника")


class ProductResponse(ProductCreate):
    id: int
    supplier: Optional[SupplierResponse] = None

    class Config:
        from_attributes = True


class ImportResponse(BaseModel):
    imported: int
    message: str


app = FastAPI(
   
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get(
    "/suppliers",
    response_model=list[SupplierResponse],
    tags=["Постачальники"],
    summary="Отримати всіх постачальників",
)
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(SupplierORM).all()


@app.post(
    "/suppliers",
    response_model=SupplierResponse,
    status_code=201,
    tags=["Постачальники"],
    summary="Додати нового постачальника",
)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    existing = db.query(SupplierORM).filter_by(contact_email=payload.contact_email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Постачальник з таким email вже існує")
    supplier = SupplierORM(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@app.get(
    "/suppliers/{supplier_id}",
    response_model=SupplierResponse,
    tags=["Постачальники"],
    summary="Отримати постачальника за ID",
)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(SupplierORM).filter_by(id=supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Постачальника не знайдено")
    return s


@app.delete(
    "/suppliers/{supplier_id}",
    tags=["Постачальники"],
    summary="Видалити постачальника",
)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(SupplierORM).filter_by(id=supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Постачальника не знайдено")
    db.delete(s)
    db.commit()
    return {"detail": f"Постачальника #{supplier_id} видалено"}


# ── Products endpoints ─────────────────────────────────────────────────────────
@app.get(
    "/products",
    response_model=list[ProductResponse],
    tags=["Продукти"],
    summary="Отримати всі продукти",
)
def list_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
):
    q = db.query(ProductORM)
    if category:
        q = q.filter(ProductORM.category == category)
    if min_price is not None:
        q = q.filter(ProductORM.price >= min_price)
    if max_price is not None:
        q = q.filter(ProductORM.price <= max_price)
    return q.all()


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=201,
    tags=["Продукти"],
    summary="Додати новий продукт",
)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    supplier = db.query(SupplierORM).filter_by(id=payload.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Постачальника #{payload.supplier_id} не знайдено")
    product = ProductORM(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    tags=["Продукти"],
    summary="Отримати продукт за ID",
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(ProductORM).filter_by(id=product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    return p


@app.delete(
    "/products/{product_id}",
    tags=["Продукти"],
    summary="Видалити продукт",
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(ProductORM).filter_by(id=product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    db.delete(p)
    db.commit()
    return {"detail": f"Продукт #{product_id} видалено"}


# ── Import endpoint ────────────────────────────────────────────────────────────
@app.post(
    "/import",
    response_model=ImportResponse,
    tags=["Імпорт CSV"],
    summary="Імпортувати дані з data.csv у базу",
    description="Читає файл `data.csv` з поточної директорії та завантажує всі записи в базу. Постачальники дедублікуються за email.",
)
def import_csv(db: Session = Depends(get_db)):
    import csv, os

    file_path = "data.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл data.csv не знайдено. Спочатку запустіть: python generate_csv.py")

    count = 0
    with open(file_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # Дедуплікація постачальника
            supplier = db.query(SupplierORM).filter_by(contact_email=row["supplier_email"]).first()
            if not supplier:
                supplier = SupplierORM(
                    name=row["supplier_name"],
                    contact_email=row["supplier_email"],
                    phone=row["supplier_phone"],
                    country=row["supplier_country"],
                )
                db.add(supplier)
                db.flush()

            db.add(ProductORM(
                name=row["product_name"],
                category=row["product_category"],
                price=float(row["price"]),
                stock_quantity=int(row["stock_quantity"]),
                supplier_id=supplier.id,
            ))
            count += 1

    db.commit()
    return ImportResponse(imported=count, message=f"Успішно імпортовано {count} продуктів з data.csv")


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
def root():
    return HTMLResponse("""
    <html><body style="font-family:sans-serif;max-width:600px;margin:60px auto;text-align:center">
        <h1>🛒 Shop API</h1>
        <p>Відкрий <a href="/docs"><strong>Swagger UI → /docs</strong></a></p>
        <p>Або <a href="/redoc">ReDoc → /redoc</a></p>
    </body></html>
    """)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
