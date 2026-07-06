# Here we're just gonna try a really basic ensemble x ensemble sized fitness landscape
# I do not think this is gonna work well because we can't specify only 1-Mutant neighbour transitions on a 3D map (unless D = N = 2)

# returns a matrix of fitness changes between genotypes
def fitness_change(ensemble:dict,
                   fitness: list):
    diffs_matrix = np.zeros((len(ensemble), len(ensemble)))
    for i in range(len(ensemble)):
        for j in range(len(ensemble)):
            fit_diff = fitness[i] - fitness[j]
            diffs_matrix[i,j] = fit_diff
    return diffs_matrix 

# this function actually generates a plot given the diffs matrix from above, and the ensemble dict
def generate_scape(diffs: list,
                   ensemble: dict):
    z = diffs
    x = []
    y = []
    for i in ensemble.keys():
        x.append(i)
        y.append(i)
    x, y = np.meshgrid(x, y)

    # Set up plot
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(z, cmap=plt.colormaps["gist_earth"], vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)

    plt.show()