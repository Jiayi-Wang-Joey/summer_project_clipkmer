dict1 = {'A':3, 'B': 2, 'C':2, 'D':3}
new_mean_values = {k: v / total for total in (sum(dict1.values(), 0.0),) for k, v in dict1.items()}
print(new_mean_values)