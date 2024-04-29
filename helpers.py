import datetime


def format_timestamp(unix_timestamp):
    """
    converts UNIX timestamp into a new format: e.g 2024-01-01 00:00:00
    """
    timestamp = int(unix_timestamp, 16)
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def convert_wei_to_ether(wei):
    """
    converts transaction.value from wei into ether
    """
    wei = int(wei, 16)
    value = wei / 10**18  # 1 Ether is 10^18 wei
    return f"{value:.18f}"  # return with 18 decimal places
