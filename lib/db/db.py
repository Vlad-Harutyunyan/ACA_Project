from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


SQLITE = 'sqlite'
# Table Names
MEALS = 'meals'
AREA = 'area'
INGREDIENT = 'ingredient'
CATEGORIES = 'categories'
MEAL_INGREDIENT = 'meal_ingredient'


class MyDatabase:

    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        DB = dbname
        engine_url = f'sqlite:///{DB}'
        self.db_engine = create_engine(engine_url)

    def create_db_tables(self):
        metadata = MetaData()
        meals = Table(MEALS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String, nullable=False),
                      Column('category_id', String, ForeignKey('categories.id'), nullable=True),
                      Column('area_id', String, ForeignKey('area.id'),nullable=True),
                      Column ('like_count', Integer,nullable=True),
                      Column('instructions', String,nullable=True),
                      Column('img_link', String,nullable=True),
                      Column('tags',String,nullable=True),
                      Column ('video_link',String,nullable=True))
        area = Table(AREA, metadata,
                     Column('id', Integer, primary_key=True),
                     Column ('name',String,nullable=True),)
        ingredient = Table(INGREDIENT, metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String, nullable=True),
                           Column('description', String, nullable=True),)
        categories = Table(CATEGORIES, metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String, nullable=True),
                           Column('img_link', String, nullable=True),
                           Column('description', String, nullable=True), )
        meal_ingredient=Table(MEAL_INGREDIENT, metadata,
                              Column('id', Integer,primary_key=True,autoincrement=True),
                              Column("meal_id", Integer, nullable=True),
                              Column ("ingredient_id",Integer))

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '': return
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()
        print("\n")

    def sample_query(self, query):
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                res = []
                for row in result:
                    res.append(row)
                return res

    def sample_delete(self, table):
        query = "DELETE FROM {}".format(table)
        # query = "DELETE FROM {} WHERE id=3".format(MEALS)
        self.execute_query(query)

    def sample_insert(self, query):
        # Insert Data
        self.execute_query(query)


    def sample_update(self):
        # Update Data
        query = "UPDATE {} set first_name='XXXX' WHERE id={id}" \
            .format(USERS, id=3)
        self.execute_query(query)

    def delete_table_data(self, table):
        query = f'DELETE FROM {table}'
        self.execute_query(query)

    def delete_table(self, table):
        query = f'DROP TABLE IF EXISTS {table};'
        self.execute_query(query)


