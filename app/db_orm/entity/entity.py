from dataclasses import dataclass
from datetime import datetime,date
from decimal import Decimal


@dataclass
class Drugs:
    drug_id: int | None
    generic_name: str
    brand_name: str
    approval_number: str
    specifications: str
    dosage_form: str
    manufacturer: str
    therapeutic_area: str
    description: str
    create_at: datetime | None


@dataclass
class Inventory:
    inventory_id: int | None
    drug_id: int
    batch_number: str
    quantity_on_hand: int
    warehouse_location: str
    production_date: date
    expiry_date: date
    last_updated: datetime | None


@dataclass
class SalesRecords:
    sale_id: int | None
    drug_id: int
    sale_date: date
    quantity_sold: int
    unit_price: Decimal
    total_amount: Decimal
    customer_name: str
    region: str
    sales_rep: str



