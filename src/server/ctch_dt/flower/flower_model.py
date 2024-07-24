from sqlalchemy import MetaData, Table, Column, Integer, String

flower_metadata = MetaData()


flower = Table(
    "flower",
    flower_metadata,
    Column("id", Integer, primary_key=True),
    Column("flower", String, unique=True)
)