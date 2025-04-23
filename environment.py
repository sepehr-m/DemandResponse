class Environment:
    def __init__(
        self,
        hourly_prices,
        system_load_profile,
        house_profiles,
        num_houses,
        price_thresholds,
    ):
        self.hourly_prices = hourly_prices
        self.system_load_profile = system_load_profile
        self.house_profiles = hourly_prices
        self.num_houses = num_houses
        self.price_thresholds = price_thresholds

        peak_load = self.system_load["total"].max()
        self.grid_capacity = 1.2 * peak_load * num_houses

        self.incentive_rates = {
            "low": 0.01,  # $0.01 per kWh shifted during low price periods
            "medium": 0.03,  # $0.03 per kWh shifted during medium price periods
            "high": 0.05,  # $0.05 per kWh shifted during high price periods
            "very_high": 0.1,  # $0.10 per kWh shifted during very high price periods
        }

        self.reset()

    def reset(self):
        self.current_hour = 0
        self.total_daily_load = 0
        self.total_shifted_load = 0
        self.customer_satisfaction = 1.0 # Start with full satisfaction
        self.total_cost = 0
        self.total_reward = 0
        self.hour_history = []

        # Add small random variations to laod profile for stochasticity
        self.load_variation_factor = np.random.uniform(0.95, 1.05)

        return self._get_state()

    def _get_state(self):
        current_price = self.hourly_prices[self.hourly_prices['hour'] == self.current_hour].iloc[0]
        total_load = load

