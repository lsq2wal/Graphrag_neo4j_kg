from langchain_experimental.graph_transformers import LLMGraphTransformer

def initialize_graph_transformer(llm):
    return LLMGraphTransformer(
        llm=llm
        # node_properties=[
        #     "gene_name", "function", "expression_level", "location",  # 基因属性
        #     "protein_name", "structure", "interaction",  # 蛋白质属性
        #     "cell_type", "function", "lineage",  # 细胞类型属性
        #     "disease_name", "classification", "pathology",  # 疾病属性
        #     "variant_id", "gene_position", "variant_type",  # 变异属性
        #     "marker_name", "marker_type",  # 分子标记属性
        #     "drug_name", "target", "mechanism"  # 药物属性
        # ],
        # relationship_properties=[
        #     "interaction_type", "evidence", "confidence",  # 基因-基因关系
        #     "expression_regulation", "functional_relationship",  # 基因-蛋白质关系
        #     "binding_type", "binding_location",  # 蛋白质-蛋白质关系
        #     "association_type", "clinical_significance", "variant_info",  # 基因-疾病关系
        #     "clinical_relevance", "association_strength",  # 变异-疾病关系
        #     "marker_expression", "marker_category",  # 细胞类型-标记关系
        #     "target", "treatment_effect", "mechanism"  # 药物-疾病和基因-药物关系
        # ]
    )
