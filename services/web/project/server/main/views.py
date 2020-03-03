# services/web/server/main/views.py


import redis
from rq import Queue, push_connection, pop_connection
from flask import current_app, render_template, Blueprint, jsonify, request
from time import sleep
from server.main.tasks import *

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.route('/', methods=['GET'])
def home():
    return render_template('main/home.html')

@main_blueprint.route('/getRecentItems', methods=['GET'])
@main_blueprint.route('/getBrandsCount', methods=['GET'])
@main_blueprint.route('/getItemsbyColor', methods=['GET'])


def run_recent():
    q = Queue()
    if 'getRecentItems' in request.url_rule.rule:
        function = 'get_recent'
        param = request.args.get('date')
    elif 'getBrandsCount' in request.url_rule.rule:
        function ='get_brand_count'
        param = request.args.get('date')
    elif 'getItemsbyColor' in request.url_rule.rule:
        function ='get_by_color'
        param = request.args.get('color')

    task = q.enqueue(get_result,function,param)
    task_id = task.get_id()

    while task.get_status() not in ('finished','failed'):
        task = q.fetch_job(task_id)

    if task:
        if task.status =='finished':
            response_object = {
                            'status': 'success',
                            'data': task.result
                           }
        else :
            response_object = {
                'status': 'failed',
                'data': task.result
            }

    else:
        response_object = {'status': 'error',
                            'data':None}
    return jsonify(response_object)

@main_blueprint.before_request
def push_rq_connection():
    push_connection(redis.from_url(current_app.config['REDIS_URL']))


@main_blueprint.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()
