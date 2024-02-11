# tri-pool-lp-crvusd-oracle
A proposed price feed for tri-curve lp/crvUSD for isolated lending markets.

## Proposed Oracles Calculation:

Use Curve pool `lp_price` (current price of the LP token w.r.t coin at the 0th index) in combinaison with ChainLink procefeeds:

| Collateral     | Loan Asset                               | Pool Index 0 | Proposed Oracle                               |
|----------------|--------|-----|--------------------------------------------|
| [TricryptoUSDT](https://etherscan.io/address/0xf5f5b97624542d72a9e06f04804bf81baa15e2b4)  | crvUSD | USDT    | lp_price * [CL USDT/USD](https://data.chain.link/feeds/ethereum/mainnet/usdt-usd) * [CL CRVUSD/USD ](https://data.chain.link/feeds/ethereum/mainnet/crvusd-usd)                      |
| [TricryptoUSDC](https://etherscan.io/address/0x7f86bf177dd4f3494b841a37e810a34dd56c829b)  | crvUSD | USDC    | lp_price * [CL USDC/USD](https://data.chain.link/feeds/ethereum/mainnet/usdc-usd) * [CL CRVUSD/USD](https://data.chain.link/feeds/ethereum/mainnet/crvusd-usd)                       |
| [TricryptoLLAMA](https://etherscan.io/address/0x2889302a794da87fbf1d6db415c1492194663d13) | crvUSD | crvUSD  | lp_price                                      |
| [TryLSD](https://etherscan.io/address/0x2570f1bd5d2735314fc102eb12fc1afe9e6e7193)         | crvUSD | wstETH  | lp_price * [wstETH/stETH rate](https://etherscan.io/token/0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0#readContract#F10) * [CL stETH/USD](https://data.chain.link/feeds/ethereum/mainnet/steth-usd) * [CL CRVUSD/USD](https://data.chain.link/feeds/ethereum/mainnet/crvusd-usd)|
| [TriCRV](https://etherscan.io/address/0x4ebdf703948ddcea3b11f675b4d1fba9d2414a14)         | crvUSD | crvUSD  | lp_price  |

## Methodology for comparative analysis

To assess oracle soundness, we queried historical data for the last 3 months:

``` python
start_block = 18325000 # Oct-11-2023
end_block = 19205000 # Feb-11-2024
slice_count = 4_000
```

The proposed Oracle price is compared to the following:
### `sum(balance[i] * asset_price[i]) / total_supply * crvusd/usd`
_Asset price calculated from ChainLink feeds, with BTC/USD used for WBTC and TBTC_

## Results

### Variance Graphs

### MAX, MEAN, MEDIAN, PERCENTILE

