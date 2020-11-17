from atlas_web.simulation.abundances import ANDERS, ASPLUND, GREVESS
from atlas_web.simulation.grids import P_GRID, T_GRID, WAVELENGTH_GRID


def create_atlas_input_file_from_valid_form(cleaned_data):
    print("\n\nThe cleaned (=valid) form data are as follows\n")
    print(cleaned_data)
    print("End of form data\n\n")

    if cleaned_data["abundances"] == "anders":
        print("We will use anders abunances")
        abundances_to_use = ANDERS
    elif cleaned_data["abundances"] == "asplund":
        print("We will use asplund abunances")
        abundances_to_use = ASPLUND
    elif cleaned_data["abundances"] == "grevess":
        print("We will use grevess abunances")
        abundances_to_use = GREVESS
    else:
        raise

    if cleaned_data["wavelength_grid"] == "standard":
        print("We will use standard wavelength grid")
        wavelength_grid_to_use = WAVELENGTH_GRID
    elif cleaned_data["wavelength_grid"] == "non-standard":
        print("We will use non-standard wavelength grid")
        raise NotImplementedError
    else:
        raise

    if cleaned_data["T_grid"] == "standard":
        print("We will use standard temperature grid")
        T_grid_to_use = T_GRID
    elif cleaned_data["T_grid"] == "non-standard":
        print("We will use non-standard temperature grid")
        raise NotImplementedError
    else:
        raise

    if cleaned_data["p_grid"] == "standard":
        print("We will use standard pressure grid")
        P_grid_to_use = P_GRID
    elif cleaned_data["p_grid"] == "non-standard":
        print("We will use non-standard pressure grid")
        raise NotImplementedError
    else:
        raise

    fname = "tmp.txt"
    with open(fname, "w") as f:
        f.write("We use the following abunances\n")
        f.write("\n".join(str(value) for value in abundances_to_use))
        f.write("We use the following wavelength grid\n")
        f.write("\n".join(str(value) for value in wavelength_grid_to_use))
        f.write("We use the following T grid\n")
        f.write("\n".join(str(value) for value in T_grid_to_use))
        f.write("We use the following p grid\n")
        f.write("\n".join(str(value) for value in P_grid_to_use))
    return fname
