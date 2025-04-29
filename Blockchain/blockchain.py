#importing the libraries
import datetime
import hashlib
import json
from flask import Flask,jsonify


#Building a blockchain

class Blockchain:

    def __init__(self):
        # Creates an empty list self.chain to store all blocks.
        self.chain = []
        # Calls create_block() to generate the genesis block (the first block in the blockchain)
        self.create_block(proof=1 , previous_hash = '0')
    	
    #  Creates a new block and adds it to the chain.
        # proof: The proof of work (nonce) for this block.
        # previous_hash: The hash of the previous block.
    def create_block(self,proof,previous_hash):
        block = {
            'index':len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.chain.append(block)
        return block
    
    # Returns the last block in the blockchain (self.chain).
    def get_previous_block(self):
        return self.chain[-1]
    
    # Finds a number (new_proof) that solves the proof-of-work puzzle.
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False 
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof  


    # Generates a SHA256 hash of a block.
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Verifies whether the blockchain is valid and unaltered.
    def is_chain_valid (self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index< len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

#  Mining our blockchain

# creating a web app
app = Flask(__name__)

# creating a blockchain
blockchain = Blockchain()

# mining a new block
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message':'Congardualtions you just mined a block',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response),200

# getting the full blockchain
@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response),200

@app.route('/is_valid',methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)

    if is_valid:
        response = {'message' : 'All good blockchain is valid.'}
    else : 
        response = {'message' : 'Blockchain is not valid.'}
    return jsonify(response),200

#Running the app
app.run(host='0.0.0.0',port=5000)