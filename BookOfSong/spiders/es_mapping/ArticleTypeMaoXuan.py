from elasticsearch_dsl import Document, Text, analyzer
from elasticsearch_dsl.connections import connections

# Gitlab：https://github.com/elastic/elasticsearch-dsl-py
# 示例：https://blog.csdn.net/qq_21531681/article/details/108704172

# 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=['had-nn:9200'])


# 配置ES的mappings映射
class ArticleTypeMaoXuan(Document):
    # Text类型需要分词，所以需要知道中文分词器，ik_max_wordwei为中文分词器
    # ES数据库中表的各个字段声明
    # 辑
    album = Text(analyzer="ik_max_word")
    title = Text(analyzer="ik_max_word")
    author = Text()
    # 内容
    content = Text(analyzer="ik_max_word")

    # 创建索引（数据库）
    class Index:
        # 对应es的index(相当于数据库名称)
        name = "book_mao_xuan"


# 判断在本代码文件执行才执行里面的方法，其他页面调用的则不执行里面的方法
if __name__ == "__main__":
    # 通过init()方法生成index下面的type以及它的mappings
    ArticleTypeMaoXuan.init()
