import sqlalchemy

db = sqlalchemy.create_engine("postgresql+psycopg2://cocollector:12345678@192.168.84.71/BDCocoProyecto")

db.connect()
print(db)