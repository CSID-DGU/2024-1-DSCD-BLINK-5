import numpy as np
import logging


class StockTradingEnv:
    def __init__(self, data, initial_investment, args, sector_indices):
        self.stock_price_history = data
        self.n_stock, self.n_step, self.n_feature = self.stock_price_history.shape
        self.window_size = args.WINDOW_SIZE
        self.max_random_amount_stock = args.MAX_RANDOM_AMOUNT_STOCK
        self.initial_investment = initial_investment
        self.sector_indices = sector_indices
        self.current_step = None
        self.stock_owned = None
        self.cash_in_hand = None

        self.state_dim = (
            self.n_stock * self.window_size * self.n_feature + 1 + self.n_stock
        )
        
        self.reset()

    def reset(self):
        self.current_step = 0
        self.stock_owned = np.zeros(self.n_stock)
        self.cash_in_hand = self.initial_investment
        self.stock_price = self.stock_price_history[
            :, self.current_step : self.current_step + self.window_size, 3
        ]
        self.stock_state = self.stock_price_history[
            :, self.current_step : self.current_step + self.window_size, :
        ]
        return self._get_obs()

    def step(self, action, amount):
        prev_total_value = self._get_total_value()

        self.current_step += 1

        if self.current_step + self.window_size > self.n_step:
            done = True
            self.stock_price = self.stock_price_history[
                :, -self.window_size :, 3
            ]  # Handle edge case
            self.stock_state = self.stock_price_history[:, -self.window_size :, :]
        else:
            self.stock_price = self.stock_price_history[
                :, self.current_step : self.current_step + self.window_size, 3
            ]
            self.stock_state = self.stock_price_history[
                :, self.current_step : self.current_step + self.window_size, :
            ]
            done = False

        self._trade(action, amount)
        current_total_value = self._get_total_value()
        
        reward = current_total_value - prev_total_value
        info = {"current_total_value": current_total_value}
        return self._get_obs(), reward, done, info
    
    def sample(self):
        action = np.random.choice([0, 1, 2], self.n_stock)
        amount = np.random.choice(100, 500)
        return action, amount

    def _get_obs(self):
        obs = dict()
        obs["state"] = self.stock_state
        obs["owned"] = self.stock_owned
        obs["cash"] = self.cash_in_hand
        return obs

    def _get_total_value(self):
        return self.stock_owned.dot(self.stock_price[:, -1]) + self.cash_in_hand

    def _trade(self, action, amount):
        if self.cash_in_hand <= 0:
            pass
        else:
            for i, (action_type, num_stock) in enumerate(zip(action, amount)):
                if action_type == 0:  # 매도
                    if self.stock_owned[i] >= num_stock and num_stock > 0:
                        self.stock_owned[i] -= num_stock
                        self.cash_in_hand += self.stock_price[i, -1] * num_stock
            for i, (action_type, num_stock) in enumerate(zip(action, amount)):
                if action_type == 2:  # 매수
                    total_cost = self.stock_price[i, -1] * num_stock
                    if (
                        self.cash_in_hand >= total_cost
                        and num_stock > 0
                        and total_cost > 0
                    ):
                        self.stock_owned[i] += num_stock
                        self.cash_in_hand -= total_cost
                        