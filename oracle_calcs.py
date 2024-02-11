import pandas as pd
from y import Contract
import asyncio
from brownie import web3
from dank_mids.helpers import setup_dank_w3_from_sync

# Curve Pools
TRI_USDT = Contract('0xf5f5B97624542D72A9E06f04804Bf81baA15e2B4')
TRI_USDC = Contract('0x7F86Bf177Dd4F3494b841a37e810A34dD56c829B')
TRI_LLAMA = Contract('0x2889302a794dA87fBF1D6Db415C1492194663D13')
TRI_LSD = Contract('0x2570f1bD5D2735314FC102eb12Fc1aFe9e6E7193')
TRI_CRV = Contract('0x4ebdf703948ddcea3b11f675b4d1fba9d2414a14')

# ChainLink Feeds
CL_USDT_USD = Contract('0x3E7d1eAB13ad0104d2750B8863b489D65364e32D')
CL_USDC_USD = Contract('0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6')
CL_CRVUSD_USD = Contract('0xEEf0C605546958c1f899b6fB336C20671f9cD49F')
CL_BTC_USD = Contract('0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c')
CL_ETH_USD = Contract('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419')
CL_RETH_ETH = Contract('0x536218f9E9Eb48863970252233c8F271f554C2d0')
CL_STETH_USD = Contract('0xCfE54B5cD566aB89272946F602D76Ea879CAb4a8')
CL_CRV_USD = Contract('0xCd627aA160A6fA45Eb793D19Ef54f5062F20f33f')

# for sfrxETH
SFRXETH_FEED = Contract('0xB9af7723CfBd4469A7E8aa60B93428D648Bda99d')

# Lido Contract
LIDO_WSTETH_STETH = Contract('0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0')

start_block = 18325000 # Oct-11-2023
end_block = 19205000 # Feb-11-2024 
slice_count = 4_000
step_size = (end_block - start_block) // slice_count

dank_w3 = setup_dank_w3_from_sync(web3)

def main():
    asyncio.get_event_loop().run_until_complete(_main())

async def _main():
    data = await asyncio.gather(*[get_data_for_block(i) for i in range(start_block, end_block, step_size)])
    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=['Block', 'Timestamp', 'tri_usdt_oracle_new', 'tri_usdt_ref', 'tri_usdc_oracle_new', 'tri_usdc_ref', 'tri_llama_oracle_new', 'tri_llama_ref', 'tri_lsd_oracle_new', 'tri_lsd_ref', 'tri_crv_oracle_new', 'tri_crv_ref'])
    df.to_csv('dataset.csv', index=False) 

