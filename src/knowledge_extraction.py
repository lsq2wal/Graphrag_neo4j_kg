import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from langchain_community.graphs.graph_document import GraphDocument
from langchain_core.documents import Document
from src.utils.neo4j_config import graph

def process_text(text, graph_transformer):
    doc = Document(page_content=text)
    return graph_transformer.convert_to_graph_documents([doc])

def extract_knowledge_from_csv(csv_path, graph_transformer):
    graph_documents = []
    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    MAX_WORKERS = 2
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务并创建 future 对象列表
        futures = [
            executor.submit(process_text, row['cleaned_text'], graph_transformer)
            for row in rows
        ]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing documents"):
            graph_document = future.result()
            print(graph_document)
            graph_documents.extend(graph_document)
            # 打印 future 的结果
            print(f"Nodes:{graph_documents[0].nodes}")
            print(f"Relationships:{graph_documents[0].relationships}")


    # 将提取的图谱文档添加到图数据库中
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True
    )

