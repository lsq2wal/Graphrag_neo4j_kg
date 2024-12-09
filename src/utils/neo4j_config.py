import os
from langchain_community.graphs import Neo4jGraph

# 设置 Neo4j 数据库的环境变量
os.environ["NEO4J_URI"] = "neo4j+s://b0b499f9.databases.neo4j.io"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "U5jurRsllfakq5TqvM6-M54bUeE89IHK3WGqMMzVJeY"

# 初始化 Neo4j 图数据库连接
graph = Neo4jGraph()
