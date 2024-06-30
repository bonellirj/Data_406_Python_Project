import db.conn_factory as db
import data_process.data_exploration.user_exploration as ue

try:
    db_conn = db.getConnection()
except Exception as e:
    print("Ocorreu um erro ao conectar ao SQL Server:", e)
    x
finally:
    
    try:
        ue.anlise_1(db_conn)
        
    except Exception as e:
        print("Error on Analysis 1: ", e)
        
    finally:
        db_conn.close()



