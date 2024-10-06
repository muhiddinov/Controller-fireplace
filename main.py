from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from gpio_module import GPIOModule, PWMModule
from btn_iface import ButtonIfaceThread

btnApp = ButtonIfaceThread()
app = Microdot()

Response.default_content_type = 'text/html'

# Our GPIO Module
power = GPIOModule(23)   # Вкл/выкл
cooler = PWMModule(22)   # Кулер
volume = PWMModule(4)    # Звук
brigtness = PWMModule(2) # Яркость

yellow = GPIOModule(25)  # LED Yellow
blue = GPIOModule(26)    # LED Blue
red = GPIOModule(27)     # LED Red
orange = GPIOModule(32)  # LED Orange
green = GPIOModule(33)   # LED Green



@app.route('/', methods=['GET'])
async def index(request):
    return render_template('index.html', work=power.get_value(), cool=cooler.get_value())

@app.route('/yellow')
async def toggle_power(request):
    print("Receive Yellow Toggle Request!")
    yellow.toggle()
    return "OK"

@app.route('/blue')
async def toggle_power(request):
    print("Receive Blue Toggle Request!")
    blue.toggle()
    return "OK"

@app.route('/red')
async def toggle_power(request):
    print("Receive Red Toggle Request!")
    red.toggle()
    return "OK"

@app.route('/orange')
async def toggle_power(request):
    print("Receive Orange Toggle Request!")
    orange.toggle()
    return "OK"

@app.route('/green')
async def toggle_power(request):
    print("Receive Green Toggle Request!")
    green.toggle()
    return "OK"

@app.route('/togglePower')
async def toggle_power(request):
    print("Receive Power Toggle Request!")
    power.toggle()
    return "OK"

@app.route('/cooler', methods=['GET'])
async def set_cooler(request):
    pwm_val = int(request.args['value'])
    cooler.set_pwm(int(pwm_val/6*100))
    print("Cooler:", cooler.get_value())
    return "OK"


@app.route('/volume', methods=['GET'])
async def set_volume(request):
    pwm_val = int(request.args['value'])
    volume.set_pwm(pwm_val)
    print("Volume:", volume.get_value())
    return "OK"

@app.route('/brigtness', methods=['GET'])
async def set_brigtness(request):
    pwm_val = int(request.args['value'])
    brigtness.set_pwm(pwm_val)
    print("Brightness:", brigtness.get_value())
    return "OK"

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

btnApp.run()
app.run(debug=False, port=80)