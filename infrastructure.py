import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Supplier, Product
from interfaces import IRepository


class SqliteRepository(IRepository):

    def __init__(self, db_url: str = "sqlite:///shop.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # ── CSV reading ────────────────────────────────────────────────────────────
    def read_csv(self, file_path: str) -> list[dict]:
        """Зчитує рядки з CSV-файлу та повертає список словників"""
        data = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    # ── Write ──────────────────────────────────────────────────────────────────
    def save_supplier_with_product(self, supplier_dict: dict, product_dict: dict):
       
        session = self.Session()
        try:
            existing = (
                session.query(Supplier)
                .filter_by(contact_email=supplier_dict['contact_email'])
                .first()
            )
            if existing:
                supplier = existing
            else:
                supplier = Supplier(
                    name=supplier_dict['name'],
                    contact_email=supplier_dict['contact_email'],
                    phone=supplier_dict['phone'],
                    country=supplier_dict['country'],
                )
                session.add(supplier)
                session.flush()  # Отримуємо supplier.id до commit

            product = Product(
                name=product_dict['name'],
                category=product_dict['category'],
                price=float(product_dict['price']),
                stock_quantity=int(product_dict['stock_quantity']),
                supplier_id=supplier.id,
            )
            session.add(product)
            session.commit()
        except Exception as exc:
            session.rollback()
            print(f"[ERROR] save_supplier_with_product: {exc}")
        finally:
            session.close()

    def get_all_products(self) -> list[Product]:
        session = self.Session()
        products = session.query(Product).all()
        session.close()
        return products

    def get_all_suppliers(self) -> list[Supplier]:
        session = self.Session()
        suppliers = session.query(Supplier).all()
        session.close()
        return suppliers
