import data_analysis_functions as daf

def main():
    file_path = r"C:/Users/pujni/OneDrive/Desktop/University/Year 3/Thermodynamics/Semester 1/Thermo Project/Cu3AuData.xlsx"
    data = daf.load_data(file_path)
    
    choice = input(
        "1. Plot Δcₚ vs T\n"
        "2. Plot Δcₚ/T vs T\n"
        "3. Numerically integrate Δcₚ/T using scipy.quad\n"
        "4. Numerically integrate Δcₚ/T using rectangular approximation\n"
        "5. Overplot data to check which Spline is best: "
    )
    
    if choice == '1':
        daf.plot_cp_vs_t(data)
    elif choice == '2':
        daf.plot_cp_over_t_vs_t(data)
    elif choice == '3':
        daf.calculate_entropy_change(data)
    elif choice == '4':
        daf.calculate_entropy_change_rectangular(data)
    elif choice == '5':
        daf.plot_splines_with_subplots(data)
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5")

if __name__ == "__main__":
    main()