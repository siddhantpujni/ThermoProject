import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate, interpolate
import numpy as np

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 14

def load_data(file_path):
    """
    It is crucial that the data file path is specified correctly and in the appropriate format (.xlsx).
    """
    return pd.read_excel(file_path)

def plot_cp_vs_t(data):
    max_value = data['ΔC_p/R'].max()
    max_temp = data.loc[data['ΔC_p/R'].idxmax(), 'T/K']
    
    plt.figure()
    plt.plot(data['T/K'], data['ΔC_p/R'], label='Cu3Au Data')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Δcₚ (R)')
    plt.title('Δcₚ vs Temperature')
    plt.plot(max_temp, max_value, 'ro')
    plt.text(max_temp - 3, max_value, f'Temp = {max_temp}K', color='red', fontsize=12, ha='right')
    plt.legend()
    plt.show()

def plot_cp_over_t_vs_t(data):
    data['C_p/T'] = data['ΔC_p/R'] / data['T/K']
    max_value = data['C_p/T'].max()
    max_temp = data.loc[data['C_p/T'].idxmax(), 'T/K']
    
    plt.figure()
    plt.plot(data['T/K'], data['C_p/T'], label='Cu3Au Data')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Δcₚ/T (R/K)')
    plt.title('Δcₚ/T vs Temperature')
    plt.plot(max_temp, max_value, 'ro')
    plt.text(max_temp - 3, max_value, f'Temp = {max_temp}K', color='red', fontsize=12, ha='right')
    plt.legend()
    plt.show()

def calculate_entropy_change(data):
    if 'C_p/T' not in data.columns:
        data['C_p/T'] = data['ΔC_p/R'] / data['T/K']
    
    T_min = data['T/K'].min()
    T_max = data['T/K'].max()
    cp_min = data['ΔC_p/R'].min()
    delta_T = T_max - T_min  # Positive difference between the bounds of integration

    spline = interpolate.UnivariateSpline(data['T/K'], data['ΔC_p/R'], s=1)
    
    temperatures = data['T/K']
    entropy_changes = []
    
    for T in temperatures:
        if T >= T_min:
            S, _ = integrate.quad(lambda temp: spline(temp) / temp, T_min, T)
            entropy_changes.append(S)
    
    total_entropy_change, err = integrate.quad(lambda temp: spline(temp) / temp, T_min, T_max)
    
    # Calculate the error using the provided equation
    error_estimate = (cp_min / T_min) * delta_T
    
    print(f"Total entropy change from {T_min}K to {T_max}K: ΔS = {total_entropy_change:.4f} R with integration error {err:.4e}")
    print(f"Estimated error in entropy change using the formula: δ(ΔS) = {error_estimate:.4e} R")
    
    plt.figure()
    plt.plot(temperatures, entropy_changes, label='Cumulative Entropy Change')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Cumulative Entropy Change Δs (R)')
    plt.title('Cumulative Entropy Change vs Temperature')
    plt.legend()
    plt.show()

def calculate_entropy_change_rectangular(data):
    """
    Calculate the entropy change using a rectangular approximation method
    based on the sum of discrete sections as shown in guidance notes.
    """
    if 'C_p/T' not in data.columns:
        data['C_p/T'] = data['ΔC_p/R'] / data['T/K']
    
    temperatures = data['T/K']
    cp_over_t = data['C_p/T']
    
    entropy_change_sum = 0
    entropy_changes = [0]  # Starting with zero for the initial cumulative value
    
    for i in range(1, len(temperatures)):
        delta_T = temperatures[i] - temperatures[i - 1]
        Ti = cp_over_t[i - 1]
        entropy_change_sum += Ti * delta_T
        entropy_changes.append(entropy_change_sum)
    
    print(f"Total entropy change using the rectangular approximation: Δs = {entropy_change_sum:.4f} R")
    
    plt.figure()
    plt.plot(temperatures, entropy_changes, label='Cumulative Entropy Change (Rectangular Approx.)')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Cumulative Entropy Change Δs (R)')
    plt.title('Cumulative Entropy Change vs Temperature (Rectangular Approximation)')
    plt.legend()
    plt.show()
    
def plot_splines_with_subplots(data):

    fig, ax = plt.subplots(1, 2, figsize=(14, 10))
    smoothing_factors = [10, 100]
    ax = ax.ravel()  # Flatten the 2D array of axes into a 1D array for easy iteration

    temp_dense = np.linspace(data['T/K'].min(), data['T/K'].max(), 1000)
    
    for i, s in enumerate(smoothing_factors):
        # Create a univariate spline with a specific smoothing factor (s)
        spline = interpolate.UnivariateSpline(data['T/K'], data['ΔC_p/R'], s=s)
        spline_values = spline(temp_dense)

        # Plot the actual data
        ax[i].plot(data['T/K'], data['ΔC_p/R'], 'o', label='Actual Data', markersize=4)
        
        # Plot the spline curve
        ax[i].plot(temp_dense, spline_values, label=f'Spline (s = {s})', color='red')
        
        # Labels and title for each subplot
        ax[i].set_xlabel('Temperature (K)')
        ax[i].set_ylabel('Δcₚ (R)')
        ax[i].set_title(f'Univariate Spline with s = {s}')
        ax[i].legend()

    # Adjust spacing
    plt.tight_layout()
    plt.show()
    


