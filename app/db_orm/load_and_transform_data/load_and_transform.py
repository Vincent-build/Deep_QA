from app.db_orm.entity.entity import Drugs,Inventory,SalesRecords
from app.db_orm.model.orm_model import DrugsMySQL,InventoryMySQL,SalesRecordsMySQL
from app.db_orm.update_data.datas import drugs_list,inventory_list,salesrecord_list
from app.db_orm.establish_orm_operation.mysql_operator import mysql_operated
from dataclasses import asdict
import asyncio



def load_data():
    print("开始加载数据")
    drug_data_list:list[Drugs] = []

    drug_transform:list[Drugs] = [Drugs(
            drug_id=None,
            generic_name=drug[0],
            brand_name=drug[1],
            approval_number=drug[2],
            specifications=drug[3],
            dosage_form=drug[4],
            manufacturer=drug[5],
            therapeutic_area=drug[6],
            description=drug[7],
            create_at=None,
        ) for drug in drugs_list]

    drug_data_list.extend(drug_transform)

    inventory_data_list:list[Inventory] = []

    inventory_transform:list[Inventory] = [Inventory(
        inventory_id=None,
        drug_id=inventory[0],
        batch_number=inventory[1],
        quantity_on_hand=inventory[2],
        warehouse_location=inventory[3],
        production_date=inventory[4],
        expiry_date=inventory[5],
        last_updated=None,
    ) for inventory in inventory_list]


    inventory_data_list.extend(inventory_transform)

    salesrecord_data_list:list[SalesRecords] = []

    salesrecord_transform:list[SalesRecords] = [SalesRecords(
        sale_id=None,
        drug_id=salesrecord[0],
        sale_date=salesrecord[1],
        quantity_sold=salesrecord[2],
        unit_price=salesrecord[3],
        total_amount=salesrecord[4],
        customer_name=salesrecord[5],
        region=salesrecord[6],
        sales_rep=salesrecord[7],
    ) for salesrecord in salesrecord_list]

    salesrecord_data_list.extend(salesrecord_transform)

    return {"drug":drug_data_list,"inventory":inventory_data_list,"salesrecord":salesrecord_data_list}


def drug_to_model(data_list:list[Drugs])->list[DrugsMySQL]:
    print("drug数据转换")
    return [DrugsMySQL(**asdict(data)) for data in data_list]

def inventory_to_model(data_list:list[Inventory])->list[InventoryMySQL]:
    print("inventory数据转换")
    return [InventoryMySQL(**asdict(data)) for data in data_list]

def salesrecord_to_model(data_list:list[SalesRecords])->list[SalesRecordsMySQL]:
    print("salesrecord数据转换")
    return [SalesRecordsMySQL(**asdict(data)) for data in data_list]



async def update_data_to_mysql():

    data_dict = load_data()

    drug_list = data_dict.get("drug")
    inventory_list = data_dict.get("inventory")
    salesrecord_list = data_dict.get("salesrecord")

    drug_model_list = drug_to_model(drug_list)
    inventory_model_list = inventory_to_model(inventory_list)
    salesrecord_model_list = salesrecord_to_model(salesrecord_list)

    mysql_operated.check_table()

    await mysql_operated.update_data(drug_model_list)
    await mysql_operated.update_data(inventory_model_list)
    await mysql_operated.update_data(salesrecord_model_list)

    return "数据写入完成"


if __name__ == "__main__":
    asyncio.run(update_data_to_mysql())





