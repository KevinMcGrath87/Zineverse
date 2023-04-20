from flask import Flask
from flask_assets import Environment, Bundle
app = Flask(__name__)
app.secret_key = '121812'

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle("main.scss", filters = "libsass", output ="css/scss-generated.css")

assets.register("scss_all", scss)
js = Bundle(
    "node_modules/jquery/dist/jquery.min.js",
    "node_modules/@popperjs/core/dist/umd/popper.min.js",
    "node_modules/bootstrap/dist/js/bootstrap.min.js",
    filters = "jsmin",
    output = "js/generated.js"

)

assets.register("js_all",js)