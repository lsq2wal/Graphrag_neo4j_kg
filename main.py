from src.data_processing import process_and_store_biology_texts
from src.llm_initializer import initialize_llm
from src.graph_transformer import initialize_graph_transformer
from src.knowledge_extraction import extract_knowledge_from_csv

# 生物学文献文件夹路径
biology_texts_directory = "/home/share/huadjyin/home/liushiqiang/GraphRAG_neo4j_KG/data/biology_texts"
# 输出 CSV 文件路径
output_csv_path = "/home/share/huadjyin/home/liushiqiang/GraphRAG_neo4j_KG/data/output/biology_texts.csv"

# # 处理多个生物学文献文本并存储到 CSV 文件中
# process_and_store_biology_texts(biology_texts_directory, output_csv_path)

# 初始化 LLM 模型
llm = initialize_llm()

# 初始化 LLM-Graph-Transformer
graph_transformer = initialize_graph_transformer(llm)

# 从 CSV 文件中提取知识并生成图谱
extract_knowledge_from_csv(output_csv_path, graph_transformer)

