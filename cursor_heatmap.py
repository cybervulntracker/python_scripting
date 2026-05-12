
# Simple Cursor Telemetry Tracker



from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser

PORT = 8080


HTML = """

<!DOCTYPE html>
<html>

<head>

    <title>Human Detector</title>

    <style>

        body {

            background: black;
            color: lime;
            font-family: Arial;
            margin: 0;
            overflow: hidden;

        }

        #box {

            position: fixed;
            top: 20px;
            left: 20px;

            background: rgba(0,0,0,0.8);

            padding: 15px;

            border: 1px solid lime;

        }

    </style>

</head>

<body>

<div id="box">

    <h2>Telemetry Tracker</h2>

    <p id="points">
        Points: 0
    </p>

    <p id="status">
        Status: Human
    </p>

</div>

<script>

    let points = 0;

    let lastX = 0;
    let lastY = 0;

    // Detect mouse movement
    document.addEventListener("mousemove", function(event){

        points++;

        let x = event.clientX;
        let y = event.clientY;

        // Distance moved
        let dx = x - lastX;
        let dy = y - lastY;

        let distance = Math.sqrt(dx*dx + dy*dy);

        lastX = x;
        lastY = y;

        // Update points
        document.getElementById("points").innerText =
            "Points: " + points;

        // Simple bot check
        if(distance > 300){

            document.getElementById("status").innerText =
                "Status: Suspicious";

        }
        else{

            document.getElementById("status").innerText =
                "Status: Human";

        }

    });

</script>

</body>
</html>

"""

# Create local server
class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            HTML.encode()
        )

# Start server
server = HTTPServer(
    ("127.0.0.1", PORT),
    MyServer
)

print(f"Running at http://127.0.0.1:{PORT}")

# Open browser automatically
webbrowser.open(
    f"http://127.0.0.1:{PORT}"
)

# Keep running
server.serve_forever()