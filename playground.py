import numpy as np


from datetime import datetime

now = datetime.now()

current_time = now.strftime("%m/%d/%Y-%H-%M")
print("Current Time =", current_time)