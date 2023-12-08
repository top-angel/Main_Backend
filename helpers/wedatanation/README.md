# Usage

## Load user facebook data

```bash
python -m helpers.wedatanation.load_user_facebook_data \
--file staging/wedatanation/facebook.zip \
--address 0xdF1dEc52e602020E27B0644Ea0F584b6Eb5CE4eA
```

## Load user amazon data

```bash
python -m helpers.wedatanation.load_user_amazon_data \
--file staging/wedatanation/amazon.zip \
--address 0xdF1dEc52e602020E27B0644Ea0F584b6Eb5CE4eA
```

## Set wallet address for monetization

```bash
python -m helpers.wedatanation.set_web3_wallet_for_monetization \
--address 0x8438979b692196FdB22C4C40ce1896b78425555A \
--network eth_mainnet
```

```bash
python -m helpers.wedatanation.set_web3_wallet_for_monetization \
--address 0x8438979b692196FdB22C4C40ce1896b78425555A \
--network polygon_mainnet
```