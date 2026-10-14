days_per_yr = 365.2425
#days_per_week = 7
#weeks_per_yr = days_per_yr / days_per_week
days_per_mo = days_per_yr / 12

def f(num: float) -> str:
	return '${:,.2f}'.format(round(num,2))

def daily_gas_expenses(mi: float, mpg: float, ppg: float) -> float:
	return mi / mpg * ppg

def monthly_gas_expenses(mi: float, mpg: float, ppg: float) -> float:
	return days_per_mo * mi / mpg * ppg


print(f(monthly_gas_expenses(30, 14.27, 4)))
