import sys
sys.path.append('..')

import numpy as np
import pandas as pd

from pimpa.trade_models.portfolio import Portfolio
from pimpa.trade_models.interest_rate_swap import InterestRateSwap
from pimpa.trade_models.equity_european_option import EquityEuropeanOption
from pimpa.pricing_models.interest_rate_swap_pricer import InterestRateSwapPricer
from pimpa.pricing_models.equity_european_option_pricer import EquityEuropeanOptionPricer
from pimpa.market_data_objects.market_data_builder import MarketDataBuilder
from pimpa.utils.calendar_utils import generate_simulation_dates_schedule
from pimpa.utils.calendar_utils import transform_dates_to_time_differences
from data.configuration.global_parameters import global_parameters, calibration_parameters

trade_id = 3234
risk_factors = pd.read_csv(global_parameters['prototype_data_paths']['RFs_attributes'] + global_parameters['prototype_data_files']['RFs_attributes']['all_RFs_mapping'])
trade = InterestRateSwap(trade_id)
trade.load(global_parameters, risk_factors)
print('-----------------------------')
print(trade)
print('-----------------------------')

pricer = InterestRateSwapPricer('IRS_Pricer')
risk_factor_objects = MarketDataBuilder().get_risk_factors(trade.trade_underlyings, global_parameters)

print(f"rf_obj: {risk_factor_objects}")

pricer_dependencies = pricer.get_market_dependencies(trade.trade_underlyings, risk_factor_objects,calibration_parameters)
print(f"PrDe:{pricer_dependencies}")

market_data = MarketDataBuilder().load_market_data(pricer_dependencies, global_parameters)
# print('-----------------------------')
# print(f"MkDt:{market_data}")
# print('-----------------------------')
pricer.calibrate(market_data, calibration_parameters)
print(pricer)
print('-----------------------------')

starting_date = '2020-01-01'
final_date = '2040-01-01'
valuation_frequency = 'monthly'
nr_paths = 1000
global_parameters['n_paths'] = nr_paths
valuation_dates = generate_simulation_dates_schedule(starting_date, final_date, valuation_frequency, global_parameters)
scenarios = {'EUR_ZERO_YIELD_CURVE': np.random.normal(size=(nr_paths, len(valuation_dates)))}
trade_mtms = pricer.price_single_trade(trade, valuation_dates, scenarios, market_data, global_parameters)