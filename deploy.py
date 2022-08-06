#// SPDX-License-Identifier: MIT
from solcx import compile_standard,install_solc
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv() 
import json
with open("./MyContract.sol","r") as file:
    simple_file=file.read()
    # print(simple_file)
    install_solc("0.8.7")
    compiled_sol=compile_standard(
        {
            "language":"Solidity",
            "sources":{"MyContract.sol":{"content":simple_file}},
            "settings":{
                "outputSelection":{
                "*":{"*":["abi","metadata","evm.bytecode","evm.sourceMap"]}
            }
            },
        },
        solc_version="0.8.7",
    )
    # print(compiled_sol)
    with open("compiled_code.json","w") as file:
        json.dump(compiled_sol,file)
        #get bytecode
        bytecode=compiled_sol["contracts"]["MyContract.sol"]["MyContract"]["evm"]["bytecode"]["object"]
        #get abi
        abi=compiled_sol["contracts"]["MyContract.sol"]["MyContract"]["abi"]
        #for connectiong tp ganache
        w3=Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        chain_id=1337
        my_address="0x7f0A12DB8E099123955ab7f896dbFF27B75ba189"
        private_key=os.getenv("PRIVATE_KEY")
        print(private_key)
        MyContract=w3.eth.contract(abi=abi,bytecode=bytecode)
        nonce=w3.eth.getTransactionCount(my_address)
        print("Deploy")
        transaction=MyContract.constructor().buildTransaction({
           "chainId":chain_id,"from":my_address,"nonce":nonce
        })
        signed_txn=w3.eth.account.sign_transaction(transaction=transaction,private_key=private_key)
        print(signed_txn)
        tx_hash=w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
        simple_storage=w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
        print(simple_storage.functions.balance().call())
        stransaction=simple_storage.functions.initialise("Harsh").buildTransaction({"chainId":chain_id,"from":my_address,"nonce":nonce+1})
        signed_transaction=w3.eth.account.sign_transaction(stransaction,private_key=private_key)
        print("deploy")
        transaction_hash=w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        tx_receipt=w3.eth.wait_for_transaction_receipt(transaction_hash)
        print(simple_storage.functions.getname().call())