import os
import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import webbrowser

def check_dependencies():
    """Check and install required dependencies."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "twilio"])
        messagebox.showinfo("Info", "All dependencies are installed.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Dependencies could not be installed.")

def configure_credentials():
    """Configure Twilio credentials."""
    os.environ['TWILIO_ACCOUNT_SID'] = entry_sid.get()
    os.environ['TWILIO_AUTH_TOKEN'] = entry_token.get()
    messagebox.showinfo("Info", "Twilio credentials configured.")

def send_message():
    """Send SMS message."""
    clear_status()  # Clear status area before sending a new message
    
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    if not account_sid or not auth_token:
        messagebox.showerror("Error", "Twilio credentials missing.")
        return

    client = Client(account_sid, auth_token)
    body = text_body.get("1.0", END)
    numbers = text_to.get("1.0", END).split(',')

    for to_number in numbers:
        try:
            message = client.messages.create(
                body=body.strip(),
                from_='+12187876050',
                to=to_number.strip()
            )
            update_status(f'Message sent to {to_number.strip()}: {message.sid}')
        except TwilioRestException as e:
            update_status(f'Error sending to {to_number.strip()}: {e}')

def clear_status():
    """Clear status messages."""
    status_var.set('')

def update_status(message):
    """Update status messages."""
    status_var.set(status_var.get() + message + '\n')

def count_numbers():
    """Count the numbers entered."""
    numbers = text_to.get("1.0", END).split(',')
    counter_numbers.set(f"Numbers Added: {len(numbers)}")

def close_application():
    """Close the application."""
    root.destroy()

def open_twitter():
    """Open Twitter profile."""
    webbrowser.open("https://twitter.com/SrMayoZ")

# Window configuration
root = Tk()
root.title("Twilio SMS Sender")

status_var = StringVar()
counter_numbers = StringVar()

# Button to check and install dependencies
button_deps = Button(root, text="Check/Install Dependencies", command=check_dependencies)
button_deps.pack()

# Entry for Account SID
label_sid = Label(root, text="Twilio Account SID:")
label_sid.pack()

entry_sid = Entry(root, width=50)
entry_sid.pack()

# Entry for Auth Token
label_token = Label(root, text="Twilio Auth Token:")
label_token.pack()

entry_token = Entry(root, width=50)
entry_token.pack()

# Button to configure credentials
button_cred = Button(root, text="Configure Credentials", command=configure_credentials)
button_cred.pack()

# Large text field for the message
label_body = Label(root, text="Message:")
label_body.pack()

text_body = Text(root, height=10, width=50)
text_body.pack()

# Large text field for the numbers
label_to = Label(root, text="Destination Numbers (separated by commas):")
label_to.pack()

text_to = Text(root, height=5, width=50)
text_to.pack()

# Button to count numbers
button_count = Button(root, text="Count Numbers", command=count_numbers)
button_count.pack()

# Label to show the number count
label_count = Label(root, textvariable=counter_numbers)
label_count.pack()

# Button to send message
button_send = Button(root, text="Send Message", command=send_message)
button_send.pack()

# Button to close the application
button_close = Button(root, text="Close Application", command=close_application)
button_close.pack()

# Label to show status
label_status = Label(root, textvariable=status_var)
label_status.pack()

# Link to Twitter
label_twitter = Label(root, text="@SrMayoZ", fg="blue", cursor="hand2")
label_twitter.pack()
label_twitter.bind("<Button-1>", lambda e: open_twitter())

# Run the application
root.mainloop()
