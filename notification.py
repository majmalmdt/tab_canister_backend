from flask import Flask
from flask_pywebpush import WebPush,WebPushException

app = Flask(__name__)
push = WebPush(private_key='some_value',
               sender_info='mailto:admin@server.com')
push.init_app(app)

@app.route('/',methods=['GET','POST'])
def index():
    notification = {
    'title': 'Test',
    'body': 'notification body',
    }
    subscription = {
    'endpoint': '---some-value---',
    'keys': { 'auth': '---some-value---', 'p256dh': '---some-value---' },
}
    try:
        push.send(subscription, notification)
    except WebPushException as exc:
        print(exc)
    return "hello"



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0" , port=8000)


