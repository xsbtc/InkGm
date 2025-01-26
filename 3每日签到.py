import csv
from web3 import Web3
import time

# 连接到以太坊网络
w3 = Web3(Web3.HTTPProvider('https://rpc-gel.inkonchain.com'))

# 检查连接是否成功
if not w3.is_connected():
    print("无法连接到以太坊网络")
    exit()

# 读取 wallets.csv 文件中的钱包信息
wallets = []
with open('wallets.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    wallets = [row[1] for row in reader]  # 获取每行的私钥

# 目标地址和 data 信息
target_address = '0x9F500d075118272B3564ac6Ef2c70a9067Fd2d3F'
data = '0xc0129d43'

# 发送交易的函数
def send_transaction(private_key, wallet_index):
    max_retries = 5  # 最大重试次数
    for attempt in range(max_retries):
        try:
            # 使用私钥生成账户对象
            account = w3.eth.account.from_key(private_key)
            sender_address = account.address

            # 获取当前的 gas 价格
            gas_price = w3.eth.gas_price
            gas_price_gwei = w3.from_wei(gas_price, 'gwei')
            print(f"当前 gas 价格: {gas_price_gwei} gwei")

            # 获取当前 nonce
            nonce = w3.eth.get_transaction_count(sender_address)

            # 构建交易
            transaction = {
                'to': target_address,
                'value': 0,  # 发送 0 ETH
                'gas': 200000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': 57073,  # 链 ID
                'data': data  # 附加 data 信息
            }

            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

            # 发送交易
            txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"钱包 {wallet_index} 已成功发送交易，交易哈希: {txn_hash.hex()}")
            return True  # 交易成功，返回 True

        except Exception as e:
            print(f"钱包 {wallet_index} 发送交易失败: {e}")
            time.sleep(3)  # 等待 3 秒后重试
            if attempt == max_retries - 1:
                print(f"钱包 {wallet_index} 达到最大重试次数，无法发送交易。")
            else:
                print(f"钱包 {wallet_index} 重试中... (尝试 {attempt + 1}/{max_retries})")
    return False  # 如果超过最大重试次数，返回 False

# 遍历钱包私钥并发送交易
for index, private_key in enumerate(wallets, start=1):
    print(f"正在操作第 {index} 个钱包...")
    while not send_transaction(private_key, index):
        print(f"第 {index} 个钱包交易失败，正在重试...")
    time.sleep(5)  # 等待 5 秒，避免发送过快

print("所有钱包交易已处理完毕。")
