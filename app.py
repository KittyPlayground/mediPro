from flask import Flask
from views import customer_views, medicine_views, order_views, home_views

app = Flask(__name__)

app.register_blueprint(home_views.bp)
app.register_blueprint(customer_views.bp)
app.register_blueprint(medicine_views.bp)
app.register_blueprint(order_views.bp)

if __name__ == "__main__":
    app.run(debug=True)
