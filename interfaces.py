from abc import ABC, abstractmethod


class IRepository(ABC):

    @abstractmethod
    def read_csv(self, file_path: str):
        pass

    @abstractmethod
    def save_supplier_with_product(self, supplier_dict: dict, product_dict: dict):
        pass

    @abstractmethod
    def get_all_products(self):
        pass

    @abstractmethod
    def get_all_suppliers(self):
        pass


class IPresentationLayer(ABC):

    @abstractmethod
    def display_products(self, products):
        pass

    @abstractmethod
    def display_suppliers(self, suppliers):
        pass
