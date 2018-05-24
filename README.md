# scrapy
这是一个基于scrapy的爬虫

### 爬取对象：
爬取对象为豆瓣读书,爬取了主标题,副标题,类型，详情链接等信息

### 内容存储:
简单的将内容存入了数据库中

### 环境:
安装过scrapy环境

### 运行:
按照sql文件创建对应的库表后,更改settings.py文件后,执行 #scrapy crawl douban 就可以运行了

### 目录结构: 
├── doubanread </br>
│   ├── __init__.py </br>
│   ├── items.py </br>
│   ├── middlewares.py </br>
│   ├── pipelines.py </br>
│   ├── settings.py </br>
│   └── spiders </br>
│       ├── douban_spider.py </br>
│       ├── __init__.py </br>
├── doubanread.sql </br>
├── README.md </br>
└── scrapy.cfg </br>
其中,douban_spider.py是爬虫可爬取的内容提取.item.py规定了数据格式,pipelines.py完成了对数据的编码和存储(写入数据库或写入文件)，settings.py是这个爬虫的一些配置(我将一部分配置写入了douban_spider.py文件中,可以根据需求更改)
