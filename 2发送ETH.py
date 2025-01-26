import csv
from web3 import Web3
import time

# 读取私钥
with open('key.txt', 'r') as f:
    private_key = f.readline().strip()  # 读取私钥并去除换行符

# 连接到以太坊网络
w3 = Web3(Web3.HTTPProvider('https://rpc-gel.inkonchain.com'))

# 检查连接是否成功
if not w3.is_connected():
    print("无法连接到以太坊网络")
    exit()

# 获取发送者地址
account = w3.eth.account.from_key(private_key)
sender_address = account.address

# 读取钱包地址
with open('wallets.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    wallets = [row[0] for row in reader]  # 读取地址


# 发送ETH的函数
def send_eth(to_address, amount):
    max_retries = 5  # 最大重试次数
    for attempt in range(max_retries):
        try:
            # 获取当前的 gas 价格（以 wei 为单位）
            gas_price = w3.eth.gas_price  # 获取当前 gas 价格
            gas_price_gwei = w3.from_wei(gas_price, 'gwei')  # 转换为 gwei
            print(f"当前 gas 价格: {gas_price_gwei} gwei")

            # 获取当前 nonce
            nonce = w3.eth.get_transaction_count(sender_address)

            # 构建交易
            transaction = {
                'to': to_address,
                'value': w3.to_wei(amount, 'ether'),  # 转换为 wei
                'gas': 2000000,
                'gasPrice': gas_price,  # 使用当前 gas 价格
                'nonce': nonce,
                'chainId': 57073  # 链ID
            }

            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

            # 发送交易
            txn_hash = w3.eth.send_raw_transaction(signed_txn['raw_transaction'])  # 使用正确的属性
            print(f"已成功发送 {amount} ETH 到 {to_address}, 交易哈希: {txn_hash.hex()}")
            return txn_hash  # 发送成功，返回交易哈希

        except Exception as e:
            print(f"发送到 {to_address} 失败: {e}")
            time.sleep(3)  # 等待3秒后重试
            if attempt == max_retries - 1:
                print(f"达到最大重试次数，无法发送到 {to_address}。")
            else:
                print(f"重试中... (尝试 {attempt + 1}/{max_retries})")


# 循环发送ETH到每个地址
amount_to_send = 0.00001  # 每个地址发送的ETH数量

for address in wallets:
    send_eth(address, amount_to_send)
    time.sleep(5)  # 等待5秒，避免发送过快

print("所有交易已处理完毕。")
