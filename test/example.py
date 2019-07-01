#!/usr/bin/env python

import time

import web3 # Web3, HTTPProvider

class Example:

    def __init__(self):
        # after the transaction has been send we wait this time for it to be mined
        self.MAX_RETRIES = 10
        self.SECONDS_BETWEEN_RETRIES = 1

        client_url = "https://rpc.slock.it/tobalaba"
        wallet_add = "0x68F89f072A37c9571733E899EFF7219a03d51bb0"
        wallet_pwd = "f97120b63afc4a6c622a4131687ac6d3ef068590beec04276a3d13bc4148c12b"

        contract = {
            "address": "0xc68fb291a6ddf3d4d9e3a061de39563bf269d868",
            "abi": [{'constant': False,
                    'inputs': [{'name': '_assetId', 'type': 'uint256'}, {'name': '_newSmartMeter', 'type': 'address'}],
                    'name': 'updateSmartMeter', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable',
                    'type': 'function'},
                    {'constant': True, 'inputs': [{'name': '_assetId', 'type': 'uint256'}], 'name': 'getAssetLocation',
                    'outputs': [{'name': 'country', 'type': 'bytes32'}, {'name': 'region', 'type': 'bytes32'},
                                {'name': 'zip', 'type': 'bytes32'}, {'name': 'city', 'type': 'bytes32'},
                                {'name': 'street', 'type': 'bytes32'}, {'name': 'houseNumber', 'type': 'bytes32'},
                                {'name': 'gpsLatitude', 'type': 'bytes32'}, {'name': 'gpsLongitude', 'type': 'bytes32'}],
                    'payable': False, 'stateMutability': 'view', 'type': 'function'},
                    {'constant': False, 'inputs': [{'name': '_dbAddress', 'type': 'address'}], 'name': 'init', 'outputs': [],
                    'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                    {'constant': False, 'inputs': [{'name': '_newLogic', 'type': 'address'}], 'name': 'update', 'outputs': [],
                    'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                    {'constant': False, 'inputs': [], 'name': 'createAsset', 'outputs': [], 'payable': False,
                    'stateMutability': 'nonpayable', 'type': 'function'},
                    {'constant': True, 'inputs': [], 'name': 'db', 'outputs': [{'name': '', 'type': 'address'}],
                    'payable': False, 'stateMutability': 'view', 'type': 'function'},
                    {'constant': False, 'inputs': [
                    {'name': '_assetId', 'type': 'uint256'}, {'name': '_country', 'type': 'bytes32'},
                    {'name': '_region', 'type': 'bytes32'}, {'name': '_zip', 'type': 'bytes32'},
                    {'name': '_city', 'type': 'bytes32'}, {'name': '_street', 'type': 'bytes32'},
                    {'name': '_houseNumber', 'type': 'bytes32'}, {'name': '_gpsLatitude', 'type': 'bytes32'},
                    {'name': '_gpsLongitude', 'type': 'bytes32'}], 'name': 'initLocation', 'outputs': [], 'payable': False,
                                                                                        'stateMutability': 'nonpayable',
                                                                                        'type': 'function'},
                    {'constant': True, 'inputs': [], 'name': 'getAssetListLength', 'outputs': [{'name': '', 'type': 'uint256'}],
                    'payable': False, 'stateMutability': 'view', 'type': 'function'},
                    {'constant': True, 'inputs': [], 'name': 'cooContract', 'outputs': [{'name': '', 'type': 'address'}],
                    'payable': False, 'stateMutability': 'view', 'type': 'function'},
                    {'constant': True, 'inputs': [{'name': '_role', 'type': 'uint8'}, {'name': '_caller', 'type': 'address'}],
                    'name': 'isRole', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view',
                    'type': 'function'},
                    {'constant': True, 'inputs': [{'name': '_assetId', 'type': 'uint256'}], 'name': 'getActive',
                    'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view',
                    'type': 'function'},
                    {'constant': False, 'inputs': [{'name': '_assetId', 'type': 'uint256'},
                                                                        {'name': '_active', 'type': 'bool'}],
                                        'name': 'setActive', 'outputs': [], 'payable': False,
                                        'stateMutability': 'nonpayable', 'type': 'function'},
                    {'constant': True, 'inputs': [{'name': '_assetId', 'type': 'uint256'}],
                    'name': 'getLastSmartMeterReadFileHash', 'outputs': [{'name': 'datalog', 'type': 'bytes32'}],
                    'payable': False, 'stateMutability': 'view', 'type': 'function'},
                    {'inputs': [{'name': '_cooContract', 'type': 'address'}], 'payable': False, 'stateMutability': 'nonpayable',
                    'type': 'constructor'}, {'anonymous': False,
                                            'inputs': [{'indexed': True, 'name': '_assetId', 'type': 'uint256'},
                                                        {'indexed': True, 'name': '_fileHash', 'type': 'bytes32'},
                                                        {'indexed': False, 'name': '_oldMeterRead', 'type': 'uint256'},
                                                        {'indexed': False, 'name': '_newMeterRead', 'type': 'uint256'},
                                                        {'indexed': False, 'name': '_certificatesUsedForWh',
                                                        'type': 'uint256'},
                                                        {'indexed': False, 'name': '_smartMeterDown', 'type': 'bool'}],
                                            'name': 'LogNewMeterRead', 'type': 'event'}, {'anonymous': False, 'inputs': [
                    {'indexed': False, 'name': 'sender', 'type': 'address'},
                    {'indexed': True, 'name': '_assetId', 'type': 'uint256'}], 'name': 'LogAssetCreated', 'type': 'event'},
                    {'anonymous': False, 'inputs': [{'indexed': True, 'name': '_assetId', 'type': 'uint256'}],
                    'name': 'LogAssetFullyInitialized', 'type': 'event'},
                    {'anonymous': False, 'inputs': [{'indexed': True, 'name': '_assetId', 'type': 'uint256'}],
                    'name': 'LogAssetSetActive', 'type': 'event'},
                    {'anonymous': False, 'inputs': [{'indexed': True, 'name': '_assetId', 'type': 'uint256'}],
                    'name': 'LogAssetSetInactive', 'type': 'event'},
                    {'constant': False,
                                                                    'inputs': [{'name': '_assetId', 'type': 'uint256'},
                                                                                {'name': '_smartMeter', 'type': 'address'},
                                                                                {'name': '_owner', 'type': 'address'},
                                                                                {'name': '_operationalSince',
                                                                                'type': 'uint256'},
                                                                                {'name': '_capacityWh', 'type': 'uint256'},
                                                                                {'name': 'maxCapacitySet', 'type': 'bool'},
                                                                                {'name': '_active', 'type': 'bool'}],
                                                                    'name': 'initGeneral', 'outputs': [], 'payable': False,
                                                                    'stateMutability': 'nonpayable', 'type': 'function'},
                    {'constant': False,
                    'inputs': [{'name': '_assetId', 'type': 'uint256'}, {'name': '_newMeterRead', 'type': 'uint256'},
                                {'name': '_lastSmartMeterReadFileHash', 'type': 'bytes32'},
                                {'name': '_smartMeterDown', 'type': 'bool'}], 'name': 'saveSmartMeterRead', 'outputs': [],
                    'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                    {'constant': True, 'inputs': [{'name': '_assetId', 'type': 'uint256'}], 'name': 'getAssetGeneral',
                    'outputs': [{'name': '_smartMeter', 'type': 'address'}, {'name': '_owner', 'type': 'address'},
                                {'name': '_operationalSince', 'type': 'uint256'}, {'name': '_capacityWh', 'type': 'uint256'},
                                {'name': '_maxCapacitySet', 'type': 'bool'},
                                {'name': '_lastSmartMeterReadWh', 'type': 'uint256'},
                                {'name': '_certificatesUsedForWh', 'type': 'uint256'}, {'name': '_active', 'type': 'bool'},
                                {'name': '_lastSmartMeterReadFileHash', 'type': 'bytes32'}], 'payable': False,
                    'stateMutability': 'view', 'type': 'function'},
                    {'constant': True, 'inputs': [{'name': '_assetId', 'type': 'uint256'}], 'name': 'getConsumingProperies',
                    'outputs': [{'name': 'capacityWh', 'type': 'uint256'}, {'name': 'maxCapacitySet', 'type': 'bool'},
                                {'name': 'certificatesUsedForWh', 'type': 'uint256'}], 'payable': False,
                    'stateMutability': 'view', 'type': 'function'},
                    {'constant': False,
                                                                    'inputs': [{'name': '_assetId', 'type': 'uint256'},
                                                                                {'name': '_consumed', 'type': 'uint256'}],
                                                                    'name': 'setConsumptionForPeriode', 'outputs': [],
                                                                    'payable': False, 'stateMutability': 'nonpayable',
                                                                    'type': 'function'}],
            "bytecode": '0x6060604052341561000f57600080fd5b6040516020806114408339810160405280805160008054600160a060020a03909216600160a060020a031990921691909117905550506113ec806100546000396000f3006060604052600436106100e25763ffffffff60e060020a6000350416630705244281146100e75780631314394d1461010b57806319ab453c146101685780631c1b877214610187578063244a613a146101a6578063312f9a8c146101de57806331a5daf3146102185780634d655aff1461022b5780637715ad901461025a5780639963aece1461027b578063a861c6ef146102aa578063ade1e992146102c3578063ae51439c14610331578063b1f2cc9d14610356578063bb5a389e14610369578063c53fb1a5146103a2578063e60a955d146103b8578063f7105c05146103d3575b600080fd5b34156100f257600080fd5b610109600435600160a060020a03602435166103e9565b005b341561011657600080fd5b610121600435610487565b60405197885260208801969096526040808801959095526060870193909352608086019190915260a085015260c084015260e0830191909152610100909101905180910390f35b341561017357600080fd5b610109600160a060020a036004351661054a565b341561019257600080fd5b610109600160a060020a03600435166105a7565b34156101b157600080fd5b610109600435600160a060020a036024358116906044351660643560843560a435151560c435151561062b565b34156101e957600080fd5b6101f4600435610736565b60405192835290151560208301526040808301919091526060909101905180910390f35b341561022357600080fd5b6101096107c0565b341561023657600080fd5b61023e610880565b604051600160a060020a03909116815260200160405180910390f35b341561026557600080fd5b610109600435602435604435606435151561088f565b341561028657600080fd5b61010960043560243560443560643560843560a43560c43560e43561010435610c0c565b34156102b557600080fd5b610109600435602435610cc0565b34156102ce57600080fd5b6102d9600435610d92565b604051600160a060020a03998a1681529790981660208801526040808801969096526060870194909452911515608086015260a085015260c0840152151560e083015261010082019290925261012001905180910390f35b341561033c57600080fd5b610344610e70565b60405190815260200160405180910390f35b341561036157600080fd5b61023e610ed9565b341561037457600080fd5b61038e60ff60043516600160a060020a0360243516610ee8565b604051901515815260200160405180910390f35b34156103ad57600080fd5b61038e600435611063565b34156103c357600080fd5b61010960043560243515156110d6565b34156103de57600080fd5b6103446004356111d3565b600154600160a060020a0316151561040057600080fd5b600261040c8133610ee8565b151561041757600080fd5b600154600160a060020a0316630ff85b94848460405160e060020a63ffffffff85160281526004810192909252600160a060020a03166024820152604401600060405180830381600087803b151561046e57600080fd5b6102c65a03f1151561047f57600080fd5b505050505050565b6001546000908190819081908190819081908190600160a060020a0316631314394d8a83604051610100015260405160e060020a63ffffffff8416028152600481019190915260240161010060405180830381600087803b15156104ea57600080fd5b6102c65a03f115156104fb57600080fd5b5050506040518051906020018051906020018051906020018051906020018051906020018051906020018051906020018051905097509750975097509750975097509750919395975091939597565b60006105568133610ee8565b151561056157600080fd5b600154600160a060020a03161561057757600080fd5b506001805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a0392909216919091179055565b600054600160a060020a0390811690331681146105c357600080fd5b600154600160a060020a031663a6f9dae18360405160e060020a63ffffffff8416028152600160a060020a039091166004820152602401600060405180830381600087803b151561061357600080fd5b6102c65a03f1151561062457600080fd5b5050505050565b600154600160a060020a0316151561064257600080fd5b60048561064f8282610ee8565b151561065a57600080fd5b60026106668133610ee8565b151561067157600080fd5b600154600160a060020a031663de280a638b8b8b8b8b8b6000808d8160405160e060020a63ffffffff8d16028152600481019a909a52600160a060020a0398891660248b015296909716604489015260648801949094526084870192909252151560a486015260c485015260e484015290151561010483015261012482015261014401600060405180830381600087803b151561070d57600080fd5b6102c65a03f1151561071e57600080fd5b50505061072a8a611226565b50505050505050505050565b60015460009081908190600160a060020a031663312f9a8c85836040516060015260405160e060020a63ffffffff84160281526004810191909152602401606060405180830381600087803b151561078d57600080fd5b6102c65a03f1151561079e57600080fd5b5050506040518051906020018051906020018051929791965091945092505050565b600060026107ce8133610ee8565b15156107d957600080fd5b600154600160a060020a03166331a5daf36000604051602001526040518163ffffffff1660e060020a028152600401602060405180830381600087803b151561082157600080fd5b6102c65a03f1151561083257600080fd5b505050604051805190509150817fd3ab0c36887772472a25b1c1cecc0dee794b7c5ca472edaa2db255346878ee6b33604051600160a060020a03909116815260200160405180910390a25050565b600154600160a060020a031681565b600154600090600160a060020a031615156108a957600080fd5b600154600160a060020a031663ed9c058b8660006040516020015260405160e060020a63ffffffff84160281526004810191909152602401602060405180830381600087803b15156108fa57600080fd5b6102c65a03f1151561090b57600080fd5b5050506040518051905080600160a060020a031633600160a060020a031614151561093557600080fd5b600154600160a060020a031663c53fb1a58760006040516020015260405160e060020a63ffffffff84160281526004810191909152602401602060405180830381600087803b151561098657600080fd5b6102c65a03f1151561099757600080fd5b5050506040518051905015156109ac57600080fd5b600154600160a060020a031663042157c28760006040516020015260405160e060020a63ffffffff84160281526004810191909152602401602060405180830381600087803b15156109fd57600080fd5b6102c65a03f11515610a0e57600080fd5b505050604051805160015490935085915087907fa0ab5f173b69a28f81848a665a77213faedda299f939f047032c1e714ce6e94b9085908990600160a060020a031663b91dccde8560006040516020015260405160e060020a63ffffffff84160281526004810191909152602401602060405180830381600087803b1515610a9557600080fd5b6102c65a03f11515610aa657600080fd5b5050506040518051905088604051938452602084019290925260408084019190915290151560608301526080909101905180910390a3600154600160a060020a031663a60b6fdc878660405160e060020a63ffffffff851602815260048101929092526024820152604401600060405180830381600087803b1515610b2a57600080fd5b6102c65a03f11515610b3b57600080fd5b5050600154600160a060020a031690506357c3bc60878760405160e060020a63ffffffff851602815260048101929092526024820152604401600060405180830381600087803b1515610b8d57600080fd5b6102c65a03f11515610b9e57600080fd5b5050600154600160a060020a031690506336016d71874260405160e060020a63ffffffff851602815260048101929092526024820152604401600060405180830381600087803b1515610bf057600080fd5b6102c65a03f11515610c0157600080fd5b505050505050505050565b600154600160a060020a03161515610c2357600080fd5b6002610c2f8133610ee8565b1515610c3a57600080fd5b600154600160a060020a0316639963aece8b8b8b8b8b8b8b8b8b60405160e060020a63ffffffff8c160281526004810199909952602489019790975260448801959095526064870193909352608486019190915260a485015260c484015260e483015261010482015261012401600060405180830381600087803b151561070d57600080fd5b60008054600160a060020a03169063a34b80b090604051602001526040518163ffffffff1660e060020a028152600401602060405180830381600087803b1515610d0957600080fd5b6102c65a03f11515610d1a57600080fd5b5050506040518051905080600160a060020a031633600160a060020a0316141515610d4457600080fd5b600154600160a060020a031663c2791306848460405160e060020a63ffffffff851602815260048101929092526024820152604401600060405180830381600087803b151561046e57600080fd5b6000806000806000806000806000600160009054906101000a9004600160a060020a0316600160a060020a031663ade1e9928b6000604051610120015260405160e060020a63ffffffff8416028152600481019190915260240161012060405180830381600087803b1515610e0657600080fd5b6102c65a03f11515610e1757600080fd5b505050604051805190602001805190602001805190602001805190602001805190602001805190602001805190602001805190602001805190509850985098509850985098509850985098509193959799909294969850565b600154600090600160a060020a031663ae51439c82604051602001526040518163ffffffff1660e060020a028152600401602060405180830381600087803b1515610eba57600080fd5b6102c65a03f11515610ecb57600080fd5b505050604051805191505090565b600054600160a060020a031681565b6000805481908190600160a060020a038086169116638da5cb5b83604051602001526040518163ffffffff1660e060020a028152600401602060405180830381600087803b1515610f3857600080fd5b6102c65a03f11515610f4957600080fd5b50505060405180519050600160a060020a03161415610f6b576001925061105b565b60008054600160a060020a031690635c7460d690604051602001526040518163ffffffff1660e060020a028152600401602060405180830381600087803b1515610fb457600080fd5b6102c65a03f11515610fc557600080fd5b50505060405180519050600160a060020a031663265209f28560006040516020015260405160e060020a63ffffffff8416028152600160a060020a039091166004820152602401602060405180830381600087803b151561102557600080fd5b6102c65a03f1151561103657600080fd5b50505060405180519050915084600681111561104e57fe5b60020a8281161515935090505b505092915050565b600154600090600160a060020a031663c53fb1a583836040516020015260405160e060020a63ffffffff84160281526004810191909152602401602060405180830381600087803b15156110b657600080fd5b6102c65a03f115156110c757600080fd5b50505060405180519392505050565b600154600160a060020a031615156110ed57600080fd5b60026110f98133610ee8565b151561110457600080fd5b600154600160a060020a031663e60a955d848460405160e060020a63ffffffff8516028152600481019290925215156024820152604401600060405180830381600087803b151561115457600080fd5b6102c65a03f1151561116557600080fd5b50505081156111a057827fbb4a2f3fc0f65f1ee98dc140226f7718191ba94892efdc55613785ccbf00a8e860405160405180910390a26111ce565b827f61f3fbe0c2049de9b0219669983a937b4377c1dced582b6a720a87b49ae3c08b60405160405180910390a25b505050565b600154600090600160a060020a031663f7105c0583836040516020015260405160e060020a63ffffffff84160281526004810191909152602401602060405180830381600087803b15156110b657600080fd5b60015460009081908190600160a060020a031663c6bc1a7685836040516060015260405160e060020a63ffffffff84160281526004810191909152602401606060405180830381600087803b151561127d57600080fd5b6102c65a03f1151561128e57600080fd5b505050604051805190602001805190602001805190509250925092508280156112b45750815b80156112be575080155b156113ba5760018054600160a060020a03169063054dddde90869060405160e060020a63ffffffff8516028152600481019290925215156024820152604401600060405180830381600087803b151561131657600080fd5b6102c65a03f1151561132757600080fd5b505050837f1952717c0461c82af1fee2f55fe9887230a44916d9214bcdf89905bd2c3918a960405160405180910390a2600154600160a060020a03166336016d71854260405160e060020a63ffffffff851602815260048101929092526024820152604401600060405180830381600087803b15156113a557600080fd5b6102c65a03f115156113b657600080fd5b5050505b505050505600a165627a7a72305820f3b55a3d2521c8621f59cd4bf65d6dadc2ccb2c988e7771ecd0dbb85be51a58b0029'
        }
        self.contract = contract

        self.w3 = web3.Web3(web3.HTTPProvider(client_url))

        contract_instance = self.w3.eth.contract(
            abi=contract['abi'],
            address=self.w3.toChecksumAddress(contract['address']),
            bytecode=contract['bytecode'])

        method_name = "getAssetGeneral"
        asset_id = 0
        args = [asset_id]
        assetLocation = getattr(contract_instance.functions, method_name)(*args).call()
        #assetLocation = contract_instance.functions.getAssetLocation(0).call()

        dataDict = {}

        method = self.getContractMethod(method_name)

        for i, value in enumerate(assetLocation):
            key = method['outputs'][i]['name']
            if type(value) == bytes:
                dataDict[key] = value.decode().rstrip('\00')
            else:
                dataDict[key] = value

        print(dataDict)

        return

        nonce = self.w3.eth.getTransactionCount(account=self.w3.toChecksumAddress(wallet_add))
        transaction = {
            'from': self.w3.toChecksumAddress(wallet_add),
            'gas': 400000,
            'gasPrice': self.w3.toWei('0', 'gwei'),
            'nonce': nonce,
        }

        #tx = contract_instance.functions.getAssetLocation(0).buildTransaction(transaction)

        method_name = "saveSmartMeterRead"

        method = self.getContractMethod(method_name)
        oldReading = 13399420
        reading =    14000000
        dataDict = {
            '_assetId': 0,
            '_newMeterRead': reading,
            '_lastSmartMeterReadFileHash': 'ok',
            '_smartMeterDown': False
        }
        args = self.getContractArgs(method, dataDict)

        tx = getattr(contract_instance.functions, method_name)(*args).buildTransaction(transaction)

        private_key = bytearray.fromhex(wallet_pwd)

        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=private_key)

        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        if not tx_hash:
            raise ConnectionError('Transaction was not sent.')

        tx_receipt = None

        for _ in range(self.MAX_RETRIES):
            tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
            if tx_receipt and tx_receipt['blockNumber']:
                self.tx_receipt = tx_receipt
                return
            time.sleep(self.SECONDS_BETWEEN_RETRIES)

        raise ConnectionAbortedError(f'Coudn\'t get transaction receipt after {self.MAX_RETRIES * self.SECONDS_BETWEEN_RETRIES}s')

    def getContractMethod(self, method_name):
        for method in self.contract['abi']:
            try:
                if method['name'] == method_name:
                    return method
            except KeyError:
                continue

        raise BaseException(f'Method {method_name} not found in contract abi.')

    def getContractArgs(self, method, arg_dict):
        args = []
        for i in method['inputs']:
            variable_name = i['name']
            value = arg_dict[variable_name]
            if type(value) == str:
                args.append(value.encode())
            else:
                args.append(value)
        print(args)
        return args


def main():
    e = Example()
    #print(e.tx_receipt)

if __name__=="__main__":
    main()