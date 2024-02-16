import pandas as pd
import matplotlib.pyplot as plt

# Your data
data = {
    'day_of_week': ['Monday', 'Tuesday', 'Tuesday', 'Tuesday', 'Wednesday', 'Wednesday', 'Wednesday'],
    'exercise': ['Push Up', 'Run', 'Kettle Bell 24', 'Dead Lift', 'Run', 'Dead Lift', 'Push Up'],
    'total_exercise_count': [90, 888, 58, 23, 134, 44, 40]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Pivot the data
pivot_df = df.pivot(index='day_of_week', columns='exercise', values='total_exercise_count')

# Replace NaN values with 0
pivot_df = pivot_df.fillna(0)

# Plot
pivot_df.plot(kind='bar', stacked=False)

# Show the plot
plt.show()


