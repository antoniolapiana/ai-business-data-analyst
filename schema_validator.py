import sqlglot
from sqlglot import exp


def validate_schema(sql_query, schema):
    valid_columns = {column[1] for column in schema}

    parsed_query = sqlglot.parse_one(sql_query)

    aliases = {
        alias.alias
        for alias in parsed_query.find_all(exp.Alias)
    }

    columns = parsed_query.find_all(exp.Column)

    for column in columns:
        column_name = column.name

        if column_name in aliases:
            continue

        if column_name not in valid_columns:
            raise ValueError(
                f"Column '{column_name}' does not exist in the database schema."
            )