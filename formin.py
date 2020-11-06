from flask import (
    Flask,
    request,
    redirect,
    url_for,
    jsonify,
    render_template,
    send_from_directory,
)
from helper import *
import smtplib

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("firstpage.html")


@app.route("/cal2", methods=["POST"])
def hello():
    cal = request.form["caltype"]  # ODF, Model or Intensities calculations
    inptype = int(request.form["cominp"])  # Standard(0) or User-defined(1)
    basetype = int(request.form["comtype"])  # Anders(0), Grevess(1) or Asplund()

    mbyh = float(request.form["mbyh"])  # M/H value

    anderslist = np.array(
        [
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
        ]
    )
    asplundlist = np.array(
        [
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
        ]
    )
    grevesslist = np.array(
        [
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
        ]
    )

    vallist = [anderslist, grevesslist, asplundlist]

    ablist = vallist[basetype]
    if cal == "ODF":
        return render_template(
            "odf2.html", mh=mbyh, stdtype=inptype, abtype=basetype, abunlist=ablist
        )
    elif cal == "Model":
        return render_template(
            "model2.html", mh=mbyh, stdtype=inptype, abtype=basetype, abunlist=ablist
        )
    elif cal == "Intensities":
        return render_template(
            "flux2.html", mh=mbyh, stdtype=inptype, abtype=basetype, abunlist=ablist
        )
    else:
        return "Wrong Input"


@app.route("/resodf", methods=["POST"])
def resultsodf():

    anderslist = [
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
    ]
    asplundlist = [
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
    ]
    grevesslist = [
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
    ]
    vallist = [anderslist, grevesslist, asplundlist]

    inptype = int(request.form["stdtype"])  # Standard(0) or User-defined(1)
    basetype = int(request.form["abtype"])  # Anders(0), Grevess(1) or Asplund(2)
    waveinp = int(request.form["waveinp"])  # Standard(0) or User-defined(1)
    tempinp = int(request.form["tempinp"])  # Standard(0) or User-defined(1)
    mbyh = float(request.form["mbyh"])
    minwave, maxwave, tgridstat = None, None, True
    tmin, tmax, tstep, pmin, pmax, pstep = None, None, None, None, None, None

    if waveinp == 1:
        minwave = int(request.form["wavemin"])
        maxwave = int(request.form["wavemax"])

    if tempinp == 1:
        tmin = int(request.form["tmin"])
        tmax = int(request.form["tmax"])
        tstep = int(request.form["tstep"])
        pmin = float(request.form["pmin"])
        pmax = float(request.form["pmax"])
        pstep = int(request.form["pstep"])
        gen_Tgrid_inp("INPUT/atlas9.Tgrid", tmin, tmax, tstep, pmin, pmax, pstep)
        tgridstat = False

    ablist = []

    if inptype == 1:
        for i in range(1, 100):
            id = "at" + str(i)
            ablist.append(float(request.form[id]))
    else:
        ablist = vallist[basetype]

    stat = False
    if (
        (inptype == 0) and (tempinp == 0) and waveinp == 0
    ):  # Check  for solutions in lib
        odfval, stat = check_ODF("ODFgrid.txt", mbyh, basetype)

    stat = True
    gen_pun_inp("INPUT/atlas9.punched.input", ablist, 1, basetype, mbyh)
    gen_inODF_inp("INPUT/atlas9.inODF", 1, [2.4])
    gen_control_inp("atlas9.control", 1, tgridstat)

    filename = "atlas9.odf"
    return render_template("results.html", filename=filename, curstat=stat)


@app.route("/resmodel", methods=["POST"])
def resultsmodel():

    anderslist = [
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
    ]
    asplundlist = [
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
    ]
    grevesslist = [
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
    ]
    vallist = [anderslist, grevesslist, asplundlist]

    inptype = int(request.form["stdtype"])  # Standard(0) or User-defined(1)
    basetype = int(request.form["abtype"])  # Anders(0), Grevess(1) or Asplund(2)
    # waveinp = int(request.form['waveinp']) #Standard(0) or User-defined(1)
    # tempinp = int(request.form['tempinp']) #Standard(0) or User-defined(1)
    mbyh = float(request.form["mbyh"])
    minwave, maxwave, tgridstat = None, None, True
    tmin, tmax, tstep, pmin, pmax, pstep = None, None, None, None, None, None

    # if (waveinp == 1):
    # 	minwave = int(request.form['wavemin'])
    # 	maxwave = int(request.form['wavemax'])

    # if tempinp == 1:
    # 	tmin = int(request.form['tmin'])
    # 	tmax = int(request.form['tmax'])
    # 	tstep = int(request.form['tstep'])
    # 	pmin = float(request.form['pmin'])
    # 	pmax = float(request.form['pmax'])
    # 	pstep = int(request.form['pstep'])
    # 	gen_Tgrid_inp("INPUT/atlas9.Tgrid", tmin, tmax, tstep, pmin, pmax, pstep)
    # 	tgridstat = False

    ablist = []

    if inptype == 1:
        for i in range(1, 100):
            id = "at" + str(i)
            ablist.append(float(request.form[id]))
    else:
        ablist = vallist[basetype]

    stat = False
    # if (inptype==0) and (tempinp==0) and waveinp ==0:	#Check  for solutions in lib
    # 	odfval, stat = check_ODF("ODFgrid.txt", mbyh, basetype)

    # stat = True
    # gen_pun_inp("INPUT/atlas9.punched.input", ablist, 1, basetype, mbyh)
    # gen_inODF_inp("INPUT/atlas9.inODF", 1, [2.4])
    # # gen_Tgrid_inp("INPUT/atlas9.Tgrid", minT, maxT, numT, minP, maxP, numP)

    # gen_control_inp("atlas9.control", 1, tgridstat)
    # stat = True
    filename = "atlas9.odf"
    # os.system("./runatlas9c.x")
    # send_from_directory(path, filename=image_name, as_attachment=True)
    # return "Hi you"
    return render_template("results.html", filename=filename, curstat=stat)


