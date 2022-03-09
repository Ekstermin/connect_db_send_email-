# import to send email
import smtplib

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# import to connect with database
import pymssql


# import time
import time


def send_mail(htm, address):

    host = "smtp_server"
    port = 587  # For starttls
    sender = "smtp@gmail.com.pl"
    mail_to = address

    password = "password"
    mail_title = "Email title"

    message = MIMEMultipart("alternative")
    message["Subject"] = mail_title
    message["From"] = sender
    message["To"] = mail_to
    print(message["To"])
    # message["Cc"] = mail_to

    html = htm

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")

    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    contex = ssl.create_default_context()

    try:
        server = smtplib.SMTP(host, port, timeout=30)
        # server.set_debuglevel(1)
        # print("debug lvl")
        server.starttls(context=contex)
        server.login(sender, password)
        server.sendmail(
            sender,
            message["To"],
            message.as_string(),
        )
        print("after send")
        server.quit()
    except Exception as e:
        # Print any error messages to stdout
        print(e)


def connect_db_and_return_html():
    try:
        # Connection variables
        server = "localhost"
        database = "database_name"
        username = "user_name"
        password = "user_password"

        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor()

        cursor.execute("EXEC [dbo].[procedure_name]")
        timestr = time.strftime("%Y%m%d-%H-%M-%S")
        print(timestr)
        path = f".arch/info_from_database_" + timestr + ".html"
        print(path)

        # get a next column from result
        row = cursor.fetchone()
        # comit changes from procedure
        conn.commit()
        print("row: ", row)
        print("row type: ", row[0])
        if row[0] == None:
            row_string = "empty result"
            print("none")
            with open(path, "w") as out:
                out.write(row_string)
        else:
            row_string = "".join(row)

            with open(path, "w") as out:
                out.write(row_string)
        conn.close()
        return row_string

    except Exception as e:
        # Print any error messages to stdout
        print("Error: ", e)
        conn.close()


table_from_procedure = connect_db_and_return_html()
address_list = ["mail@gmail.com.pl"]

timestr = time.strftime("%Y%m%d-%H-%M-%S")

log = open("log", "a")
log.write(timestr + "\n")
for adrrr in address_list:
    flag = True

    while flag:
        try:

            send_mail(
                "Message in mail\n" + table_from_procedure,
                adrrr,
            )
            flag = False
            log.write("sent: " + adrrr + "\n")
        except Exception as e:
            print("Error sending to address: " + adrrr)
            log.write("error: " + adrrr + "\n")

log.close()
