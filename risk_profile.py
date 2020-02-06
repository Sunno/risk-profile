import datetime


class RiskProfileCalculator(object):
    """
    This class calculates all the risk score
    """
    INELIGIBLE = 'ineligible'
    REGULAR = 'regular'
    ECONOMIC = 'economic'
    RESPONSIBLE = 'responsible'

    def __init__(self, data):
        """
        This assumes data has been validated before
        """
        self._data = data
        self._base_score = sum(data['risk_questions'])
        self.__have_income_vehicle_houses = data['house'] or\
            data['income'] or data['vehicle']
        self.__is_over_60 = data['age'] > 60
        if data['age'] < 30:  # 3
            self._base_score -= 2
        elif 30 <= data['age'] <= 40:
            self._base_score -= 1

        if data['income'] < 200000:  # 4
            self._base_score -= 1

    def __process_score(self, score):
        if score <= 0:
            return self.ECONOMIC
        if 1 <= score <= 2:
            return self.REGULAR
        if score >= 3:
            return self.RESPONSIBLE

    def _calculate_auto(self):
        if not self.__have_income_vehicle_houses:  # 1
            return self.INELIGIBLE
        score = self._base_score

        current_year = datetime.datetime.now().year

        if self._data['vehicle']:
            if self._data['vehicle']['year'] >= current_year - 5:
                score += 1

        return self.__process_score(score)

    def _calculate_disability(self):
        if not self.__have_income_vehicle_houses:  # 1
            return self.INELIGIBLE

        if self.__is_over_60:  # 2
            return self.INELIGIBLE
        score = self._base_score

        if self._data['house']:
            if self._data['house']['ownership_statul'] == 'mortgaged':  # 5
                score += 1

        if self._data['dependents'] > 0:  # 6
            score += 1

        if self._data['marital_status'] == 'married':  # 7
            score -= 1

        return self.__process_score(score)

    def _calculate_home(self):
        if not self.__have_income_vehicle_houses:  # 1
            return self.INELIGIBLE

        score = self._base_score
        if self._data['house']:
            if self._data['house']['ownership_statul'] == 'mortgaged':  # 5
                score += 1
        return self.__process_score(score)

    def _calculate_life(self):
        if self.__is_over_60:  # 2
            return self.INELIGIBLE
        score = self._base_score

        if self._data['dependents'] > 0:  # 6
            score += 1

        if self._data['marital_status'] == 'married':  # 7
            score += 1

        return self.__process_score(score)

    def calculate(self):
        '''
        Returns risk score calculation according to validated data provided
        '''
        return {
            'auto': self._calculate_auto(),
            'disability': self._calculate_disability(),
            'home': self._calculate_home(),
            'life': self._calculate_life()
        }
