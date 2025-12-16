"""Example: Social Network Graph Queries"""

from sqlpgq import (
    PropertyGraph,
    VertexTable,
    EdgeTable,
    Column,
    Node,
    Edge,
    Integer,
    String,
    Date,
)


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

print("=" * 60)
print("CREATE PROPERTY GRAPH")
print("=" * 60)
print(social.create_statement())
print()

print("=" * 60)
print("Find Alice's friends")
print("=" * 60)
a = Node("a", "Person")
b = Node("b", "Person")

query = (
    social.query()
    .match(a >> Edge(label="knows") >> b)
    .where(a.name == "Alice")
    .columns(friend_name=b.name)
)
print(query.to_sql())
print()

print("=" * 60)
print("Friends of friends")
print("=" * 60)
a = Node("a", "Person")
b = Node("b", "Person")
c = Node("c", "Person")

query = (
    social.query()
    .match(
        a >> Edge(label="knows") >> b,
        b >> Edge(label="knows") >> c,
    )
    .where(a.name == "Alice")
    .where(a.id != c.id)
    .columns(friend_of_friend=c.name)
)
print(query.to_sql())
print()

print("=" * 60)
print("Variable-length path (1-3 hops)")
print("=" * 60)
a = Node("a", "Person")
b = Node("b", "Person")

query = (
    social.query()
    .match(a >> Edge(label="knows").repeat(1, 3) >> b)
    .where(a.name == "Alice")
    .columns(reachable=b.name)
)
print(query.to_sql())
print()

print("=" * 60)
print("Edge properties (friendship date)")
print("=" * 60)
a = Node("a", "Person")
b = Node("b", "Person")
e = Edge(alias="e", label="knows")

query = (
    social.query()
    .match(a >> e >> b)
    .where(a.name == "Alice")
    .columns(friend=b.name, since=e.since)
)
print(query.to_sql())
