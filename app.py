from flask import Flask
from multiprocessing import Process
import time
from views import customer_views, medicine_views, order_views, home_views

app = Flask(__name__)

# Register blueprints for different views
app.register_blueprint(home_views.bp)
app.register_blueprint(customer_views.bp)
app.register_blueprint(medicine_views.bp)
app.register_blueprint(order_views.bp)


def worker():
    time.sleep(5)  # Simulate time-consuming task
    print("Background task completed.")


@app.route('/')
def index():
    p = Process(target=worker)
    p.start()
    p.join()
    return "Hello, World! Background task is running."


if __name__ == "__main__":
    app.run(debug=True)
