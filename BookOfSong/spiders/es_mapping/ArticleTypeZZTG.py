from elasticsearch_dsl import Document, Text
from elasticsearch_dsl.connections import connections

# 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=['had-nn:9200'])

'''
《资治通鉴》
配置ElasticSearch的mapping
'''


class ArticleTypeZZTG(Document):
    # Text类型需要分词，所以需要知道中文分词器，ik_max_wordwei为中文分词器
    # ES数据库中表的各个字段声明
    # 辑
    album_name = Text(analyzer="ik_max_word")
    # 篇目名称
    title = Text(analyzer="ik_max_word")
    # 作者
    author = Text()
    # 字数
    char_num = Text()
    # 内容
    content = Text(analyzer="ik_max_word")

    # 创建索引（数据库）
    class Index:
        # 对应es的index(相当于数据库名称)
        name = "book_zi_zhi_tong_jian"


# 判断在本代码文件执行才执行里面的方法，其他页面调用的则不执行里面的方法
if __name__ == "__main__":
    # 通过init()方法生成index下面的type以及它的mappings
    ArticleTypeZZTG.init()
