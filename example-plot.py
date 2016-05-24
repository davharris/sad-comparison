from __future__ import division
import numpy as np
import macroeco_distributions as md
from scipy.stats import zipf
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline

# BBS 61036
# fia site 14057000012
# Gentry site 95
ab_array = np.array([[1L, 15L, 3L, 1L, 1L, 1L, 1L, 8L, 2L, 3L, 1L, 1L, 5L, 3L, 1L,
7L, 6L, 2L, 5L, 2L, 1L, 6L, 28L, 12L, 30L, 2L, 8L, 3L, 7L, 9L,
1L, 2L, 1L, 13L, 1L, 4L, 4L, 7L, 26L, 10L, 1L, 28L, 5L, 4L, 14L,
11L, 3L, 4L, 2L, 4L, 1L, 20L, 1L, 4L, 17L, 1L, 2L, 5L, 3L, 2L,
14L, 1L, 2L, 3L, 3L, 4L, 5L, 18L, 30L, 5L, 5L, 6L, 7L, 3L, 2L,
4L],
              [2L, 1L, 1L, 2L, 1L, 2L, 1L, 5L, 1L, 1L, 1L, 4L, 7L, 2L, 1L,
2L, 1L, 3L, 5L, 1L, 1L],
             [4L, 22L, 7L, 12L, 2L, 6L, 2L, 15L, 5L, 6L, 1L, 3L, 1L, 2L,
3L, 6L, 1L, 3L, 2L, 3L, 9L, 5L, 8L, 2L, 5L, 1L, 5L, 7L, 4L, 1L,
4L, 3L, 4L, 1L, 2L, 3L, 11L, 5L, 7L, 3L, 1L, 2L, 1L, 1L, 1L,
4L, 1L, 1L, 9L, 3L, 8L, 3L, 2L, 10L, 4L, 14L, 4L, 2L, 3L, 1L,
1L, 8L]])

# Color Brewer's 3-class Dark2 colors, plus black
colors = ["#000000", "#1b9e77", "#d95f02", "#7570b3"]
plot_labels = ["A: BBS site 61036", "B: FIA site 14057000012", "C: Gentry site 95"]

for i in range(3):
    ab = ab_array[i]

    x_values = np.array(range(max(ab) + 2)[1:])

    logser_p = md.logser_solver(ab)
    logser_values = md.trunc_logser.pmf(x_values, logser_p, upper_bound=float("inf"))
    lsll = md.logser_ll(ab, logser_p)

    nb_n, nb_p = md.nbinom_lower_trunc_solver(ab)
    nb_values = md.nbinom_lower_trunc.pmf(x_values, nb_n, nb_p)
    nbll = md.nbinom_lower_trunc_ll(ab, nb_n, nb_p)

    pln_mu, pln_sigma = md.pln_solver(ab)
    pln_values = md.pln.pmf(x_values, pln_mu, pln_sigma, lower_trunc=True)
    plnll = md.pln_ll(ab, pln_mu, pln_sigma)

    zipf_par = md.zipf_solver(ab)
    zipf_values = zipf.pmf(x_values, zipf_par)
    zll = md.zipf_ll(ab, zipf_par)

    ab_y = np.zeros(len(x_values) + 1)
    for j in range(len(ab)):
        ab_y[ab[j]] = ab_y[ab[j]] + 1/len(ab)

    fig= plt.figure(figsize=(12, 8), dpi=800)
    ax1 = fig.add_subplot(111)
    ax1.set_xlim([0,min(50, max(x_values))])
    #ax1.set_ylim([0,max(ab_y) * 1.25])

    plt.ylabel('frequency')
    plt.xlabel('abundance')
    plt.title(plot_labels[i])

    # Width originally set at 12 when width was 50.
    # This should be the same proportional width
    width = 12 / min(50, max(x_values)) * 50

    ax1.vlines(x = x_values, ymin = [0], ymax = .0025, color = "#AAAAAA")
    ax1.vlines(x = x_values, ymin=[0], ymax=ab_y[1:], linewidth = width, color = "#AAAAAA")
    ax1.plot(x_values, logser_values, color = colors[0], label = "log-series: " + str(round(lsll)), linewidth = 3)
    ax1.plot(x_values, nb_values, color = colors[1], label = "negative binomial: " + str(round(nbll)), linewidth = 3)
    ax1.plot(x_values, pln_values, color = colors[2], label = "Poisson lognormal: " + str(round(plnll)), linewidth = 3)
    ax1.plot(x_values, zipf_values, color = colors[3], label = "Zipf: " + str(round(zll)), linewidth = 3)
    plt.legend(loc='upper right');