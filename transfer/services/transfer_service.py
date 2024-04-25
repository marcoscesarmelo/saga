import json

import requests
from flask import Flask, abort
from utils import config

from dal import amount_repo

app = Flask(__name__)



def get_amount(id) -> float:
    returned_amount = amount_repo.get_amount(id)
    return float(returned_amount)


def transfer(origin, destination, amount):
    previous_origin_amount = get_amount(origin)
    previous_destination_amount = get_amount(destination)
    new_origin_amount = previous_origin_amount - amount
    new_destination_amount = previous_destination_amount + amount

    try:
        take_origin(origin, amount)
        provide_destination(origin, destination, amount, previous_origin_amount,False)
        update_origin(origin, destination, new_origin_amount, False, previous_origin_amount, previous_destination_amount)
        update_destination(origin, destination, new_destination_amount, False, previous_origin_amount, previous_destination_amount)
        update_channel(origin, destination, new_origin_amount, new_destination_amount, False)
    except Exception as e:
        abort(config.status_nok, description="Service didn't return appropriate response: " + str(e))


def take_origin(origin, amount):
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.taker_url + str(origin), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        raise e


def provide_destination(origin, destination, amount, previous_amount, is_rollback):
    step = 2
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.provider_url + str(destination), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        if not is_rollback:
            undo_take_origin(origin, destination, previous_amount)
        else:
            amount_repo.send_to_failure(step, origin, destination, previous_amount)
        raise e


def update_origin(origin, destination, amount, is_rollback, previous_origin_amount, previous_destination_amount ):
    step = 3
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.provider_update + str(origin), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        if not is_rollback:
            undo_provide_destination(origin, destination, previous_destination_amount)
            undo_take_origin(origin, destination, previous_origin_amount)
        else:
            amount_repo.send_to_failure(step, origin, destination, amount)
        raise e


def update_destination(origin, destination, amount, is_rollback, previous_origin_amount, previous_destination_amount ):
    step = 4
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.taker_update + str(destination), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        if not is_rollback:
            undo_provide_destination(origin, destination, previous_destination_amount)
            undo_take_origin(origin, destination, previous_origin_amount)
        else:
            amount_repo.send_to_failure(step, origin, destination, amount)
        raise e


def update_channel(origin, destination, origin_amount, destination_amount, is_rollback):
    step = 5
    try:
        amount_repo.update_amount(origin, origin_amount)
        amount_repo.update_amount(destination, destination_amount)
    except Exception as e:
        if not is_rollback:
            undo_update_destination(origin, destination, destination_amount)
            undo_update_origin(origin, destination, origin_amount)
        else:
            amount_repo.send_to_failure(step, origin, destination, origin_amount)
            amount_repo.send_to_failure(step, origin, destination, destination_amount)
        raise e


def undo_take_origin(origin, destination, amount):
    step = 6
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.taker_update + str(origin), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        amount_repo.send_to_failure(step, origin, destination, amount)


def undo_provide_destination(origin, destination, amount):
    step = 7
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.provider_update + str(destination), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        amount_repo.send_to_failure(step, origin, destination, amount)


def undo_update_origin(origin, destination, amount):
    step = 8
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.provider_update + str(destination), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        amount_repo.send_to_failure(step, origin, destination, amount)


def undo_update_destination(origin, destination, amount):
    step = 9
    try:
        transfer_object = "{ \"amount\": " + str(amount) + "}"
        transfer_json_object = json.loads(transfer_object)
        response = requests.patch(config.taker_update + str(origin), json=transfer_json_object)
        if response.status_code != config.status_ok:
            raise ValueError("Service didn't return appropriate response: " + str(response.status_code))
    except Exception as e:
        amount_repo.send_to_failure(step, origin, destination, amount)