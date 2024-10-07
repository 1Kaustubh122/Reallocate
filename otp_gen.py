import vonage

client = vonage.Client(key="abdefea5", secret="Q61qfUtljwgo0ggk")
sms = vonage.Sms(client)

responseData = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": "917303166961",
        "text": "A text message sent using the Nexmo SMS API",
    }
)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")