from flask import Flask, render_template, request, jsonify
import os
import math
import statistics
import socket
import stats_calculator

app = Flask(__name__)

def get_local_ip():
    """Detects the local IPv4 address for network access by Android devices."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def get_port():
    """Reads the PORT environment variable provided by Render or defaults to 5000."""
    return int(os.environ.get('PORT', 5000))

def _args_to_list(args):
    """Helper to allow statistical functions to accept either comma-separated args or a list."""
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return list(args[0])
    return list(args)

def get_allowed_eval_names():
    """Builds a safe dictionary of mathematical and statistical functions for expression evaluation."""
    # Base mathematical functions from standard math module
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    
    # Safe built-in functions
    allowed.update({
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'ln': math.log,
        'log10': math.log10,
        'pi': math.pi,
        'e': math.e,
        # Statistical functions accessible directly inside expressions
        'sum': lambda *a: sum(_args_to_list(a)),
        'mean': lambda *a: statistics.mean(_args_to_list(a)),
        'median': lambda *a: statistics.median(_args_to_list(a)),
        'mode': lambda *a: statistics.mode(_args_to_list(a)),
        'stdev': lambda *a: statistics.stdev(_args_to_list(a)),
        'pstdev': lambda *a: statistics.pstdev(_args_to_list(a)),
        'var': lambda *a: statistics.variance(_args_to_list(a)),
        'variance': lambda *a: statistics.variance(_args_to_list(a)),
        'pvariance': lambda *a: statistics.pvariance(_args_to_list(a)),
    })
    return allowed

@app.route('/manifest.json', methods=['GET'])
def manifest():
    """Web app manifest for Android PWA installation (Add to Home screen)."""
    return jsonify({
        "name": "PNC Scientific & Statistical Calculator",
        "short_name": "PNC-Calc",
        "description": "Scientific & Statistical Calculator with step-by-step processes for PC and Android",
        "start_url": "/",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#121316",
        "theme_color": "#1e2025",
        "icons": [
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%231e2025'/><text x='50' y='65' font-size='50' text-anchor='middle' fill='%234caf50'>%F0%9F%A7%AE</text></svg>",
                "sizes": "192x192 512x512",
                "type": "image/svg+xml"
            }
        ]
    })

@app.route('/', methods=['GET'])
def index():
    local_ip = get_local_ip()
    return render_template('index.html', active_tab='scientific', local_ip=local_ip, port=get_port())

@app.route('/calculate', methods=['POST'])
def calculate():
    is_json = request.is_json
    if is_json:
        data = request.get_json() or {}
        expression = data.get('expression', '')
    else:
        expression = request.form.get('expression', '')

    calc_expr = expression.replace('^', '**')
    error = None
    result = None

    if not expression.strip():
        result = ""
    else:
        try:
            allowed_names = get_allowed_eval_names()
            raw_res = eval(calc_expr, {"__builtins__": {}}, allowed_names)
            
            if isinstance(raw_res, float):
                if raw_res.is_integer():
                    result = int(raw_res)
                else:
                    result = stats_calculator.format_num(raw_res, max_decimals=6)
            elif isinstance(raw_res, list):
                result = [stats_calculator.format_num(x) if isinstance(x, (int, float)) else x for x in raw_res]
            else:
                result = raw_res
        except Exception as e:
            error = f"Error: {str(e)}"
            result = error

    if is_json:
        return jsonify({
            'success': error is None,
            'expression': expression,
            'result': result,
            'error': error
        })
    
    local_ip = get_local_ip()
    port = get_port()
    return render_template(
        'index.html', 
        active_tab='scientific', 
        result=result, 
        expression=expression,
        local_ip=local_ip,
        port=port
    )

@app.route('/calculate-stats', methods=['POST'])
def calculate_stats():
    is_json = request.is_json
    if is_json:
        req_data = request.get_json() or {}
        data_input = req_data.get('data_input', '')
    else:
        data_input = request.form.get('data_input', '')

    try:
        data_list = stats_calculator.parse_dataset(data_input)
        stats_data = stats_calculator.calculate_full_statistics(data_list)
        error = None
    except Exception as e:
        stats_data = None
        error = str(e)

    if is_json:
        if error:
            return jsonify({'success': False, 'error': error}), 400
        return jsonify({
            'success': True,
            'data_input': data_input,
            'stats': stats_data
        })

    local_ip = get_local_ip()
    port = get_port()
    return render_template(
        'index.html',
        active_tab='stats',
        data_input=data_input,
        stats_data=stats_data,
        stats_error=error,
        local_ip=local_ip,
        port=port
    )

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = get_port()
    print("=" * 65)
    print(" 🚀 Scientific & Statistical Calculator Server Started!")
    print(f" 💻 Personal Computer (Local):  http://127.0.0.1:{port}")
    print(f" 📱 Android Devices (Network):   http://{local_ip}:{port}")
    print(" (Make sure PC and Android device are on the same Wi-Fi)")
    print("=" * 65)
    app.run(host='0.0.0.0', port=port, debug=True)