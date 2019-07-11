import logging

from flask import Blueprint, redirect, jsonify, current_app, request


bp = Blueprint("auth", __name__)


@bp.route('/auth', methods=['GET'])
def auth():
    return redirect(
        current_app.spotify._authorization_code_flow_authentication()
    )


@bp.route('/callback')
def callback():
    response = current_app.spotify._client_credentials_authentication(
        request.args['code']
    )

    current_app.spotify._access_token = response['access_token']
    token_type = response['token_type']
    current_app.spotify._token_expires_in = response['expires_in']

    logging.info('authenticated')

    return jsonify(
        authenticated=True,
        token_type=token_type,
        token_expires_in=current_app.spotify._token_expires_in
    )
