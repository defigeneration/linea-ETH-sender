import time
import random
from web3 import Web3

# Параметры соединения с Linea Mainnet
RPC_URL = 'https://linea-mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'  # Замените на ваш URL

# Загрузка приватных ключей и адресов получателей
with open('privates.txt', 'r') as f:
    private_keys = [line.strip() for line in f.readlines()]

with open('destination.txt', 'r') as f:
    destinations = [line.strip() for line in f.readlines()]

# Проверка, что количество ключей и адресов совпадает
if len(private_keys) != len(destinations):
    raise ValueError('Количество приватных ключей и адресов получателей должно совпадать')

# Подключение к Linea Mainnet
web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise ConnectionError('Не удалось подключиться к Linea Mainnet')

# Функция для отправки ETH
def send_eth(private_key, to_address, min_balance=0.0055, max_balance=0.0067):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    
    balance = web3.eth.get_balance(account.address)
    gas_price = web3.to_wei('50', 'gwei')
    gas_limit = 21000
    
    # Сумма, которую нужно оставить на кошельке
    leave_amount = web3.to_wei(random.uniform(min_balance, max_balance), 'ether')
    
    # Рассчитываем сумму для отправки
    value = balance - (gas_limit * gas_price) - leave_amount
    
    if value <= 0:
        print(f'Недостаточно средств на кошельке {account.address} для отправки')
        return
    
    transaction = {
        'to': Web3.to_checksum_address(to_address),
        'value': value,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 59144  # Chain ID для Linea Mainnet
    }

    signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'Transaction sent: {tx_hash.hex()}')

# Параметры задержки
delay_min = 60  # Минимальная задержка между транзакциями в секундах
delay_max = 180  # Максимальная задержка между транзакциями в секундах

# Отправка ETH
for private_key, to_address in zip(private_keys, destinations):
    send_eth(private_key, to_address)
    delay = random.randint(delay_min, delay_max)
    print(f'Задержка перед следующей транзакцией: {delay} секунд')
    time.sleep(delay)
