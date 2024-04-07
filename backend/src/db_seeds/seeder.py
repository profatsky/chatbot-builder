import asyncio
import json
import os

from sqlalchemy import text, TextClause
from sqlalchemy.exc import IntegrityError, DBAPIError

from src.core.db import async_session_maker


def get_json_file_paths(directory: str):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


def get_jsons_from_files(file_paths: list[str]) -> list[dict]:
    jsons_from_files = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            jsons_from_files.append(data)
    return jsons_from_files


def transform_jsons_to_sql_inserts(jsons: list[dict]) -> list[TextClause]:
    sql_inserts = []

    for seed in jsons:
        data = seed['data']

        columns = list(data[0].keys())

        sql_values_rows = []
        for json_item in data:
            values = json_item.values()

            sql_values_row = (
                    '(' + ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in values) + ')'
            )
            sql_values_rows.append(sql_values_row)

        columns_to_sql = ', '.join(columns)

        '''
        A separate insert is created for each set of values. When adding data at once in one insert, 
        a conflict may occur, which will cause no query to be executed.
        '''
        for row in sql_values_rows:
            sql = text(f'''
                INSERT INTO {seed['tablename']} ({columns_to_sql}) VALUES {row}
            ''')
            sql_inserts.append(sql)

    return sql_inserts


async def insert_data(sql_inserts: list[TextClause]):
    async with async_session_maker() as session:
        for sql_insert in sql_inserts:
            try:
                await session.execute(sql_insert)
                await session.commit()
            except (IntegrityError, DBAPIError):
                pass



async def main():
    file_paths = get_json_file_paths('data/')
    jsons_from_files = get_jsons_from_files(file_paths)
    sql_inserts = transform_jsons_to_sql_inserts(jsons_from_files)
    await insert_data(sql_inserts)


if __name__ == '__main__':
    asyncio.run(main())
