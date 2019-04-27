from argparse import ArgumentParser

import flask
from flask import Flask, request, render_template, session, redirect, url_for
import json
from blockchain import Blockchain
import os
app = Flask(__name__)
address = ''
blockchain = Blockchain()


def new_node(peer):
    if not peer:
        return flask.jsonify({
            'message': 'peer\'s address missing'
        }), 400
    blockchain.register(peer)
    return flask.jsonify({
        'message': f"peer at {peer} added "
                   f"(total: {len(blockchain.peers)})"
    })

def set_auth(peer):
    if not peer:
        return flask.jsonify({
            'message': 'authority\'s address missing'
        }), 400

    blockchain.set_authority(peer)

    return flask.jsonify({
        'message': f"authority set at {peer}"
    })

@app.route('/')
def base():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        context = {
            'message': f'running on {address}',
            'chain': blockchain.blocs
        }
        role = session.get('logged_in')
        if(role == 'node'):
            template = 'node.html' #can create transactions and see all nodes
        else:
            template = 'auth.html'  #can call mine function and see all nodes
        return render_template(template, context=context)

@app.route('/login', methods=['POST'])
def admin_login():
    t = request.form['userType']
    session['logged_in'] = t
    peer = request.remote_addr
    if(t == 'node'):
        new_node(peer)
    else:
        set_auth(peer)
    return redirect(url_for('base'))

@app.route('/mine')
def mine():
    context = dict()
    context['chain'] = blockchain.blocs
    if(session.get('logged_in') == 'authority'):
        updated = blockchain.mine(miner = request.remote_addr)
        if(updated==0): message = 'Block Mined'
        elif(updated==1): message = 'Forge trigger not reached'
        context['message']= message
        return render_template('auth.html', context=context)
    else:
        context['message'] = 'No Auth to mine blocks'
        return render_template('auth.html', context=context)
@app.route('/sync')
def sync():
    changed = blockchain.sync()
    return flask.jsonify({
        'message': 'chain updated' if changed else 'chain up to date'
    })


@app.route('/transaction', methods=['POST'])
def new_transaction():
    payload = dict(request.form)
    blockchain.new_transaction(
        sender=request.remote_addr,
        content=payload
    )
    context = {
        'message': 'transaction added',
        'chain': blockchain.blocs
    }
    return render_template('node.html',context=context)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    parser = ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        default=5000,
        type=int,
        help='port to listen on'
    )
    parser.add_argument(
        '-ht',
        '--host',
        default='127.0.0.1',
        type=str,
        help='peer\'s host'
    )
    args = parser.parse_args()

    port = args.port
    host = args.host

    address = f'{host}:{port}'

    app.run(host=host, port=port, debug=True)
