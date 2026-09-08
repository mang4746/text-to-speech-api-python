#from decimal import Decimal
#
#from sqlalchemy import Integer, Numeric, ForeignKey, String
#from sqlalchemy.orm import Mapped, mapped_column, relationship
#
#from app.db.oracle.base import OracleBase
#
#
#class Credito(OracleBase):
#    __tablename__ = "F_CAR_CREDITOS"
#
#    __table_args__ = {
#        "schema": "BDPSAM"
#    }
#
#    sec_credito: Mapped[int] = mapped_column(
#        Integer,
#        primary_key=True,
#    )
#
#    estado: Mapped[str] = mapped_column(
#        String(50),
#    )
#
#    monto_desembolsado: Mapped[Decimal] = mapped_column(
#        Numeric(16, 2),
#    )
#
#    # sec_persona: Mapped[int] = mapped_column(
#    #     ForeignKey("BDPSAM.CLIENTES.sec_persona"),
#    # )
#
#    # cliente = relationship(
#    #     "Cliente",
#    #     back_populates="creditos",
#    # )