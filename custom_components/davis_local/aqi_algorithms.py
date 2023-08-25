class AQICalculator:
    def calculate(self, pm25, pm10):
        raise NotImplementedError
    
class EPA_USA(AQICalculator):
    EPA_USA_BREAKPOINTS_PM25 = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500)
    ]
    EPA_USA_BREAKPOINTS_PM10 = [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, 504, 301, 400),
        (505, 604, 401, 500)
    ]

    def calculate_aqi(self, concentration, breakpoints):
        # Round the concentration to the nearest 1 decimal place
        concentration = round(concentration, 1)

        for low_concentration, high_concentration, low_index, high_index in breakpoints:
            if low_concentration <= concentration < high_concentration:
                return int((high_index - low_index) / (high_concentration - low_concentration) * (concentration - low_concentration) + low_index)
        return None  # For concentrations not covered by any breakpoint

    def calculate(self, pm25, pm10):
        aqi_pm25 = self.calculate_aqi(pm25, self.EPA_USA_BREAKPOINTS_PM25)
        aqi_pm10 = self.calculate_aqi(pm10, self.EPA_USA_BREAKPOINTS_PM10)

        if aqi_pm25 is None:
            return aqi_pm10
        elif aqi_pm10 is None:
            return aqi_pm25
        else:
            return max(aqi_pm25, aqi_pm10)

# class Canada_Health(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class EU_EEA_Common(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class EU_European(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class UK_COMEAP_Daily(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class Australia_NEPM(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class India_CPCB_National(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class China_MEP(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class Mexico_IMECA(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class Japan_MOE(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class AIRKOREA_MOE_Common(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class Singapore_PSI(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# class Colombia_MADS(AQICalculator):
#     def calculate(self, pm25, pm10):
#         # Implementation here
#         pass

# Map algorithm names to their respective classes
ALGORITHMS = {
    'EPA_USA': {'class': EPA_USA, 'friendly_name': 'United States EPA'},
    # 'CANADA_HEALTH': {'class': Canada_Health, 'friendly_name': 'Canada Health'},
    # 'EU_EEA_COMMON': {'class': EU_EEA_Common, 'friendly_name': 'EU EEA Common'},
    # 'EU_EUROPEAN': {'class': EU_European, 'friendly_name': 'EU European'},
    # 'UK_COMEAP_DAILY': {'class': UK_COMEAP_Daily, 'friendly_name': 'UK COMEAP Daily'},
    # 'AUSTRALIA_NEPM': {'class': Australia_NEPM, 'friendly_name': 'Australia NEPM'},
    # 'INDIA_CPCB_NATIONAL': {'class': India_CPCB_National, 'friendly_name': 'India CPCB National'},
    # 'CHINA_MEP': {'class': China_MEP, 'friendly_name': 'China MEP'},
    # 'MEXICO_IMECA': {'class': Mexico_IMECA, 'friendly_name': 'Mexico IMECA'},
    # 'JAPAN_MOE': {'class': Japan_MOE, 'friendly_name': 'Japan MOE'},
    # 'AIRKOREA_MOE_COMMON': {'class': AIRKOREA_MOE_Common, 'friendly_name': 'AIRKOREA MOE Common'},
    # 'SINGAPORE_PSI': {'class': Singapore_PSI, 'friendly_name': 'Singapore PSI'},
    # 'COLOMBIA_MADS': {'class': Colombia_MADS, 'friendly_name': 'Colombia MADS'},
}