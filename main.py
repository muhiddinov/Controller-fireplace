from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from gpio_module import GPIOModule, PWMModule

app = Microdot()

Response.default_content_type = 'text/html'

@app.route('/', methods=['GET'])
async def index(request):
    
    return render_template('index.html', work=False)

@app.route('/yellow')
async def toggle_power(request):
    print("Receive Yellow Toggle Request!")
    return "OK"

@app.route('/blue')
async def toggle_power(request):
    print("Receive Blue Toggle Request!")
    return "OK"

@app.route('/red')
async def toggle_power(request):
    print("Receive Red Toggle Request!")
    return "OK"

@app.route('/orange')
async def toggle_power(request):
    print("Receive Orange Toggle Request!")
    return "OK"

@app.route('/green')
async def toggle_power(request):
    print("Receive Green Toggle Request!")
    return "OK"

@app.route('/togglePower')
async def toggle_power(request):
    print("Receive Power Toggle Request!")
    return "OK"

@app.route('/cooler', methods=['GET'])
async def set_cooler(request):
    pwm_val = int(request.args['value'])
    return "OK"


@app.route('/volume', methods=['GET'])
async def set_volume(request):
    pwm_val = int(request.args['value'])
    return "OK"

@app.route('/brigtness', methods=['GET'])
async def set_brigtness(request):
    pwm_val = int(request.args['value'])
    return "OK"

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        return 'Not found', 404
    return send_file('static/' + path)

app.run(debug=False, port=80)