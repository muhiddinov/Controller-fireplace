from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from gpio_module import GPIOModule, PWMModule
from btn_iface import ButtonIfaceThread

appIFace = ButtonIfaceThread()

app = Microdot()

Response.default_content_type = 'text/html'

@app.route('/', methods=['GET'])
async def index(request):
    return render_template('index.html', work=appIFace.start())

@app.route('/yellow')
async def toggle_yellow(request):
    appIFace.setColorToRGB('yellow')
    return "OK"

@app.route('/blue')
async def toggle_blue(request):
    appIFace.setColorToRGB('blue')
    return "OK"

@app.route('/red')
async def toggle_red(request):
    appIFace.setColorToRGB('red')
    return "OK"

@app.route('/orange')
async def toggle_orange(request):
    appIFace.setColorToRGB('orange')
    return "OK"

@app.route('/green')
async def toggle_green(request):
    appIFace.setColorToRGB('green')
    return "OK"

@app.route('/work')
async def toggle_power(request):
    state = request.args['value']
    if state == 'true':
        appIFace.start(1)
    else:
        appIFace.start(0)
    return "OK"

@app.route('/cooler', methods=['GET'])
async def set_cooler(request):
    pwm_val = int(request.args['value'])
#     appIFace.coolerSpeed(pwm_val)
    appIFace.coolerSpeedInc()
    return "OK"


@app.route('/volume', methods=['GET'])
async def set_volume(request):
    pwm_val = int(request.args['value'])
    appIFace.volume(pwm_val)
    return "OK"

@app.route('/brigtness', methods=['GET'])
async def set_brigtness(request):
    pwm_val = int(request.args['value'])
    appIFace.brighness(pwm_val)
    return "OK"

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    appIFace.shutdown()
    return 'The server is shutting down...'

@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        return 'Not found', 404
    return send_file('static/' + path)

appIFace.run()
app.run(debug=False, port=80)