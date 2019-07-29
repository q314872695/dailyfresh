# dailyfresh
天天生鲜项目练习  
功能已经全部完成  
数据库：mysql5.7  
python版本：3.7  
项目部署时需要setting.py中的DEBUG=True改成False  
然后运行python manage.py collectionstatic 命令手机静态文件  
media为用户上传的文件夹  
static为网页静态文件的文件夹  
运行时pymysql报错django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.   
解决方法：  
    1、raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__) 　　　django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3. 　　解决办法：C:\Python37\Lib\site-packages\django\db\backends\mysql（python安装目录）打开base.py，注释掉以下内容： 　　　　　　　if version < (1, 3, 13): 　　　　　　　　　　raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)  
    2、File "C:\Python37\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query 　　 query = query.decode(errors='replace') 　　AttributeError: 'str' object has no attribute 'decode' 　　解决办法：打开此文件把146行的decode修改为encode
全文检索jieba配置：  
    1、建立ChineseAnalyzer.py文件，保存在haystack的安装文件夹下，路径如“/home/python/.virtualenvs/django_py2/lib/python2.7/site-packages/haystack/backends”  
    内容如下：
    
    import jieba  
    from whoosh.analysis import Tokenizer, Token
    
    class ChineseTokenizer(Tokenizer):
        def __call__(self, value, positions=False, chars=False,
                     keeporiginal=False, removestops=True,
                     start_pos=0, start_char=0, mode='', **kwargs):
            t = Token(positions, chars, removestops=removestops, mode=mode,
                      **kwargs)
            seglist = jieba.cut(value, cut_all=True)
            for w in seglist:
                t.original = t.text = w
                t.boost = 1.0
                if positions:
                    t.pos = start_pos + value.find(w)
                if chars:
                    t.startchar = start_char + value.find(w)
                    t.endchar = start_char + value.find(w) + len(w)
                yield t
    
    
    def ChineseAnalyzer():
        return ChineseTokenizer()
        
    2、复制whoosh_backend.py文件，改名为whoosh_cn_backend.py
    注意：复制出来的文件名，末尾会有一个空格，记得要删除这个空格
    from .ChineseAnalyzer import ChineseAnalyzer 
    查找
    analyzer=StemmingAnalyzer()
    改为
    analyzer=ChineseAnalyzer()