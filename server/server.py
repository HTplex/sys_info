"""
By Yushi Hu Sep 07 2019
All Rights Reserved
"""
from flask import Flask
from get_status import get_machine_info

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    info = get_machine_info(print_result=False)
    info = info.split("\n")
    multiline_text = ""
    for info_line in info:
        multiline_text += '<p >' + info_line + '</p>'

    rendered_html = \
        """
    <html>
    <head>
        <title>Home</title>
        <style type="text/css">
            body {
            background-color: black;
            color: #32CD32;
            }
            p { 
            font-family: monaco, Consolas, Lucida Console, monospace; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; 
            line-height: 10px;
            white-space:pre;
            text-align: center;
            }
            h2 {
            text-align: center;
            }
        </style>
        <meta http-equiv="refresh" content="15">
    </head>
    <body>
        <h2>System Status</h2>""" + multiline_text + \
        """
    </body>
    </html>
    """
    return rendered_html


if __name__ == "__main__":
    app.run()
