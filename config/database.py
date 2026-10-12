import mysql.connector
from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="attendx_pool",
                    pool_size=5,
                    pool_reset_session=True,
                    host=os.getenv("DB_HOST", "localhost"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    database=os.getenv("DB_NAME", "attendx_db"),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", "")
                )
            except Error as e:
                print(f"Error creating connection pool: {e}")
                raise e
        return cls._pool

    @classmethod
    def get_connection(cls):
        try:
            pool = cls.get_pool()
            return pool.get_connection()
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            raise e

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """Utility to execute SQL queries safely using parameterized queries."""
    conn = None
    cursor = None
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
            
        if commit:
            conn.commit()
            
        return result
    except Error as e:
        if conn and commit:
            conn.rollback()
        print(f"Database error executing query: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def execute_transaction(queries_with_params):
    """
    Execute multiple queries in a single transaction.
    queries_with_params: List of tuples (query_string, params_tuple)
    """
    conn = None
    cursor = None
    try:
        conn = DatabaseConnection.get_connection()
        # Start transaction explicitly
        conn.start_transaction()
        cursor = conn.cursor()
        
        for query, params in queries_with_params:
            cursor.execute(query, params or ())
            
        conn.commit()
        return True
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Transaction failed: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
