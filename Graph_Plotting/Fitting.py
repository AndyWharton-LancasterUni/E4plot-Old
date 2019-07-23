from linfit.linfit import linfit
import numpy as np
import math
import copy
from scipy import stats


# Fit two linear lines to the data and find their intersection
def cv_fits(data):

    # Find the average error for all the data points
    mean_error = sum(data.inverse_c_squared_error)/len(data.inverse_c_squared_error)

    # Make copies of the data
    errors = copy.deepcopy(data.inverse_c_squared_error)
    voltages = copy.deepcopy(data.v_mean)
    capacitances = copy.deepcopy(data.inverse_c_squared)

    # Find points with unrealistically small or large errors
    remove_indices = []
    for i in range(len(errors)):
        if errors[i] > 10 * mean_error or errors[i] < 0.1 * mean_error:
            remove_indices.append(i)

    # Fill lists with the values to be removed
    bad_v = []
    bad_c = []
    bad_c_error = []
    for i in remove_indices:
        bad_v.append(voltages[i])
        bad_c.append(capacitances[i])
        bad_c_error.append(errors[i])

    # Remove points
    for i in bad_v:
        voltages.remove(i)

    for i in bad_c:
        capacitances.remove(i)

    for i in bad_c_error:
        errors.remove(i)

    combined_reduced_chi_squared = []

    # Find where to divide the data to produce the two best linear fits
    for i in range(3, len(voltages) - 3):
        v_1 = voltages[:i]
        c_1 = capacitances[:i]
        c_1_error = errors[:i]
        v_2 = voltages[i:]
        c_2 = capacitances[i:]
        c_2_error = errors[i:]

        fit1, cvm1, info1 = linfit(v_1, c_1, sigmay=c_1_error, relsigma=False, return_all=True)
        fit2, cvm2, info2 = linfit(v_2, c_2, sigmay=c_2_error, relsigma=False, return_all=True)

        red_chi_sqr1 = float(info1.rchisq)
        red_chi_sqr2 = float(info2.rchisq)

        combined_reduced_chi_squared.append(red_chi_sqr1 + red_chi_sqr2)

    r = np.argmin(combined_reduced_chi_squared) + 3

    # Create the lists for the best lines
    v_1 = voltages[:r]
    c_1 = capacitances[:r]
    c_1_error = errors[:r]
    c_2_error = errors[r:]
    v_2 = voltages[r:]
    c_2 = capacitances[r:]

    fit1, cvm1, info1 = linfit(v_1, c_1, sigmay=c_1_error, relsigma=False, return_all=True)
    fit2, cvm2, info2 = linfit(v_2, c_2, sigmay=c_2_error, relsigma=False, return_all=True)

    c_1_new = []
    c_2_new = []
    for l in range(len(data.v_mean)):
        c_1_new.append(fit1[1] + fit1[0] * data.v_mean[l])
    for l in range(len(data.v_mean)):
        c_2_new.append(fit2[1] + fit2[0] * data.v_mean[l])

    # Find where they intersect, the depletion voltage, and the error
    intersection = (fit2[1] - fit1[1]) / (fit1[0] - fit2[0])
    intersection_error = round_sig(abs(intersection * math.sqrt(
        ((math.sqrt(info1.fiterr[1] ** 2 + info2.fiterr[1] ** 2) / (fit2[1] - fit1[1])) ** 2) + (
                    (math.sqrt(info1.fiterr[0] ** 2 + info2.fiterr[0] ** 2)) / (fit1[0] - fit2[0])) ** 2)), 1)
    intersection = round_sig(intersection, 2)

    output = [c_1_new, c_2_new, intersection, intersection_error]

    return output


# Find if the difference between the largest current and the smallest current is greater than 25%
def it_fits(data):
    """
    # A very rough method of trying to ignore anomalous points in the It data
    mean_current = sum(data.i_mean) / len(data.i_mean)
    mean_error = stats.sem(data.i_mean)
    main_data_i = []
    main_data_t = []
    main_data_ierror = []
    bad_data_i = []
    bad_data_t = []
    bad_data_ierror = []
    for i in range(len(data.i_mean)):
        if mean_current + (100 * mean_error) > data.i_mean[i] > mean_current - (100 * mean_error):
            main_data_t.append(data.time[i])
            main_data_i.append(data.i_mean[i])
            main_data_ierror.append(data.i_error[i])
        else:
            bad_data_t.append(data.time[i])
            bad_data_i.append(data.i_mean[i])
            bad_data_ierror.append(data.i_error[i])

    minimum_y = min(main_data_i)
    maximum_y = max(main_data_i)
    """
    # Largest current
    minimum_y = min(data.i_mean)
    # Smallest allowed current
    max_allowed_y = minimum_y * 0.75
    # Smallest current
    maximum_y = max(data.i_mean)

    if maximum_y > max_allowed_y:
        pass_or_fail = 'Fail'
    else:
        pass_or_fail = 'Pass'

    return minimum_y, maximum_y, max_allowed_y, pass_or_fail


# Find when breakdown occurs - when increases by 20% or more between two consecutive measurements
def breakdown_voltage(data):
    bd_voltage = 0
    for x in range(1, len(data.i_mean) - 1):
        if abs(data.i_mean[x + 1]) >= abs(data.i_mean[x] * 1.2):
            bd_voltage = data.v_mean[x]
            break
        else:
            continue
    if bd_voltage != 0:
        return [bd_voltage, f'Breakdown occurs at {bd_voltage}V']
    else:
        return [None, 'Breakdown has not been reached']


# Rounding
def round_sig(x, sig=2):
    return round(x, sig-int(math.floor(math.log10(abs(x))))-1)