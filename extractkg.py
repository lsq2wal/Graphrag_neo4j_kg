import os
import re
import glob
import csv
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.llms import Ollama
from langchain_ollama import ChatOllama
from langchain_community.graphs.graph_document import GraphDocument
from langchain_core.documents import Document
from langchain_community.graphs import Neo4jGraph

# 设置 Neo4j 数据库的环境变量
os.environ["NEO4J_URI"] = "neo4j+s://b0b499f9.databases.neo4j.io"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "U5jurRsllfakq5TqvM6-M54bUeE89IHK3WGqMMzVJeY"

# 初始化 Neo4j 图数据库连接
graph = Neo4jGraph()

# 读取多个生物学文献文本内容并进行预处理，并存储到 CSV 文件中
def process_and_store_biology_texts(directory_path, output_csv_path):
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['file_name', 'cleaned_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for file_path in glob.glob(os.path.join(directory_path, "*.txt")):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            # 简单的文本清理，例如移除多余的空格和特殊字符
            cleaned_text = re.sub(r'\s+', ' ', text)
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,]', '', cleaned_text)
            
            # 写入 CSV 文件
            writer.writerow({'file_name': os.path.basename(file_path), 'cleaned_text': cleaned_text})

# 生物学文献文件夹路径
biology_texts_directory = "/home/share/huadjyin/home/liushiqiang/GraphRAG_neo4j_KG/data/biology_texts"
# 输出 CSV 文件路径
output_csv_path = "/home/share/huadjyin/home/liushiqiang/GraphRAG_neo4j_KG/data/output/biology_texts.csv"

# 处理多个生物学文献文本并存储到 CSV 文件中
process_and_store_biology_texts(biology_texts_directory, output_csv_path)

# 初始化 LLM 模型，使用本地部署的 Llama 3.1 模型
# llm = Ollama(
#     model="llama3.1",
#     base_url="http://localhost:11434"  # 本地 Ollama 服务的 URL
# )

llm = ChatOllama(
    model="llama3.1",
    temperature=0.5,
    base_url="http://localhost:11434"  # 本地 Ollama 服务的 URL

)

# 初始化 LLM-Graph-Transformer
# 修改节点和关系属性以更适合生物学领域的知识提取
graph_transformer = LLMGraphTransformer(
    llm=llm,
    node_properties=[
        "gene_name", "function", "expression_level", "location",  # 基因属性
        "protein_name", "structure", "interaction",  # 蛋白质属性
        "cell_type", "function", "lineage",  # 细胞类型属性
        "disease_name", "classification", "pathology",  # 疾病属性
        "variant_id", "gene_position", "variant_type",  # 变异属性
        "marker_name", "marker_type",  # 分子标记属性
        "drug_name", "target", "mechanism"  # 药物属性
    ],
    relationship_properties=[
        "interaction_type", "evidence", "confidence",  # 基因-基因关系
        "expression_regulation", "functional_relationship",  # 基因-蛋白质关系
        "binding_type", "binding_location",  # 蛋白质-蛋白质关系
        "association_type", "clinical_significance", "variant_info",  # 基因-疾病关系
        "clinical_relevance", "association_strength",  # 变异-疾病关系
        "marker_expression", "marker_category",  # 细胞类型-标记关系
        "target", "treatment_effect", "mechanism"  # 药物-疾病和基因-药物关系
    ]
)

# 定义图谱提取函数
def process_text(text: str) -> List[GraphDocument]:
    doc = Document(page_content=text)
    return graph_transformer.convert_to_graph_documents([doc])

# 并行化请求，加速提取过程，并将结果存储到图数据库中
def extract_knowledge_from_csv(csv_path):
    graph_documents = []
    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        print(rows)
        
    MAX_WORKERS = 2
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务并创建 future 对象列表
        futures = [
            executor.submit(process_text, row['cleaned_text'])
            for row in rows
        ]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing documents"):
            graph_document = future.result()
            graph_documents.extend(graph_document)

    # 将提取的图谱文档添加到图数据库中
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True
    )

# 从 CSV 文件中提取知识并生成图谱
extract_knowledge_from_csv(output_csv_path)

# # 查询知识图谱中的特定节点
# response = graph_transformer.query(
#     node_id="12345",  # 示例节点 ID
#     query="Describe this biological entity and its relationships in the graph"
# )

# # 输出描述信息
# print(response)
