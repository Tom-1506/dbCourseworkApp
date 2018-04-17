from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

connection = psycopg2.connect('dbname=postgres user=postgres password=journey')
cursor = connection.cursor()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/task1', methods=["POST"])
def task1():
    customerID = request.form["CustomerID"]
    customerName = request.form["CustomerName"]
    customerEmail = request.form["CustomerEmail"]

    cursor.execute(
        "INSERT INTO Customer (CustomerID,Name,Email) VALUES (%s, %s, %s)",
        [customerID, customerName, customerEmail])

    connection.commit()

    return render_template('index.html', task1SuccessString="Query was Successful!")

@app.route('/task2', methods=['POST'])
def task2():
    ticketID = request.form["TicketID"]
    problem = request.form["Problem"]
    customerID = request.form["CustomerID"]
    productID = request.form["ProductID"]

    cursor.execute(
        "INSERT INTO Ticket (TicketID,Problem,Status,Priority,LoggedTime,CustomerID,ProductID)"
        "VALUES(%s,%s,'open','1',current_timestamp,%s,%s) RETURNING *",
        [ticketID, problem, customerID, productID])

    task2return = cursor.fetchall()
    connection.commit()

    return render_template('task2.html', task2SuccessString="Query was Successful!", task2return=task2return)

@app.route('/task3', methods=['POST'])
def task3():
    ticketUpdateID = request.form["TicketUpdateID"]
    message = request.form["Message"]
    ticketID = request.form["TicketID"]
    staffID = request.form["StaffID"]

    cursor.execute(
        "INSERT INTO TicketUpdate (TicketUpdateID,Message,UpdateTime,TicketID,StaffID)"
        "VALUES(%s,%s,current_timestamp,%s,%s)",
        [ticketUpdateID, message, ticketID, staffID])

    connection.commit()

    return render_template('index.html', tsak3SuccessString="Query was Successful!")

@app.route('/task4', methods=["POST"])
def task4():
    cursor.execute("""SELECT 
        Ticket.TicketID,
        Status,
        UpdateTime
      FROM Ticket FULL OUTER JOIN TicketUpdate ON Ticket.TicketID = TicketUpdate.TicketID
        WHERE Status = 'open'
      GROUP BY Ticket.ticketid, ticketupdate.updatetime
      ORDER BY TicketID ASC;""")

    task4return = cursor.fetchall()
    connection.commit()

    return render_template('task4.html', task4SuccessString="Query was Successful!", task4return=task4return)

@app.route('/task5', methods=["POST"])
def task5():
    ticketID = request.form["TicketID"]

    cursor.execute("UPDATE Ticket SET Status = 'closed' WHERE TicketID = %s AND Status = 'open'", [ticketID])

    connection.commit()

    return render_template('index.html', task5SuccessString="Query was Successful!")

@app.route('/task6', methods=["POST"])
def task6():
    ticketID = request.form["TicketID"]

    cursor.execute("""SELECT 
      Ticket.TicketID,
      Problem,
      TicketUpdateID,
      Message,
      UpdateTime,
      Name 
    FROM Ticket FULL OUTER JOIN TicketUpdate
        ON Ticket.TicketID = TicketUpdate.TicketID FULL OUTER JOIN Staff 
        ON TicketUpdate.StaffID = Staff.StaffID 
          WHERE Ticket.TicketID = '1'
    ORDER BY UpdateTime ASC;""", [ticketID])

    task6return = cursor.fetchall()
    connection.commit()

    return render_template('task6.html', task6SuccessString="Query was Successful!", task6return=task6return)

@app.route('/task7', methods=["POST"])
def task7():
    cursor.execute("""SELECT 
        Ticket.TicketID,
        Status,
        COUNT(TicketUpdate.TicketID) AS "NumberOfUpdates",
        MIN(TicketUpdate.UpdateTime) - Ticket.LoggedTime AS "TimeTillFirstUpdate",
        MAX(TicketUpdate.UpdateTime) - Ticket.LoggedTime AS "TimeTillLastUpdate" 
    FROM Ticket INNER JOIN TicketUpdate ON Ticket.TicketID = TicketUpdate.TicketID
        WHERE Status = 'closed' 
        GROUP BY Ticket.TicketID 
        ORDER BY Ticket.TicketID;""")

    task7return = cursor.fetchall()
    connection.commit()

    return render_template('task7.html', task7SuccessString="Query was Successful!", task7return=task7return)

@app.route('/task8', methods=["POST"])
def task8():
    customerID = request.form["CustomerID"]

    cursor.execute("DELETE FROM Customer WHERE CustomerID = %s", [customerID])

    connection.commit()

    return render_template('index.html', task8SuccessString="Query was Successful!")


if __name__ == '__main__':
    app.run()
