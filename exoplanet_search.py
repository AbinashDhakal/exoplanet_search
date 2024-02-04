import numpy as np
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('exoplanet_confirm_and_candidates.csv')

# Rename columns for better readability
df = df.rename(columns={"# name": "planet_name", "mass": "mass_jup", "radius": "radius_jup"})

# Calculate additional columns in Earth units
df['mass_earth'] = df['mass_jup'] * 317.8
df['radius_earth'] = df['radius_jup'] * 11.5

# Take logarithm for better visualization on a log scale, handling zero or negative values
df['log_mass_earth'] = np.log10(df['mass_earth'].replace(0, np.nan))
df['log_radius_earth'] = np.log10(df['radius_earth'].replace(0, np.nan))
df['log_orbital_period'] = np.log10(df['orbital_period'].replace(0, np.nan))
df['log_star_teff'] = np.log10(df['star_teff'].replace(0, np.nan))

# Select relevant columns excluding those related to errors and unnecessary information
columns = list(df.columns)
new_columns = [i for i in columns if 'error' not in i]
df_2 = df[new_columns].drop(['inclination', 'angular_distance', 'discovered', 'updated', 'omega', 'tperi',
                             'tconj', 'tzero_tr', 'tzero_tr_sec', 'lambda_angle', 'impact_parameter',
                             'tzero_vr', 'hot_point_lon', 'log_g', 'publication', 'ra', 'dec', 'mag_v',
                             'mag_i', 'mag_j', 'mag_h', 'mag_k', 'star_detected_disc', 'star_magnetic_field',
                             'star_alternate_names'], axis=1)

# Split the dataframe into confirmed and candidates
confirmed = df_2.query('planet_status == "Confirmed"')
candidates = df_2.query('planet_status == "Candidate"')

# Visualizations for confirmed exoplanets

# Orbital period - planet mass
fig_orbital_period_mass = px.scatter(confirmed, x="log_orbital_period", y="log_mass_earth",
                                     hover_data=['planet_name'], color='star_teff',
                                     title='Orbital Period vs. Planet Mass for Confirmed Exoplanets')
fig_orbital_period_mass.show()

# Save the plot as a PNG file
fig_orbital_period_mass.write_image("orbital_period_mass_plot.png")

# Remove the hottest stars for better visualization
confirmed_temp = confirmed.query('star_teff <= 10000')
fig_orbital_period_mass_filtered = px.scatter(confirmed_temp, x="log_orbital_period", y="log_mass_earth",
                                              hover_data=['planet_name'], color='star_teff',
                                              title='Filtered: Orbital Period vs. Planet Mass for Confirmed Exoplanets')
fig_orbital_period_mass_filtered.show()

# Save the plot as a PNG file
fig_orbital_period_mass_filtered.write_image("orbital_period_mass_filtered_plot.png")

# Scatter plot for confirmed exoplanets without temperature filter
fig_orbital_period_mass_all = px.scatter(confirmed, x="log_orbital_period", y="log_mass_earth",
                                         hover_data=['planet_name'], color='star_teff')
fig_orbital_period_mass_all.show()

# Save the plot as a PNG file
fig_orbital_period_mass_all.write_image("orbital_period_mass_all_plot.png")

# Scatter plot for confirmed exoplanets with temperature filter on radius
confirmed_temp = confirmed.query('star_teff <= 10000')
confirmed_rad = confirmed_temp.query('log_radius_earth > -1 & log_radius_earth < 1.5')
fig_orbital_period_radius = px.scatter(confirmed_rad, x="log_orbital_period", y="log_radius_earth",
                                       hover_data=['planet_name'], color='star_teff')
fig_orbital_period_radius.show()

# Save the plot as a PNG file
fig_orbital_period_radius.write_image("orbital_period_radius_plot.png")

# Further analysis and visualizations can be added as per your specific objectives.

# Displaying statistical information about the datasets
print("Confirmed Exoplanets:")
print(confirmed.describe())

print("\nCandidate Exoplanets:")
print(candidates.describe())
