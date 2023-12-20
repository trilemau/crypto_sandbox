import numpy as np
import matplotlib.pyplot as plt

def dynamic_dca_contribution(base_contribution, rsi, a=500, b=1):
    # Ensure RSI is between 0 and 100
    rsi = max(0, min(100, rsi))
    
    # Calculate adjusted contribution using the logarithmic scale
    adjusted_contribution = a / np.log(rsi + b)
    
    return adjusted_contribution

# Example usage:
base_contribution = 500  # Base contribution in fiat currency

# Generate RSI values from 1 to 100 (avoiding log(0))
rsi_values = np.arange(1, 101, 1)

# Calculate adjusted contributions for each RSI value
adjusted_contributions = [dynamic_dca_contribution(base_contribution, rsi) for rsi in rsi_values]

# Plot results
plt.figure(figsize=(8, 5))
plt.plot(rsi_values, adjusted_contributions, linestyle='-', color='b')
plt.title('Adjusted Contribution Based on RSI')
plt.xlabel('RSI')
plt.ylabel('Adjusted Contribution (EUR)')
plt.grid(True)
plt.show()
