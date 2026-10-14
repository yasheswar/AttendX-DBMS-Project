import os
import sqlite3
import datetime
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    _engine = None  # 'MYSQL' or 'SQLITE'
    _mysql_pool = None
    _sqlite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'attendx_cloud.db')

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            # Try connecting to MySQL first
            cls._init_engine()
        return cls._engine

    @classmethod
    def _init_engine(cls):
        host = os.getenv("DB_HOST", "localhost")
        port = int(os.getenv("DB_PORT", 3306))
        db = os.getenv("DB_NAME", "attendx_db")
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")

        # Check if Streamlit secrets exist (when hosted on Streamlit Cloud)
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "DB_HOST" in st.secrets:
                host = st.secrets["DB_HOST"]
                port = int(st.secrets.get("DB_PORT", 3306))
                db = st.secrets.get("DB_NAME", "attendx_db")
                user = st.secrets.get("DB_USER", "root")
                password = st.secrets.get("DB_PASSWORD", "")
        except Exception:
            pass

        try:
            import mysql.connector
            from mysql.connector import pooling
            
            # Quick connectivity test
            test_conn = mysql.connector.connect(
                host=host, port=port, database=db, user=user, password=password,
                connection_timeout=2
            )
            test_conn.close()

            # Create pool
            cls._mysql_pool = pooling.MySQLConnectionPool(
                pool_name="attendx_pool",
                pool_size=5,
                pool_reset_session=True,
                host=host,
                port=port,
                database=db,
                user=user,
                password=password
            )
            cls._engine = 'MYSQL'
            print(f"Connected to MySQL 8.0 on {host}:{port}")
        except Exception as e:
            print(f"MySQL not accessible ({e}). Switching to Cloud Engine (SQLite fail-safe).")
            cls._engine = 'SQLITE'
            if not os.path.exists(cls._sqlite_path):
                from sync_cloud_db import export_mysql_to_sqlite
                try:
                    export_mysql_to_sqlite()
                except Exception as ex:
                    print(f"Could not auto-generate cloud db: {ex}")

    @classmethod
    def get_sqlite_conn(cls):
        conn = sqlite3.connect(cls._sqlite_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Register MySQL compatibility functions
        conn.create_function("CONCAT", -1, lambda *args: "".join(str(a) if a is not None else "" for a in args))
        conn.create_function("IFNULL", 2, lambda a, b: b if a is None else a)
        def _datediff(d1, d2):
            try:
                s1 = str(d1)[:10]
                s2 = str(d2)[:10]
                return (datetime.date.fromisoformat(s1) - datetime.date.fromisoformat(s2)).days
            except Exception:
                return 0
        conn.create_function("DATEDIFF", 2, _datediff)
        return conn

def get_database_engine_name():
    engine = DatabaseManager.get_engine()
    if engine == 'MYSQL':
        host = os.getenv("DB_HOST", "localhost")
        return f"MySQL 8.0 ({host})"
    return "Cloud Database Engine (Online Demo)"

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """Executes query across active engine (MySQL or SQLite cloud fail-safe) transparently."""
    engine = DatabaseManager.get_engine()
    params = params or ()

    if engine == 'MYSQL':
        import mysql.connector
        conn = None
        cursor = None
        try:
            conn = DatabaseManager._mysql_pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            
            result = None
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
                
            if commit:
                conn.commit()
            return result
        except mysql.connector.Error as e:
            if conn and commit:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    else:
        # SQLite Engine
        # Intercept stored procedure calls if running in cloud fallback
        if query.strip().upper().startswith("CALL SP_GET_STUDENT_SUMMARY"):
            stu_id = params[0] if params else 1
            query = """
                SELECT 
                    s.student_id,
                    s.registration_number,
                    (s.first_name || ' ' || s.last_name) AS full_name,
                    s.department,
                    s.semester,
                    COUNT(DISTINCT co.offering_id) AS enrolled_courses,
                    ROUND(IFNULL(AVG(v.attendance_percentage), 0), 2) AS cumulative_attendance,
                    (SELECT COUNT(*) FROM leave_applications WHERE student_id = ? AND application_status = 'APPROVED') AS approved_leaves,
                    (SELECT COUNT(*) FROM alerts WHERE student_id = ? AND is_resolved = 0) AS active_alerts
                FROM students s
                JOIN student_section ss ON s.student_id = ss.student_id
                JOIN course_offerings co ON ss.section_id = co.section_id
                LEFT JOIN vw_student_attendance_percentage v ON s.student_id = v.student_id AND co.offering_id = v.offering_id
                WHERE s.student_id = ?
                GROUP BY s.student_id;
            """
            params = (stu_id, stu_id, stu_id)

        # Convert %s placeholder to ? for sqlite
        sqlite_query = query.replace("%s", "?")
        conn = DatabaseManager.get_sqlite_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(sqlite_query, params)
            
            result = None
            if fetch_one:
                row = cursor.fetchone()
                result = dict(row) if row is not None else None
            elif fetch_all:
                rows = cursor.fetchall()
                result = [dict(r) for r in rows]
                
            if commit:
                conn.commit()
            return result
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            conn.close()

def execute_transaction(queries_with_params):
    """Executes a list of (query, params) queries in an atomic transaction."""
    engine = DatabaseManager.get_engine()
    
    if engine == 'MYSQL':
        import mysql.connector
        conn = None
        cursor = None
        try:
            conn = DatabaseManager._mysql_pool.get_connection()
            conn.start_transaction()
            cursor = conn.cursor()
            for query, params in queries_with_params:
                cursor.execute(query, params or ())
            conn.commit()
            return True
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    else:
        conn = DatabaseManager.get_sqlite_conn()
        try:
            cursor = conn.cursor()
            for query, params in queries_with_params:
                sqlite_query = query.replace("%s", "?")
                cursor.execute(sqlite_query, params or ())
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
