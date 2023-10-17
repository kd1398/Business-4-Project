# importing required libraries
import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="NumbSkull@55"
)

# preparing a cursor object
cursorObject = dataBase.cursor()

# creating database
cursorObject.execute("CREATE DATABASE fetherstill_db")