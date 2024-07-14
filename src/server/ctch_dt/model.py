from sqlalchemy import MetaData, Table, Column, ARRAY, Integer, String, TIMESTAMP

bouquet_metadata = MetaData()


bouquet = Table(
    "bouquet",
    bouquet_metadata,
    Column("id", Integer, primary_key=True),
    Column("bouquet_name", String, nullable=False, unique=True),
    Column("photo_address", String, nullable=False),
    Column("type_flowers", ARRAY(String), nullable=False),
    Column("cost", Integer, nullable=False),
    Column("count", Integer, nullable=False),
    Column("add_at", TIMESTAMP, nullable=False)
)