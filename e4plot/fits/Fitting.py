from linfit.linfit import linfit
import numpy as np
import math
import copy


def cv_fits(data):
    print('Fitting CV')

    mean_error = sum(data.inverse_c_squared_error)/len(data.inverse_c_squared_error)

    """
    for i in data.inverse_c_squared_error:
        if i > 10*mean_error or i < 0.1*mean_error:
            #del(data.v_mean[i])
            #del(data.inverse_c_squared[i])
            del(data.v_mean[data.inverse_c_squared_error.index(i)])
            del(data.inverse_c_squared[data.inverse_c_squared_error.index(i)])
            print(data.inverse_c_squared_error.index(i))
            data.inverse_c_squared_error.remove(i)
            print(i)

            print(type(i))
    """

    errors = copy.deepcopy(data.inverse_c_squared_error)
    voltages = copy.deepcopy(data.v_mean)
    capacitances = copy.deepcopy(data.inverse_c_squared)

    remove_indices = []
    for i in range(len(errors)):
        if errors[i] > 10 * mean_error or errors[i] < 0.1 * mean_error:
            remove_indices.append(i)

    bad_v = []
    bad_c = []
    bad_c_error = []
    for i in remove_indices:
        bad_v.append(voltages[i])
        bad_c.append(capacitances[i])
        bad_c_error.append(errors[i])

    for i in bad_v:
        voltages.remove(i)

    for i in bad_c:
        capacitances.remove(i)

    for i in bad_c_error:
        errors.remove(i)

    combined_reduced_chi_squared = []

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

    intersection = (fit2[1] - fit1[1]) / (fit1[0] - fit2[0])
    intersection_error = round_sig(abs(intersection * math.sqrt(
        ((math.sqrt(info1.fiterr[1] ** 2 + info2.fiterr[1] ** 2) / (fit2[1] - fit1[1])) ** 2) + (
                    (math.sqrt(info1.fiterr[0] ** 2 + info2.fiterr[0] ** 2)) / (fit1[0] - fit2[0])) ** 2)), 1)
    intersection = round_sig(intersection, 2)

    output = [c_1_new, c_2_new, intersection, intersection_error]

    return output


def it_fits(data):
    """
    differences = []

    for i in range(len(data.i_mean) - 1):
        for x in range(i+1, len(data.i_mean)):
            if data.i_mean[i] < 1.2 * data.i_mean[x]:
                #differences.append(f'Current of {data.i_mean[i]}A at {data.time[i]}hours is more than 25% higher than {data.i_mean[x]}A at {data.time[x]}hours')
                differences.append([data.i_mean[i], data.i_mean[x]])
                break
            elif data.i_mean[i] > 0.8 * data.i_mean[x]:
                differences.append([data.i_mean[i], data.i_mean[x]])
                break
                #differences.append(f'Current of {data.i_mean[i]}A at {data.time[i]}hours is less than 25% low than {data.i_mean[x]}A at {data.time[x]}hours')
            else:
                continue
    print(differences)

    
    for i in range(len(data.i_mean)-1):
        if abs(data.i_mean[i]) > 1.25*abs(data.i_mean[i+1]):
            differences.append(f'Current of {data.i_mean[i]}A at {data.time[i]}hours is more than 25% higher than {data.i_mean[i+1]}A at {data.time[i+1]}hours')
        elif abs(data.i_mean[i]) < 0.75*abs(data.i_mean[i+1]):
            differences.append(f'Current of {data.i_mean[i]}A at {data.time[i]}hours is less than 25% low than {data.i_mean[i+1]}A at {data.time[i+1]}hours')
    """

    print('Fitting It')
    minimum_y = min(data.i_mean)
    max_allowed_y = minimum_y * 0.75
    maximum_y = max(data.i_mean)
    if maximum_y > max_allowed_y:
        pass_or_fail = 'Fail'
    else:
        pass_or_fail = 'Pass'

    return minimum_y, maximum_y, max_allowed_y, pass_or_fail


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


def round_sig(x, sig=2):
    return round(x, sig-int(math.floor(math.log10(abs(x))))-1)