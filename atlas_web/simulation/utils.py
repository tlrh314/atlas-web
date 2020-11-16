from atlas_web.simulation.abundances import ANDERS, ASPLUND, GREVESS


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
        pass
        # raise SomethingError

    fname = "tmp.txt"
    with open(fname, "w") as f:
        f.write("We use the following abunances\n")
        f.write("\n".join(str(value) for value in abundances_to_use))
    return fname
