""" Use tuple for pre-defined lists b/c tuples are immutable """

# https://ui.adsabs.harvard.edu/abs/1989GeCoA..53..197A/abstract
ANDERS = (
    0.911,
    0.089,
    -10.88,
    -10.89,
    -9.44,
    -3.48,
    -3.99,
    -3.11,
    -7.48,
    -3.95,
    -5.71,
    -4.46,
    -5.57,
    -4.49,
    -6.59,
    -4.83,
    -6.54,
    -5.48,
    -6.82,
    -5.68,
    -8.94,
    -7.05,
    -8.04,
    -6.37,
    -6.65,
    -4.37,
    -7.12,
    -5.79,
    -7.83,
    -7.44,
    -9.16,
    -8.63,
    -9.67,
    -8.69,
    -9.41,
    -8.81,
    -9.44,
    -9.14,
    -9.8,
    -9.54,
    -10.62,
    -10.12,
    -20.0,
    -10.2,
    -10.92,
    -10.35,
    -11.1,
    -10.18,
    -10.58,
    -10.04,
    -11.04,
    -9.8,
    -10.53,
    -9.81,
    -10.92,
    -9.91,
    -10.82,
    -10.49,
    -11.33,
    -10.54,
    -20.0,
    -11.04,
    -11.53,
    -10.92,
    -11.94,
    -10.94,
    -11.78,
    -11.11,
    -12.04,
    -10.96,
    -11.28,
    -11.16,
    -11.91,
    -10.93,
    -11.77,
    -10.59,
    -10.69,
    -10.24,
    -11.03,
    -10.95,
    -11.14,
    -10.19,
    -11.33,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -11.92,
    -20.0,
    -12.51,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
)

# https://ui.adsabs.harvard.edu/abs/2006NuPhA.777....1A/abstract
ASPLUND = (
    0.9204,
    0.07834,
    -10.99,
    -10.66,
    -9.34,
    -3.61,
    -4.21,
    -3.35,
    -7.48,
    -4.11,
    -5.8,
    -4.44,
    -5.59,
    -4.53,
    -6.63,
    -4.92,
    -6.54,
    -5.64,
    -7.01,
    -5.7,
    -8.89,
    -7.09,
    -8.11,
    -6.4,
    -6.61,
    -4.54,
    -7.05,
    -5.82,
    -7.85,
    -7.48,
    -9.0,
    -8.39,
    -9.74,
    -8.7,
    -9.5,
    -8.79,
    -9.52,
    -9.17,
    -9.83,
    -9.46,
    -10.58,
    -10.16,
    -20.0,
    -10.29,
    -11.13,
    -10.47,
    -11.1,
    -10.33,
    -11.24,
    -10.0,
    -11.03,
    -9.86,
    -10.49,
    -9.8,
    -11.0,
    -9.86,
    -10.94,
    -10.46,
    -11.32,
    -10.62,
    -20.0,
    -11.08,
    -11.52,
    -10.97,
    -11.74,
    -10.94,
    -11.56,
    -11.12,
    -11.94,
    -11.2,
    -11.94,
    -11.19,
    -12.16,
    -11.19,
    -11.78,
    -10.64,
    -10.66,
    -10.42,
    -11.12,
    -10.87,
    -11.14,
    -10.29,
    -11.39,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -12.02,
    -20.0,
    -12.58,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
)

# https://ui.adsabs.harvard.edu/abs/1998SSRv...85..161G/abstract
GREVESS = (
    0.9204,
    0.0783,
    -10.94,
    -10.64,
    -9.49,
    -3.52,
    -4.12,
    -3.21,
    -7.48,
    -3.96,
    -5.71,
    -4.46,
    -5.57,
    -4.49,
    -6.59,
    -4.71,
    -6.54,
    -5.64,
    -6.92,
    -5.68,
    -8.87,
    -7.02,
    -8.04,
    -6.37,
    -6.65,
    -4.54,
    -7.12,
    -5.79,
    -7.83,
    -7.44,
    -9.16,
    -8.63,
    -9.67,
    -8.63,
    -9.41,
    -8.73,
    -9.44,
    -9.07,
    -9.8,
    -9.44,
    -10.62,
    -10.12,
    -20.0,
    -10.2,
    -10.92,
    -10.35,
    -11.1,
    -10.27,
    -10.38,
    -10.04,
    -11.04,
    -9.8,
    -10.53,
    -9.87,
    -10.91,
    -9.91,
    -10.87,
    -10.46,
    -11.33,
    -10.54,
    -20.0,
    -11.03,
    -11.53,
    -10.92,
    -11.69,
    -10.9,
    -11.78,
    -11.11,
    -12.04,
    -10.96,
    -11.98,
    -11.16,
    -12.17,
    -10.93,
    -11.76,
    -10.59,
    -10.69,
    -10.24,
    -11.03,
    -10.91,
    -11.14,
    -10.09,
    -11.33,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -11.95,
    -20.0,
    -12.54,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
    -20.0,
)