@app.route("/resflux", methods=["POST"])
def resultsflux():

    anderslist = [
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
    ]
    asplundlist = [
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
    ]
    grevesslist = [
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
    ]
    vallist = [anderslist, grevesslist, asplundlist]

    inptype = int(request.form["stdtype"])  # Standard(0) or User-defined(1)
    basetype = int(request.form["abtype"])  # Anders(0), Grevess(1) or Asplund(2)
    # waveinp = int(request.form['waveinp']) #Standard(0) or User-defined(1)
    # tempinp = int(request.form['tempinp']) #Standard(0) or User-defined(1)
    mbyh = float(request.form["mbyh"])
    minwave, maxwave, tgridstat = None, None, True
    tmin, tmax, tstep, pmin, pmax, pstep = None, None, None, None, None, None

    # if (waveinp == 1):
    # 	minwave = int(request.form['wavemin'])
    # 	maxwave = int(request.form['wavemax'])

    # if tempinp == 1:
    # 	tmin = int(request.form['tmin'])
    # 	tmax = int(request.form['tmax'])
    # 	tstep = int(request.form['tstep'])
    # 	pmin = float(request.form['pmin'])
    # 	pmax = float(request.form['pmax'])
    # 	pstep = int(request.form['pstep'])
    # 	gen_Tgrid_inp("INPUT/atlas9.Tgrid", tmin, tmax, tstep, pmin, pmax, pstep)
    # 	tgridstat = False

    ablist = []

    if inptype == 1:
        for i in range(1, 100):
            id = "at" + str(i)
            ablist.append(float(request.form[id]))
    else:
        ablist = vallist[basetype]

    stat = False
    # if (inptype==0) and (tempinp==0) and waveinp ==0:	#Check  for solutions in lib
    # 	odfval, stat = check_ODF("ODFgrid.txt", mbyh, basetype)

    # stat = True
    # gen_pun_inp("INPUT/atlas9.punched.input", ablist, 1, basetype, mbyh)
    # gen_inODF_inp("INPUT/atlas9.inODF", 1, [2.4])
    # # gen_Tgrid_inp("INPUT/atlas9.Tgrid", minT, maxT, numT, minP, maxP, numP)

    # gen_control_inp("atlas9.control", 1, tgridstat)
    stat = False
    filename = "atlas9.odf"
    # os.system("./runatlas9c.x")
    # send_from_directory(path, filename=image_name, as_attachment=True)
    # return "Hi you"
    return render_template("results.html", filename=filename, curstat=stat)


@app.route("/download", methods=["POST"])
def downloads():
    fname = request.form["fname"]
    path = "/home/pratik/flaskapp/bin/INPUT"
    # os.system("./runatlas9c.x")
    try:
        return send_from_directory(path, filename=fname, as_attachment=True)
    except FileNotFoundError:
        return redirect(url_for("home"))


@app.route("/download", methods=["GET"])
def download1():
    fname = "atlas9.odf"
    path = "/home/pratik/flaskapp/bin/INPUT"
    # os.system("./runatlas9c.x")
    try:
        return send_from_directory(path, filename=fname, as_attachment=True)
    except FileNotFoundError:
        return redirect(url_for("home"))


@app.route("/downl2", methods=["POST"])
def download2():
    ename = request.form["email"]
    # path = "/home/pratik/flaskapp/INPUT"
    os.system("./runatlas9c.x")

    sender = "pratikkedia44@gmail.com"
    receivers = [ename]
    # receivers = ['pr3t4k@gmail.com']

    # message = "From: From Person <from@fromdomain.com>\n\
    # To: To Person <to@todomain.com>\n\
    # Subject: SMTP e-mail test\n\
    # This is a test e-mail message.\
    # "
    message = "This mail is sent via python.\n http://127.0.0.1:5000/download"

    smtpObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpObj.login("pratikkedia44@gmail.com", "pratik123")
    smtpObj.sendmail(sender, receivers, message)
    print("Successfully sent email")
    smtpObj.quit()
    # try:
    # 	smtpObj = smtplib.SMTP_SSL("pratikkedia44@gmail.com", "pratik123")
    # 	smtpObj.sendmail(sender, receivers, message)
    # 	print ("Successfully sent email")
    # # except SMTPException:
    # except :
    # 	print ("Error: unable to send email")

    return redirect(url_for("home"))
    # try:
    # 	return send_from_directory(path, filename=fname, as_attachment=True)
    # except FileNotFoundError:
    # 	return redirect(url_for("home"))


# Convection status in ODF and lbyh, teff, logg

# convect on/off  1.5-2.0
# overshoot on-off (off)
# Number of velocities and velocity list in ODF
# Number of T and P
# what to do with the wavelength range
# standard tgrid is one given
# control file should have path for ODF file
