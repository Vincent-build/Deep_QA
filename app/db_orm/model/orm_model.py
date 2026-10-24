from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,Text,DateTime,Numeric,text,Date,ForeignKey
from decimal import Decimal
from datetime import datetime,date
from app.db_orm.model.base import Base


class DrugsMySQL(Base):
    __tablename__ = "drugs"

    drug_id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="唯一ID码")
    generic_name:Mapped[str] = mapped_column(String(100),nullable=False,comment="通用名")
    brand_name:Mapped[str] = mapped_column(String(100),comment="商品名")
    approval_number:Mapped[str] = mapped_column(String(50),comment="批准字号")
    specifications:Mapped[str] = mapped_column(String(100),comment="规格")
    dosage_form:Mapped[str] = mapped_column(String(50),comment="剂型(胶囊/片剂/注射液)")
    manufacturer:Mapped[str] = mapped_column(String(100),comment="生产厂家")
    therapeutic_area:Mapped[str] = mapped_column(String(50),comment="治疗领域")
    description:Mapped[str] = mapped_column(Text,comment="药品详情")
    create_at:Mapped[datetime] = mapped_column(DateTime,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    inventory:Mapped["InventoryMySQL"] = relationship(back_populates="drugs")
    sales_records:Mapped["SalesRecordsMySQL"] = relationship(back_populates="drugs")


class InventoryMySQL(Base):
    __tablename__ = "inventory"

    inventory_id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    drug_id:Mapped[int] = mapped_column(Integer,ForeignKey("drugs.drug_id"),nullable=False)
    batch_number:Mapped[str] = mapped_column(String(50),nullable=False,comment="生产批号")
    quantity_on_hand:Mapped[int] = mapped_column(Integer,default=0,comment="当前库存量")
    warehouse_location:Mapped[str] = mapped_column(String(50),comment="仓库位置")
    production_date:Mapped[date] = mapped_column(Date,comment="生产日期")
    expiry_date:Mapped[date] = mapped_column(Date,comment="有效期至")
    last_updated:Mapped[datetime] = mapped_column(DateTime,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    drugs: Mapped["DrugsMySQL"] = relationship(back_populates="inventory")


class SalesRecordsMySQL(Base):
    __tablename__ = "sales_records"

    sale_id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    drug_id:Mapped[int] = mapped_column(Integer,ForeignKey("drugs.drug_id"),nullable=False)
    sale_date:Mapped[date] = mapped_column(Date,nullable=False,comment='销售日期')
    quantity_sold:Mapped[int] = mapped_column(Integer,nullable=False,comment='销售数量')
    unit_price:Mapped[Decimal] = mapped_column(Numeric(10,2),comment='销售单价')
    total_amount:Mapped[Decimal] = mapped_column(Numeric(15,2),comment='销售总额')
    customer_name:Mapped[str] = mapped_column(String(100),comment="客户名称")
    region:Mapped[str] = mapped_column(String(50),comment="销售区域")
    sales_rep:Mapped[str] = mapped_column(String(50),comment="销售代表")

    drugs: Mapped["DrugsMySQL"] = relationship(back_populates="sales_records")





