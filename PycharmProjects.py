from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

#open pcycopg2 connection and cursor
connection = psycopg2.connect('dbname=postgres user=postgres password=journey')
cursor = connection.cursor()

#app route for home page named index.html
@app.route('/')
def home():
    #list of tickets for task6 drop down menu
    cursor.execute("SELECT TicketID FROM Ticket ORDER BY TicketID ASC")

    listOfTickets = cursor.fetchall() #put results of query into variable

    #list of tickets for task5 drop down menu
    cursor.execute("SELECT TicketID FROM Ticket WHERE Status = 'open' ORDER BY TicketID ASC")

    listOfOpenTickets = cursor.fetchall() #put results of query into variable

    #render index.html and pass the data for the dropdown menus to html
    return render_template('index.html', listOfTickets=listOfTickets, listOfOpenTickets=listOfOpenTickets)

#app route for task 1
@app.route('/task1', methods=["POST"])
def task1():
    try: #try and except for error catching
        #get values from html form
        customerID = request.form["CustomerID"]
        customerName = request.form["CustomerName"]
        customerEmail = request.form["CustomerEmail"]

        #inserts new customer into customer table
        cursor.execute(
            "INSERT INTO Customer (CustomerID,Name,Email) VALUES (%s, %s, %s)",
            [customerID, customerName, customerEmail])

        connection.commit() #commit the changes
    except psycopg2.Error as e: #catch error
        connection.rollback()

        #render index.html
        return render_template('index.html', task1FailureString=e) #give a failure string to the html

    #render index.html and pass the success string to html
    return render_template('index.html', task1SuccessString="Query was Successful!")

#app route for task 2
@app.route('/task2', methods=['POST'])
def task2():
    try: #try and except for error catching
        #get values from html form
        ticketID = request.form["TicketID"]
        problem = request.form["Problem"]
        customerID = request.form["CustomerID"]
        productID = request.form["ProductID"]

        #create a new ticket and show the details
        cursor.execute(
            "INSERT INTO Ticket (TicketID,Problem,Status,Priority,LoggedTime,CustomerID,ProductID)"
            "VALUES(%s,%s,'open','1',current_timestamp,%s,%s) RETURNING *",
            [ticketID, problem, customerID, productID])

        task2return = cursor.fetchall() #put query result in variable
        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task2FailureString=e) #give a failure string to the html

    # render task2.html and pass the success string to html, also pass data for output
    return render_template('task2.html', task2SuccessString="Query was Successful!", task2return=task2return)

#app route for task 3
@app.route('/task3', methods=['POST'])
def task3():
    try: #try and except for error catching
        #get values from html form
        ticketUpdateID = request.form["TicketUpdateID"]
        message = request.form["Message"]
        ticketID = request.form["TicketID"]
        staffID = request.form["StaffID"]

        #create new ticket update
        cursor.execute(
            "INSERT INTO TicketUpdate (TicketUpdateID,Message,UpdateTime,TicketID,StaffID)"
            "VALUES(%s,%s,current_timestamp,%s,%s)",
            [ticketUpdateID, message, ticketID, staffID])

        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task3FailureString=e) #give a failure string to the html

    # render index.html and pass the success string to html
    return render_template('index.html', tsak3SuccessString="Query was Successful!")

#app route for task 4
@app.route('/task4', methods=["POST"])
def task4():
    try: #try and except for error catching

        #select all outstanding tickets and their last update
        cursor.execute("""SELECT 
            Ticket.TicketID,
            Status,
            UpdateTime
          FROM Ticket FULL OUTER JOIN TicketUpdate ON Ticket.TicketID = TicketUpdate.TicketID
            WHERE Status = 'open'
          GROUP BY Ticket.ticketid, ticketupdate.updatetime
          ORDER BY TicketID ASC;""")

        task4return = cursor.fetchall() #put results in variable
        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task4FailureString=e) #give a failure string to the html

    # render task4.html and pass the success string to html, also pass data for output
    return render_template('task4.html', task4SuccessString="Query was Successful!", task4return=task4return)

#app route for task 5
@app.route('/task5', methods=["POST"])
def task5():
    try: #try and except for error catching
        #get value from html form
        ticketID = request.form["TicketID"]

        #set the status of a ticket to closed
        cursor.execute("UPDATE Ticket SET Status = 'closed' WHERE TicketID = %s", [ticketID])

        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task5FailureString=e) #give a failure string to the html

    # render index.html and pass the success string to html
    return render_template('index.html', task5SuccessString="Query was Successful!")

#app route for task 6
@app.route('/task6', methods=["POST"])
def task6():
    try: #try and except for error catching
        #get value from html form
        ticketID = request.form["TicketID"]

        #display the updates to a ticket in chronological order
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
              WHERE Ticket.TicketID = %s
        ORDER BY UpdateTime ASC;""", [ticketID])

        task6return = cursor.fetchall() #put results in variable
        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task6FailureString=e) #give a failure string to the html

    # render task6.html and pass the success string to html, also pass data for output
    return render_template('task6.html', task6SuccessString="Query was Successful!", task6return=task6return)

#app route for task 7
@app.route('/task7', methods=["POST"])
def task7():
    try: #try and except for error catching

        #select all closed tickets, the number of updates they have and times between updates
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

        task7return = cursor.fetchall() #put results in variable
        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task7FailureString=e) #give a failure string to the html

    # render task7.html and pass the success string to html, also pass data for output
    return render_template('task7.html', task7SuccessString="Query was Successful!", task7return=task7return)

#app route for task 8
@app.route('/task8', methods=["POST"])
def task8():
    try: #try and except for error catching
        #get value from html form
        customerID = request.form["CustomerID"]

        #delete a customer
        cursor.execute("DELETE FROM Customer WHERE CustomerID = %s", [customerID])

        connection.commit() #commit the changes

    except psycopg2.Error as e: #catch error
        connection.rollback()

        # render index.html
        return render_template('index.html', task8FailureString=e) #give a failure string to the html

    # render index.html and pass the success string to html
    return render_template('index.html', task8SuccessString="Query was Successful!")


if __name__ == '__main__':
    app.run()
