class RiskProfileCalculator(object):

    def __init__(self, data):
        self._data = data

    def _calculate_auto(self):
        return 'regular'

    def _calculate_disability(self):
        return 'ineligible'

    def _calculate_home(self):
        return 'economic'

    def _calculate_life(self):
        return 'regular'

    def calculate(self):
        return {
            'auto': self._calculate_auto(),
            'disability': self._calculate_disability(),
            'home': self._calculate_home(),
            'life': self._calculate_life()
        }
