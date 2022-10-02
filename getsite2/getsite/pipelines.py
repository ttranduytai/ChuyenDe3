import mysql.connector

class MysqlDemoPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'nhandan'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS nhandan2(
            id int NOT NULL auto_increment, 
            title VARCHAR(1000),
            date VARCHAR(1000),
            content VARCHAR(1000000),
            category VARCHAR(1000),
            url VARCHAR(1000),
            image_urls VARCHAR(1000),
            PRIMARY KEY (id)
        )
        """)



    # def process_item(self, item, spider):
    #     ## Define insert statement
    #     self.cur.execute(""" insert into wp_nhandanposts (post_author,post_title, post_date, post_content, post_name) values (%s,%s,%s,%s,%s)""", (
    #         1,
    #         str(item["title"]),
    #         str(item["date"]),
    #         str(item["content"]),
    #         str(item["title"]),
    #         ))

    #     self.cur.execute(""" insert into wp_nhandanterms (name) values (%s)""", (
    #         str(item["category"]),
    #         ))

    #     ## Execute insert of data into database
    #     self.conn.commit()

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" insert into nhandan2 (title,date,content,category,url,image_urls) values (%s,%s,%s,%s,%s,%s)""", (
            str(item["title"]),
            str(item["date"]),
            str(item["content"]),
            str(item["category"]),
            str(item["url"]),
            str(item["image_urls"]),
            ))

        ## Execute insert of data into database
        self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()