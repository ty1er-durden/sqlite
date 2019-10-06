import argparse
import json
import sqlite3

# Because lists  of IPs are to be stored in the data base we will use
# JSON serialization/deserialization to represent them
sqlite3.register_adapter(list, json.dumps)
sqlite3.register_converter("json", json.loads)

# Table definitions

# Table containing basic LB infomation
SQL_LB_TABLE = """
CREATE TABLE IF NOT EXISTS lb (
    id integer PRIMARY KEY NOT NULL,
    mgmt_ip text NOT NULL,
    hostname text NOT NULL,
    vendor text NOT NULL,
    version text NOT NULL
);"""

# Table containing detailed information is stored separately
# for our F5 load balancers, to say A10 because different columns
# may be required
SQL_F5_DETAIL_TABLE = """
CREATE TABLE IF NOT EXISTS f5_detail (
    id integer PRIMARY KEY,
    lb_id integer NOT NULL,
    frontend_ip json,
    backend_ip json,
    FOREIGN KEY (lb_id) REFERENCES lb (mgmt_ip)
);"""


def connect(path):
    """ Connect to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        return conn
    except sqlite3.Error as e:
        print(f"SQLite failure: {e}")
    except Exception as e:
        print(f"General failure: {e}")


def create_table(conn, create_table_sql):
    """Creates a table """
    cur = conn.cursor()
    cur.execute(create_table_sql)


def insert(conn, table_name, **kwargs):
    """inserts row in to a table"""
    columns = []
    values = []
    qmarks = []
    for k, v in kwargs.items():
        columns.append(k)
        values.append(v)
        qmarks.append("?")
    columns, values
    sql = f"""INSERT INTO {table_name}({",".join(columns)})
    VALUES({",".join(qmarks)})
    """
    cur = conn.cursor()
    cur.execute(sql, tuple(values))
    return cur.lastrowid


def select_all(conn, query):
    """Executes select and retruns all rows"""
    cur = conn.cursor()
    cur.execute(query)
    column_names = [description[0] for description in cur.description]
    return (column_names, cur.fetchall())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    args = parser.parse_args()

    conn = sqlite3.connect(args.path)

    with conn:
        # create projects table
        create_table(conn, SQL_LB_TABLE)

        # create tasks table
        create_table(conn, SQL_F5_DETAIL_TABLE)

        # Add record 1
        lb = {
            "vendor": "F5",
            "mgmt_ip": "10.55.137.24",
            "hostname": "bigip-01.customer1.local",
            "version": "10",
        }
        lb_id = insert(conn, "lb", **lb)
        # create detail record
        f5_detail = {
            "lb_id": lb_id,
            "frontend_ip": ["205.134.12.57"],
            "backend_ip": [
                "10.55.136.100",
                "10.55.136.101",
                "10.55.136.102",
                "10.55.136.103",
            ],
        }
        lb_id = insert(conn, "f5_detail", **f5_detail)

        # Add record 2
        lb = {
            "vendor": "F5",
            "mgmt_ip": "10.83.121.250",
            "hostname": "my-load-balancer.customer2.internal",
            "version": "11",
        }
        lb_id = insert(conn, "lb", **lb)
        # create detail record
        f5_detail = {
            "lb_id": lb_id,
            "frontend_ip": ["69.254.121.36"],
            "backend_ip": ["10.83.121.10", "10.83.121.11"],
        }
        lb_id = insert(conn, "f5_detail", **f5_detail)

        # Add record 3
        lb = {
            "vendor": "F5",
            "mgmt_ip": "10.55.12.30",
            "hostname": "big-ip.customer3.com",
            "version": "10",
        }
        lb_id = insert(conn, "lb", **lb)
        # create detail record
        f5_detail = {
            "lb_id": lb_id,
            "frontend_ip": ["220.242.72.34"],
            "backend_ip": [
                "10.55.13.44",
                "10.55.13.45",
                "10.55.13.46",
                "10.55.13.47",
            ],
        }
        lb_id = insert(conn, "f5_detail", **f5_detail)

        # Select data with relationships resolved
        sql = """
        SELECT
            lb.hostname as HOSTANME,
            lb.vendor as VENDOR,
            lb.mgmt_ip as 'IP ADDRESS',
            f5_detail.frontend_ip as 'FRONTEND POOL',
            f5_detail.backend_ip as 'BACKEND POOL'
        FROM lb LEFT JOIN f5_detail
        WHERE lb.id = f5_detail.lb_id
        """
        column_names, rows = select_all(conn, sql)

        # Print out contents
        print("")
        print(f"Query returned {len(rows)} row(s):")
        print("")
        for row in rows:
            i = 0
            for column in row:
                print(column_names[i], column, sep=": ")
                i += 1
            print("")
