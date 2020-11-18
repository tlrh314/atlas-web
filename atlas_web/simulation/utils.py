import math

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

    convection = cleaned_data["convection"]

    def writefile(filename, var1, var2):
        with open(filename, "w") as fo:
            fo.write("Test text" + var1 + var2)
        print(var1)

    NAMETYPE = {1: "ODF", 2: "Model", 3: "Flux"}

    NAMEABUN = {"anders": 0, "grevess": 1, "asplund": 2, "User Defined": 3}

    # gen_pun_inp("INPUT/atlas9.punched.input", ablist, 1, basetype, mbyh)
    def gen_pun_inp(
        filename,  # "INPUT/atlas9.punched.input"
        ablist,  # ablist
        caltype,  # 1
        comtype,  # basetype Anders(0), Grevess(1) or Asplund(2)
        mbyh,  # mbhy
        constat=True,
        lbyh=0.0,
        teff=4000.0,
        gravity=5.00000,
    ):
        lines = ["" for i in range(15)]

        calstr, comstr = NAMETYPE[caltype], NAMEABUN[comtype]

        lines[0] = "TEFF   {:.0f}  GRAVITY {:.5f} LTE\n".format(teff, gravity)

        lines[1] = "TITLE  {} [{:.1f}] composition:{} L/H = {:.2f}\n".format(
            calstr, mbyh, comstr, lbyh
        )

        lines[2] = " OPACITY IFOP 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0\n"

        line4p1 = ""
        if cleaned_data["convection"]:
            line4p1 = " CONVECTION on   "
        else:
            line4p1 = " CONVECTION off  "

        lines[3] = line4p1 + "{:.2f} TURBULENCE off   0.00  0.00  0.00  0.00\n".format(
            lbyh
        )

        line5p1 = "ABUNDANCE SCALE   " + format(pow(10, mbyh), ".3f")
        line5p2 = (
            " ABUNDANCE CHANGE 1 "
            + format(ablist[0], ".5f")
            + " 2 "
            + format(ablist[1], ".5f")
            + "\n"
        )
        lines[4] = line5p1 + line5p2

        stra = " ABUNDANCE CHANGE"

        for i in range(2, 98, 6):
            linestr = stra
            for j in range(i, i + 6):

                if j < 9:
                    linestr += "  " + str(j + 1)
                else:
                    linestr += " " + str(j + 1)
                if ablist[j] <= -10:
                    linestr += " " + format(ablist[j], ".2f")
                else:
                    linestr += "  " + format(ablist[j], ".2f")
            linestr += "\n"
            lines.append(linestr)

        line22 = stra + " 99"
        if ablist[98] <= -10:
            line22 += " " + format(ablist[98], ".2f")
        else:
            line22 += "  " + format(ablist[98], ".2f")
        lines.append(line22)

        with open(filename, "w") as fo:
            # fo.write("Testcode \n")
            fo.writelines(lines)
        return lines

    def gen_inmod_inp(
        filename, ablist, teff, gravity, mbyh, molstat=True, num_iterations=500
    ):
        lines = ["" for i in range(15)]

        lines[0] = "read punch\n"
        lines[1] = "read molecules\n"
        lines[2] = "opacity ifop 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0\n"
        lines[3] = "iterations {}\n".format(num_iterations)
        lines[4] = "correction on\n"
        molstr = "on\n"
        if not molstat:
            molstr = "off\n"
        lines[5] = "molecules " + molstr
        lines[6] = "print 0\n"
        lines[7] = "punch 2\n"
        lines[8] = "pressure on\n"
        lines[9] = "binsizes on\n"
        lines[10] = "frequencies 1221 1 1210 little\n"
        lines[11] = "scale b -7.600 0.100 2.10 {0:.0f} {1:.2f}\n".format(teff, gravity)
        line13p1 = "abundance scale   " + format(pow(10, mbyh), ".5f")
        line13p2 = (
            " abundance change 1 "
            + format(ablist[0], ".5f")
            + " 2 "
            + format(ablist[1], ".5f")
            + "\n"
        )
        lines[12] = line13p1 + line13p2

        stra = " abundance change"

        for i in range(2, 98, 6):
            linestr = stra
            for j in range(i, i + 6):
                if j < 9:
                    linestr += "  " + str(j + 1)
                else:
                    linestr += " " + str(j + 1)
                if ablist[j] <= -10:
                    linestr += " " + format(ablist[j], ".2f")
                else:
                    linestr += "  " + format(ablist[j], ".2f")
            linestr += "\n"
            lines.append(linestr)

        line30 = stra + " 99"
        if ablist[98] <= -10:
            line30 += " {:.2f}\n".format(ablist[98])
        else:
            line30 += "  {:.2f}\n".format(ablist[98])
        line31 = "begin\n"
        line32 = "end\n"
        lines.extend([line30, line31, line32])

        with open(filename, "w") as fo:
            fo.writelines(lines)

        return

    def gen_input_inp(filename):
        lines = ["" for i in range(15)]

        lines[0] = "read punch\n"
        lines[1] = "read molecules\n"
        lines[2] = "opacity ifop 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0\n"
        lines[3] = "correction off\n"
        lines[4] = "pressure off\n"
        lines[5] = "molecules on"
        lines[6] = "recalxne on\n"
        lines[7] = "binsizes on\n"
        lines[8] = "iterations 1\n"
        lines[9] = "print 0\n"
        lines[10] = "punch 2\n"
        lines[11] = "frequencies 1221 30 1221 little\n"
        lines[12] = "surface intensiy 1 1.0\n"
        lines[13] = "begin\n"
        lines[14] = "end\n"
        with open(filename, "w") as fo:
            fo.writelines(lines)

        return

    def gen_inODF_inp(filename, num_velocities, vel_list):
        lines = ["" for i in range(13)]

        lines[0] = "read punch\n"
        lines[1] = "read molecules\n"
        lines[2] = "opacity ifop 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0\n"
        lines[3] = "correction off\n"
        lines[4] = "molecules on\n"
        lines[5] = "print 0\n"
        lines[6] = "punch 2\n"
        lines[7] = "vecolities values {}".format(num_velocities)
        for vel in vel_list:
            lines[7] += " {:.1f}".format(vel)
        lines[7] += "\n"
        lines[8] = "pressure on\n"
        lines[9] = "binsizes on\n"
        lines[10] = "odfnumber {}\n".format(num_velocities + 1)
        lines[11] = "begin\n"
        lines[12] = "end\n"
        with open(filename, "w") as fo:
            fo.writelines(lines)

        return

    def gen_Tgrid_inp(filename, minT, maxT, numT, minP, maxP, numP):
        lines = ["" for i in range(numT + numP + 2)]
        lines[0] = str(numT) + "\n"
        lines[1] = str(numP) + "\n"

        logstepT = (math.log10(maxT) - math.log10(minT)) / (numT - 1)
        # mulfact = 10**logstepT
        lognum = math.log10(minT)
        num = minT
        for i in range(2, numT + 2):
            lines[i] = str(int(math.ceil(num))) + "\n"
            lognum = lognum + logstepT
            num = 10 ** lognum

        logstepP = (math.log10(maxP) - math.log10(minP)) / (numP - 1)
        # mult = 10**logstepP
        lognum = math.log10(minP)
        num = minP
        for i in range(numT + 2, numT + numP + 2):
            lines[i] = "\t{:.3e}\n".format(num)
            lognum = lognum + logstepP
            num = 10 ** lognum

        with open(filename, "w") as fo:
            fo.writelines(lines)

        return

    def check_ODF(filename, mbyh, comptype):
        path = "ODFlib/{}/{}".format(NAMEABUN[comptype], filename)
        fileo = open(path, "r")
        Lines = fileo.readlines()

        mindiff = 6
        minval = 0
        for line in Lines:
            line = line.strip()
            val = float(line)
            diff = abs(mbyh - val)
            if diff < mindiff:
                minval = val
                mindiff = diff
        fileo.close()
        stat = False
        if mindiff <= 0.05:
            stat = True
        return minval, stat

    def check_model(filename, teff, mbyh, logg, comptype):
        path = "MODELlib/{}/{}".format(NAMEABUN[comptype], filename)
        fileo = open(path, "r")
        Lines = fileo.readlines()
        Tpre, Mhpre, Gpre = None, None, None
        difftemp = 10000
        diffmbyh = 6
        difflogg = 5
        stat = False
        for line in Lines:
            line = line.strip()
            vals = list(map(float, line.split()))
            tdiff = abs(teff - vals[0])
            mhdiff = abs(mbyh - vals[1])
            lgdiff = abs(logg - vals[2])

            if tdiff <= 100 and mhdiff <= 0.05 and lgdiff <= 0.3:
                if not stat:
                    Tpre, Mhpre, Gpre = vals
                    stat = True
                    difftemp, diffmbyh, difflogg = tdiff, mhdiff, lgdiff

                elif (
                    (tdiff < difftemp)
                    or (tdiff <= difftemp and mhdiff < diffmbyh)
                    or (tdiff <= difftemp and mhdiff <= diffmbyh and lgdiff < difflogg)
                ):
                    Tpre, Mhpre, Gpre = vals
                    stat = True
                    difftemp, diffmbyh, difflogg = tdiff, mhdiff, lgdiff

            elif (not stat) and (
                (tdiff < difftemp)
                or (tdiff <= difftemp and mhdiff < diffmbyh)
                or (tdiff <= difftemp and mhdiff <= diffmbyh and lgdiff < difflogg)
            ):
                Tpre, Mhpre, Gpre = vals
                difftemp, diffmbyh, difflogg = tdiff, mhdiff, lgdiff

        fileo.close()
        return Tpre, Mhpre, Gpre, stat

    def get_start_model(filename, teff, mbyh, logg, comptype):
        path = "MODELlib/{}/{}".format(comptype, filename)
        fileo = open(path, "r")
        Lines = fileo.readlines()
        Tpre, Mhpre, Gpre = None, None, None
        Tdiff, Mdiff, Gdiff = abs(teff), abs(mbyh), abs(logg)

        for line in Lines:
            line = line.strip()
            vals = list(map(float, line.split()))
            tdiff = abs(teff - vals[0])
            mhdiff = abs(mbyh - vals[1])
            lgdiff = abs(logg - vals[2])
            if tdiff <= Tdiff and mhdiff <= Mdiff and lgdiff <= diff:
                Tdiff, Mdiff, Gdiff = tdiff, mhdiff, lgdiff
                Tpre, Mhpre, Gpre = vals

        fileo.close()
        return Tpre, Mhpre, Gpre

    def gen_control_inp(filename, caltype, tgridstd=True):
        flags = [0, 0, 0]
        flags[(caltype - 1) % 3] = 1
        lines = ["" for i in range(14)]
        lines[0] = "! CONTROL file for SSWOP\n"
        lines[1] = "{}	- flagODF - 1-on, 0-off\n".format(flags[0])
        lines[2] = "{}	- flagmodel - 1-on, 0-off\n".format(flags[1])
        lines[3] = "{}	- flagflux - 1-on, 0-off\n".format(flags[2])
        lines[
            4
        ] = "!!  INPUT file names first: for ODFs, then for model, then for flux\n"
        lines[5] = "'./INPUT/atlas9.inODF'\n"
        lines[6] = "'./INPUT/atlas9.inmod'\n"
        lines[7] = "'./INPUT/atlas9.input'\n"
        lines[
            8
        ] = "!!  modelfile names: first ODFs, then starting model, last either output or flux input!\n"
        if tgridstd:
            lines[9] = "'./bin/INPUT/atlas9.Tgrid'\n"
        else:
            lines[9] = "'./INPUT/atlas9.Tgrid'\n"
        lines[10] = "'./INPUT/atlas9.start'\n"
        lines[11] = "'./INPUT/atlas9.modinp'\n"
        lines[12] = "!! location and name of ODF in .nc file\n"
        lines[13] = "'./INPUT/ODF.nc'\n"
        fo = open(filename, "w")
        fo.writelines(lines)
        fo.close()
        return

    fnames = ["atlas9.punched.input", "atlas9.inODF", "atlas9.control"]
    gen_pun_inp(
        fnames[0],
        abundances_to_use,
        1,  # 1 for ODF
        cleaned_data["abundances"],
        cleaned_data["metallicity"],
    )

    gen_inODF_inp(fnames[1], 1, [2.4])

    # last argument True if we are on a custom wav grid
    # if we are on a custom T grid it is False
    gen_control_inp(fnames[2], 1, True)

    # with open(fname, "w") as f:
    #     f.write("We use the following abunances\n")
    #     f.write("\n".join(str(value) for value in abundances_to_use))
    #     f.write("We use the following wavelength grid\n")
    #     f.write("\n".join(str(value) for value in wavelength_grid_to_use))
    #     f.write("We use the following T grid\n")
    #     f.write("\n".join(str(value) for value in T_grid_to_use))
    #     f.write("We use the following p grid\n")
    #     f.write("\n".join(str(value) for value in P_grid_to_use))
    return fnames
