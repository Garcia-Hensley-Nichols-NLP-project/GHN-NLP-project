"""
A module for obtaining repo readme and language data from the github API.

Before using this module, read through it, and follow the instructions marked
TODO.

After doing so, run it like this:

    python acquire.py

To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token: https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    "https://github.com/bitcoin/bitcoin",
    "https://github.com/bitcoinbook/bitcoinbook",
    "https://github.com/bitcoin/bips",
    "https://github.com/bitcoinjs/bitcoinjs-lib",
    "https://github.com/spesmilo/electrum",
    "https://github.com/bitcoin-wallet/bitcoin-wallet",
    "https://github.com/etotheipi/BitcoinArmory",
    "https://github.com/bitcoin-dot-org/Bitcoin.org",
    "https://github.com/jgarzik/cpuminer",
    "https://github.com/BitcoinExchangeFH/BitcoinExchangeFH",
    "https://github.com/yenom/BitcoinKit",
    "https://github.com/maxme/bitcoin-arbitrage",
    "https://github.com/BitcoinUnlimited/BitcoinUnlimited",
    "https://github.com/Bitcoin-ABC/bitcoin-abc",
    "https://github.com/bisq-network/bisq",
    "https://github.com/mobnetic/BitcoinChecker",
    "https://github.com/bitcoin-abe/bitcoin-abe",
    "https://github.com/petertodd/python-bitcoinlib",
    "https://github.com/sipa/bitcoin-seeder",
    "https://github.com/imfly/bitcoin-on-nodejs",
    "https://github.com/PiSimo/BitcoinForecast",
    "https://github.com/trottier/original-bitcoin",
    "https://github.com/rust-bitcoin/rust-bitcoin",
    "https://github.com/Bit-Wasp/bitcoin-php",
    "https://github.com/btcpayserver/btcpayserver",
    "https://github.com/bitcoin-core/bitcoincore.org",
    "https://github.com/lian/bitcoin-ruby",
    "https://github.com/GammaGao/bitcoinwhitepaper",
    "https://github.com/tianmingyun/MasterBitcoin2CN",
    "https://github.com/kylemanna/docker-bitcoind",
    "https://github.com/pointbiz/bitaddress.org",
    "https://github.com/BTCPrivate/BitcoinPrivate-legacy",
    "https://github.com/jgarzik/python-bitcoinrpc",
    "https://github.com/pooler/cpuminer",
    "https://github.com/progranism/Open-Source-FPGA-Bitcoin-Miner",
    "https://github.com/HelloZeroNet/ZeroNet",
    "https://github.com/cryptean/bitcoinlib",
    "https://github.com/xiaolai/bitcoin-whitepaper-chinese-translation",
    "https://github.com/oleganza/CoreBitcoin",
    "https://github.com/bitcoin-sv/bitcoin-sv",
    "https://github.com/m0mchil/poclbm",
    "https://github.com/jgarzik/pyminer",
    "https://github.com/bitcoinxt/bitcoinxt",
    "https://github.com/paritytech/parity-bitcoin",
    "https://github.com/bitpay/insight",
    "https://github.com/stratisproject/StratisBitcoinFullNode",
    "https://github.com/Multibit-Legacy/multibit",
    "https://github.com/janoside/btc-rpc-explorer",
    "https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line",
    "https://github.com/JulyIghor/QtBitcoinTrader",
    "https://github.com/MetacoSA/NBitcoin",
    "https://github.com/p2pool/p2pool",
    "https://github.com/bitcoincashorg/bitcoincash.org",
    "https://github.com/igorbarinov/awesome-bitcoin",
    "https://github.com/buttercoin/buttercoin",
    "https://github.com/1200wd/bitcoinlib",
    "https://github.com/BitcoinPHP/BitcoinECDSA.php",
    "https://github.com/bitpay/bitcore",
    "https://github.com/lefnire/tforce_btc_trader",
    "https://github.com/bitpay/insight-api",
    "https://github.com/bitpay/bitcore-lib",
    "https://github.com/100trillionUSD/bitcoin",
    "https://github.com/jashmenn/bitcoin-reading-list",
    "https://github.com/bitpay/bitcoind-rpc",
    "https://github.com/zquestz/bitcoincash",
    "https://github.com/davout/bitcoin-central",
    "https://github.com/btcsuite/btcd",
    "https://github.com/ofek/bit",
    "https://github.com/bitpay/bitcore-wallet-service",
    "https://github.com/breadwallet/breadwallet-core",
    "https://github.com/ruimarinho/bitcoin-core",
    "https://github.com/dooglus/intersango",
    "https://github.com/Diablo-D3/DiabloMiner",
    "https://github.com/freewil/bitcoin-testnet-box",
    "https://github.com/mycelium-com/wallet-android",
    "https://github.com/benjyz/bitcoinArchive",
    "https://github.com/Blockstream/esplora",
    "https://github.com/butor/blackbird",
    "https://github.com/Bitlits/Bitcoin-Games",
    "https://github.com/znort987/blockparser",
    "https://github.com/kingrock/BitcoinExchange",
    "https://github.com/aceat64/EasyBitcoin-PHP",
    "https://github.com/eveybcd/BitcoinDiamond",
    "https://github.com/siminchen/bitcoinIDE",
    "https://github.com/ccxt/ccxt",
    "https://github.com/thallium205/BitcoinVisualizer",
    "https://github.com/brandonrobertz/BitcoinTradingAlgorithmToolkit",
    "https://github.com/libbitcoin/libbitcoin-explorer",
    "https://github.com/phishman3579/Bitcoin",
    "https://github.com/LedgerHQ/app-bitcoin",
    "https://github.com/SegwitB2X/bitcoin2x",
    "https://github.com/llSourcell/bitcoin_prediction",
    "https://github.com/alecalve/python-bitcoin-blockchain-parser",
    "https://github.com/fkysly/bitcoin0.1.0",
    "https://github.com/haskoin/haskoin-core",
    "https://github.com/philipperemy/deep-learning-bitcoin",
    "https://github.com/libbitcoin/libbitcoin-system",
    "https://github.com/ruimarinho/docker-bitcoin-core",
    "https://github.com/blinktrade/bitex",
    "https://github.com/bitcoin-core/HWI"
]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)