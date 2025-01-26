import csv
from eth_account import Account

# 创建一个空列表来存储地址和私钥
wallets = []

# 生成100个钱包地址和私钥
for _ in range(100):
    # 创建一个新的账户
    account = Account.create()
    # 获取地址和私钥
    address = account.address
    private_key = account.key.hex()  # 将私钥转换为十六进制字符串
    # 将地址和私钥添加到列表中
    wallets.append([address, private_key])

# 将地址和私钥保存到CSV文件
with open('wallets.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # 写入CSV文件的标题行
    writer.writerow(['Address', 'Private Key'])
    # 写入每个钱包的地址和私钥
    writer.writerows(wallets)

print("已生成100个钱包地址和私钥，并保存到 wallets.csv 文件中。")
