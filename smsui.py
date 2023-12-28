import os
import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def verificar_dependencias():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "twilio"])
        messagebox.showinfo("Info", "Todas las dependencias están instaladas.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "No se pudieron instalar las dependencias.")

def configurar_credenciales():
    os.environ['TWILIO_ACCOUNT_SID'] = entry_sid.get()
    os.environ['TWILIO_AUTH_TOKEN'] = entry_token.get()
    messagebox.showinfo("Info", "Credenciales de Twilio configuradas.")

def enviar_mensaje():
    clear_status()  # Limpiar el área de estado antes de enviar un nuevo mensaje
    
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    if not account_sid or not auth_token:
        messagebox.showerror("Error", "Falta configurar credenciales de Twilio.")
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
            update_status(f'Mensaje enviado a {to_number.strip()}: {message.sid}')
        except TwilioRestException as e:
            update_status(f'Error al enviar a {to_number.strip()}: {e}')
            
def clear_status():
    status_var.set('')

def update_status(message):
    status_var.set(status_var.get() + message + '\n')

def contar_numeros():
    numeros = text_to.get("1.0", END).split(',')
    contador_numeros.set(f"Números Añadidos: {len(numeros)}")

def cerrar_aplicacion():
    root.destroy()

# Configuración de la ventana
root = Tk()
root.title("Enviar SMS con Twilio")

status_var = StringVar()
contador_numeros = StringVar()

# Botón para verificar e instalar dependencias
button_deps = Button(root, text="Verificar/Instalar Dependencias", command=verificar_dependencias)
button_deps.pack()

# Entrada para Account SID
label_sid = Label(root, text="Twilio Account SID:")
label_sid.pack()

entry_sid = Entry(root, width=50)
entry_sid.pack()

# Entrada para Auth Token
label_token = Label(root, text="Twilio Auth Token:")
label_token.pack()

entry_token = Entry(root, width=50)
entry_token.pack()

# Botón para configurar credenciales
button_cred = Button(root, text="Configurar Credenciales", command=configurar_credenciales)
button_cred.pack()

# Campo de texto grande para el mensaje
label_body = Label(root, text="Mensaje:")
label_body.pack()

text_body = Text(root, height=10, width=50)
text_body.pack()

# Campo de texto grande para los números
label_to = Label(root, text="Números de destino (separados por comas):")
label_to.pack()

text_to = Text(root, height=5, width=50)
text_to.pack()

# Botón para contar números
button_count = Button(root, text="Contar Números", command=contar_numeros)
button_count.pack()

# Etiqueta para mostrar la cantidad de números
label_count = Label(root, textvariable=contador_numeros)
label_count.pack()

# Botón para enviar mensaje
button_send = Button(root, text="Enviar Mensaje", command=enviar_mensaje)
button_send.pack()

# Botón para cerrar la aplicación
button_close = Button(root, text="Cerrar Aplicación", command=cerrar_aplicacion)
button_close.pack()

# Etiqueta para mostrar el estado
label_status = Label(root, textvariable=status_var)
label_status.pack()

# Elimina logs de la UI
label_status = Label(root, textvariable=status_var)
label_status.pack()

# Ejecutar la aplicación
root.mainloop()
