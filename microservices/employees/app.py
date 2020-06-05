from flask import Flask
import pymysql.cursors
from flask import jsonify
import json
import collections
import errno
from socket import error as socket_error

app=Flask(__name__)

@app.route("/employees", methods=["GET"])
def test():
    try:
        connection = pymysql.connect(host='mysql-container',
                                     port=3306,
                                     user='root',
                                     password='secret',
                                     db='employees',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    except pymysql.err.OperationalError as e:
        return json.dumps({'*** WAIT!! ***': 'PLEASE WAIT UNTIL THE DB FINISHES POPULATING...'})

    try:
        with connection.cursor() as cursor:
            sql = "select * from employees where gender = 'M' and birth_date = '1965-02-01' and hire_date > '1990-01-01' order by first_name ASC, last_name ASC;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            objects_list = []
            for row in rows:
                print(row)
                d = collections.OrderedDict()
                d['emp_no'] = str(row['emp_no'])
                d['FirstName'] = str(row['first_name'])
                d['LastName'] = str(row['last_name'])
                d['HireDate'] = str(row['hire_date'].strftime('%Y-%m-%d'))
                d['Gender'] = str(row['gender'])
                d['BirthDate'] = str(row['birth_date'].strftime('%Y-%m-%d'))
                objects_list.append(d)
                j = json.dumps(objects_list)
            return j
    except Exception as e:
        return json.dumps({'Unexpected error': str(e)})
    finally:
        connection.close()

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
