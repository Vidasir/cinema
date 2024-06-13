from database.database_create import sql, db
from user_test.test_database import Create
from database.database_view import Search


test_db = Create()
test_db.test(sql, db, 10000)


test_search = Search()

#test_search.views(sql)
#test_search.params(sql)


