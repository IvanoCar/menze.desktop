from flask import Blueprint, render_template, request
from app import ESSENTIALS, DATABASE, API_CLIENT
from app.modules.utils import utility

from app.modules.api_client.exceptions import UpdateFailed

from app.modules.pdf.viewer import  PDFViewerProcess
from app.modules.pdf.generation import PDF

import time
import json

processing_mod = Blueprint('processing_mod', __name__)


@processing_mod.route('/send-data', methods=['POST'])
def send_after_no_internet():
    if utility.Utility.check_internet():
        try:        
            API_CLIENT.update_food(ESSENTIALS.session['restaurant_id'], {'food': DATABASE.storage['food'] })
            return json.dumps({'status': 'OK', 'redirect': '/dashboard-sent'})
        except UpdateFailed:
            return json.dumps({'status': 'API error', 'redirect': '/api-error'})
    return json.dumps({'status': 'no internet', 'redirect': '/no-internet'})


@processing_mod.route('/processing', methods=['POST'])
def process_data():
    data = request.get_json()

    ESSENTIALS.make_storage_dir()

    timestamp = time.strftime('%d-%m-%Y %H:%M:%S')
    timestamp_filename = timestamp.replace(':', '.')

    users = DATABASE.storage['users']
    data['food']['last-update'] = timestamp

    DATABASE.storage['food'] = data['food']
    DATABASE.storage['users'] = users

    DATABASE.save()

    menus_html = render_template('pdfs/menus-template.html', restaurant=ESSENTIALS.session['restaurant'],
                                 food=DATABASE.storage['food'])
    other_html = render_template('pdfs/other-template.html', restaurant=ESSENTIALS.session['restaurant'],
                                 food=DATABASE.storage['food'])

    menus_pdf = PDF(menus_html)
    menus_pdf.save(ESSENTIALS.pdf_location, 'MENIJI', timestamp_filename)

    other_pdf = PDF(other_html)
    other_pdf.save(ESSENTIALS.pdf_location, 'OSTALO', timestamp_filename)

    PDFViewerProcess(menus_pdf.path, 'Meniji').start()
    PDFViewerProcess(other_pdf.path, 'Ostalo').start()

    if utility.Utility.check_internet():
        try:        
            API_CLIENT.update_food(ESSENTIALS.session['restaurant_id'], {'food': data['food'] })
        except UpdateFailed:
            return json.dumps({'status': 'API error', 'redirect': '/api-error'})
        return json.dumps({'status': 'OK', 'redirect': '/dashboard-sent'})
    return json.dumps({'status': 'no internet', 'redirect': '/no-internet'})
