# WhatsappDic

## Iniciar el environment con:

### Windows:
python -m venv venv; ./venv/Scripts/Activate; pip --upgrade pip

### Linux/Macos:
pyton -m venv venv; venv\\Scripts\\activate.bat; pip --upgrade pip

## Instalamos las librerias
pip install -r requirements.txt

## Creamos cuenta en MongoDB y un Cluster para guardar las definiciones en la nube
https://cloud.mongodb.com/

## Creamos cuenta en Twilio para tener un numero de whatsapp
Para configurar el sandbox de Twilio para WhatsApp, vaya a Twilio Console. En Desarrollo, haga clic en Mensajería y, a continuación, en Probar. En Probar, haga clic en Enviar un mensaje de WhatsApp.
https://console.twilio.com/

## Creamos cuenta en NGROK 
Para recibir mensajes Twilio en el backend, utilizarás ngrok para alojar el host local en un servidor público.
https://dashboard.ngrok.com/

