import cantools
from can.message import Message
db = cantools.db.load_file('/home/Pond/git/pythoncan-examples/resources/motohawk.dbc')
#print the content of the dbc
print(db)

#print a particular message in the dbc
msg = db.get_message_by_name('ExampleMessage')
print(msg)