async def get_data_for_block(i):
    tri_usdt_lp_price, tri_usdt_0, tri_usdt_1, tri_usdt_2, tri_usdt_supply, tri_usdc_lp_price, tri_usdc_0, tri_usdc_1, tri_usdc_2, tri_usdc_supply, tri_llama_lp_price, tri_llama_0, tri_llama_1, tri_llama_2, tri_llama_supply, tri_lsd_lp_price, tri_lsd_0, tri_lsd_1, tri_lsd_2, tri_lsd_supply, tri_crv_price, tri_crv_0, tri_crv_1, tri_crv_2, tri_crv_supply, cl_usdt_usd, cl_usdc_usd, cl_crvusd_usd, cl_btc_usd, cl_eth_usd, cl_reth_eth, cl_steth_usd, cl_crv_usd, sfrxeth_feed, lido_wsteth_steth = await asyncio.gather(
        
        # TRI_USDT
        TRI_USDT.lp_price.coroutine(block_identifier=i), 
        TRI_USDT.balances.coroutine(0, block_identifier=i),
        TRI_USDT.balances.coroutine(1, block_identifier=i),
        TRI_USDT.balances.coroutine(2, block_identifier=i),
        TRI_USDT.totalSupply.coroutine(block_identifier=i),

        # TRI_USDC
        TRI_USDC.lp_price.coroutine(block_identifier=i),
        TRI_USDC.balances.coroutine(0, block_identifier=i),
        TRI_USDC.balances.coroutine(1, block_identifier=i),
        TRI_USDC.balances.coroutine(2, block_identifier=i),
        TRI_USDC.totalSupply.coroutine(block_identifier=i),

        # TRI_LLAMA
        TRI_LLAMA.lp_price.coroutine(block_identifier=i),
        TRI_LLAMA.balances.coroutine(0, block_identifier=i),
        TRI_LLAMA.balances.coroutine(1, block_identifier=i),
        TRI_LLAMA.balances.coroutine(2, block_identifier=i),
        TRI_LLAMA.totalSupply.coroutine(block_identifier=i),

        # TRI_LSD
        TRI_LSD.lp_price.coroutine(block_identifier=i),
        TRI_LSD.balances.coroutine(0, block_identifier=i),
        TRI_LSD.balances.coroutine(1, block_identifier=i),
        TRI_LSD.balances.coroutine(2, block_identifier=i),
        TRI_LSD.totalSupply.coroutine(block_identifier=i),

        # TRI_CRV
        TRI_CRV.lp_price.coroutine(block_identifier=i),
        TRI_CRV.balances.coroutine(0, block_identifier=i),
        TRI_CRV.balances.coroutine(1, block_identifier=i),
        TRI_CRV.balances.coroutine(2, block_identifier=i),
        TRI_CRV.totalSupply.coroutine(block_identifier=i),

        # PRICE FEEDS
        CL_USDT_USD.latestAnswer.coroutine(block_identifier=i),
        CL_USDC_USD.latestAnswer.coroutine(block_identifier=i),
        CL_CRVUSD_USD.latestAnswer.coroutine(block_identifier=i),
        CL_BTC_USD.latestAnswer.coroutine(block_identifier=i), # @notice: using BTC/USD for WBTC and TBTC feeds
        CL_ETH_USD.latestAnswer.coroutine(block_identifier=i),
        CL_RETH_ETH.latestAnswer.coroutine(block_identifier=i),
        CL_STETH_USD.latestAnswer.coroutine(block_identifier=i),
        CL_CRV_USD.latestAnswer.coroutine(block_identifier=i),
        SFRXETH_FEED.latestRoundData.coroutine(block_identifier=i),
        LIDO_WSTETH_STETH.stEthPerToken.coroutine(block_identifier=i),
    )

    # TRI_USDT
    tri_usdt_oracle_new = tri_usdt_lp_price * cl_usdt_usd / cl_crvusd_usd / 1e18
    tri_usdt_ref = (
        (tri_usdt_0 * cl_usdt_usd) * 1e4 +  # USDT, Scaling from 1e14 to 1e18
        (tri_usdt_1 * cl_btc_usd) * 1e2 +   # WBTC, Scaling from 1e16 to 1e18
        (tri_usdt_2 * cl_eth_usd) / 1e8     # ETH, Scaling down from 1e26 to 1e18
    ) * 1e8 / (tri_usdt_supply * cl_crvusd_usd)

    # TRI_USDC
    tri_usdc_oracle_new = tri_usdc_lp_price * cl_usdc_usd / cl_crvusd_usd / 1e18
    tri_usdc_ref = (
        (tri_usdc_0 * cl_usdc_usd) * 1e4 +  # USDC, Scaling from 1e14 to 1e18
        (tri_usdc_1 * cl_btc_usd) * 1e2 +   # WBTC, Scaling from 1e16 to 1e18
        (tri_usdc_2 * cl_eth_usd) / 1e8     # ETH, Scaling down from 1e26 to 1e18
    ) * 1e8 / (tri_usdc_supply * cl_crvusd_usd)

    # TRI_LLAMA
    tri_llama_oracle_new = tri_llama_lp_price / 1e18
    tri_llama_ref = (
        (tri_llama_0 * cl_usdc_usd) +  # CRVUSD
        (tri_llama_1 * cl_btc_usd) +   # TBTC
        (tri_llama_2 * lido_wsteth_steth * cl_steth_usd) / 1e18     # WSTETH
    ) / (tri_llama_supply * cl_crvusd_usd)

    # TRI_LSD
    tri_lsd_oracle_new = tri_lsd_lp_price * lido_wsteth_steth * cl_steth_usd / (cl_crvusd_usd * 1e36)
    tri_lsd_ref = (
        (tri_lsd_0 * lido_wsteth_steth * cl_steth_usd) / 1e18 +  # wstETH
        (tri_lsd_1 * cl_reth_eth * cl_eth_usd) / 1e18 +          # rETH
        (tri_lsd_2 * sfrxeth_feed[1] * cl_eth_usd) / 1e18        # sfrxETH
    ) / (tri_lsd_supply * cl_crvusd_usd)

    # TRI_CRV
    tri_crv_oracle_new = tri_crv_price / 1e18
    tri_crv_ref = (
        (tri_crv_0 * cl_usdc_usd) +  # CRVUSD
        (tri_crv_1 * cl_eth_usd) +   # ETH
        (tri_crv_2 * cl_crv_usd)     # CRV
    ) / (tri_crv_supply * cl_crvusd_usd)
    block = await dank_w3.eth.get_block(i)
    return [i, block.timestamp, tri_usdt_oracle_new, tri_usdt_ref, tri_usdc_oracle_new, tri_usdc_ref, tri_llama_oracle_new, tri_llama_ref, tri_lsd_oracle_new, tri_lsd_ref, tri_crv_oracle_new, tri_crv_ref]