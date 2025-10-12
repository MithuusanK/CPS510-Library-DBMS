from flask import Flask, render_template, jsonify
import cx_Oracle

app = Flask(__name__)

# Database configuration
dsn_tns = cx_Oracle.makedsn('oracle.cs.ryerson.ca', 1521, service_name='orcl')

@app.route('/')
def home():
    # Serve the index.html file
    return render_template('menu.html')  # Updated to serve your menu file

@app.route('/query/<option>', methods=['GET'])
def query(option):
    try:
        # Connect to the Oracle database using your credentials
        conn = cx_Oracle.connect(user='', password='', dsn=dsn_tns)
        cursor = conn.cursor()

        # SQL query options based on the menu
        if option == "view_members":
            query = "SELECT name FROM library_member"
        elif option == "view_admins":
            query = "SELECT name FROM library_admin"
        elif option == "view_books":
            query = "SELECT title FROM items WHERE genre = 'Book'"
        else:
            return jsonify({"error": "Invalid option"})

        # Execute the query and fetch results
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]  # Column names
        rows = cursor.fetchall()  # Row data

        return jsonify({"columns": columns, "rows": rows})  # Send results as JSON

    except cx_Oracle.DatabaseError as e:
        return jsonify({"error": str(e)})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)


