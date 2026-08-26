def validate_sql(sql_query):
    sql = sql_query.strip().lower()

    if not sql.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    return True