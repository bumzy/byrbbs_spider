This project is used to crawl bbs.byr.cn data.Details see [this post][1].

此项目用于爬取北邮人论坛相关数据。详细说明见[此帖][1]

only 3 steps needed:

只需以下三步：

1.create mysql db and tables

创建mysql数据库与表格

```mysql
CREATE TABLE section (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  section_url varchar(60) NOT NULL,
  section_name varchar(50) NOT NULL,
  section_article_total int(7) NOT NULL,
  top_section_name varchar(50) NOT NULL,
  top_section_num int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create TABLE articleinfo (                       
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,   
  section_name varchar(50) NOT NULL,
  article_title varchar(80) NOT NULL,   
  article_url varchar(80) NOT NULL,
  article_createtime date NOT NULL,
  article_comment int(10) unsigned NOT NULL DEFAULT '0',
  article_author varchar(50),                                            
  PRIMARY KEY (id)                                                           
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE articlebody (                       
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,   
  article_url varchar(80) NOT NULL,
  article_content text, 
  PRIMARY KEY (id)                                                           
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

```



2.crawl bbs section information(stored in table section)

爬取板块信息（存储于section表格）

```shell
scrapy crawl byr_section
```

3.crawl bbs content(stored in table articleinfo，articlebody)

爬取帖子信息（存储于articleinfo，articlebody表格）

```shell
scrapy crawl byr_article
```

[1]: https://ryderchan.github.io/2017/01/31/scrapy%E7%88%AC%E5%8F%96%E5%8C%97%E9%82%AE%E4%BA%BA%E8%AE%BA%E5%9D%9B%E6%89%80%E6%9C%89%E5%B8%96%E7%9A%84%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%E5%8F%8A%E6%AD%A3%E6%96%87/
