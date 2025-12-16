`sqlpgq` is a Python library for working with SQL/PGQ graph queries.

# Usage
Install the library with `pip install sqlpgq`.

# Example
This example shows how to create a property graph and run a query using DuckDB with the DuckPGQ extension.

## Table Setup
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
);

CREATE TABLE friendships (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    friend_id INTEGER REFERENCES users(id),
    since DATE
);

INSERT INTO users VALUES (1, 'Alice', 30), (2, 'Bob', 25), (3, 'Carol', 35);
INSERT INTO friendships VALUES (1, 1, 2, '2020-01-01'), (2, 2, 3, '2021-06-15');
```

## Generating SQL/PGQ
You can see the output of the instructions below by running `examples/social_network.py` or follow along.

Create a property graph with vertices and edges.
```python
from sqlpgq import PropertyGraph, VertexTable, EdgeTable, Column, Node, Edge, Integer, String, Date

class User(VertexTable):
    __tablename__ = "users"
    __label__ = "Person"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

class Friendship(EdgeTable):
    __tablename__ = "friendships"
    __label__ = "knows"

    __source__ = (Column("user_id"), User)
    __destination__ = (Column("friend_id"), User)
    since = Column(Date)

social = PropertyGraph("social_network", vertices=[User], edges=[Friendship])
```

Create a query.
```python
a = Node("a", "Person")
b = Node("b", "Person")
query = (
    social.query()
    .match(a >> Edge(label="knows") >> b)
    .where(a.name == "Alice")
    .columns(friend_name=b.name)
)
```

Print the generated SQL that you can run in DuckDB.
```python
print(query.to_sql())
```

# Development
- Run the tests with `uv run pytest`
- Run the linter with `uvx ruff check .`
- Run the formatter with `uvx ruff format .`