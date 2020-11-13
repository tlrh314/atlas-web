import math
import os

def writefile(filename, var1, var2):
	fo = open(filename, "w")
	fo.write("Test text"+ var1 + var2)
	fo.close()
	print(var1)


def nametype(caltype):
	if (caltype == 1):
		calstr = "ODF"
	elif (caltype == 2):
		calstr = "Model"
	elif (caltype == 3):
		calstr = "Flux"
	return calstr

def nameabun(comtype):
	if comtype == 0:
		comstr = "Anders"
	elif comtype ==1:
		comstr = "Grevess"
	elif comtype == 2:
		comstr = "Asplund"
	elif comtype == 3:
		comstr = "User Defined"
	return comstr

# def getlist():
# 	return

def gen_pun_inp(filename, ablist, caltype, comtype, mbyh, constat=True, lbyh = 0.0, teff = 4000., gravity = 5.00000):
	lines = ["" for i in range(15)]

	calstr, comstr = nametype(caltype), nameabun(comtype)
	
	lines[0] = "TEFF   {:.0f}  GRAVITY {:.5f} LTE\n".format(teff,  gravity) 
	
	lines[1] = "TITLE  {} [{:.1f}] composition:{} L/H = {:.2f}\n".format(calstr, mbyh, comstr, lbyh)
	
	lines[2] = " OPACITY IFOP 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0\n"
	
	line4p1= ""
	if constat :
		line4p1 = " CONVECTION on   "
	else :
		line4p1 = " CONVECTION off  "

	lines[3] = line4p1+"{:.2f} TURBULENCE off   0.00  0.00  0.00  0.00\n".format(lbyh)
	
	line5p1 = "ABUNDANCE SCALE   " + format(pow(10, mbyh), '.3f')
	line5p2 = " ABUNDANCE CHANGE 1 "+ format(ablist[0], '.5f') + " 2 " + format(ablist[1], '.5f')+'\n'
	lines[4] = line5p1 + line5p2
	
	stra = " ABUNDANCE CHANGE"

	for i in range(2, 98, 6):
		linestr = stra
		for j in range(i, i+6):
			
			if(j < 9):
				linestr+= "  "+str(j+1)
			else :
				linestr+= " "+str(j+1)
			if(ablist[j] <= -10):
				linestr+= " "+format(ablist[j], '.2f')
			else :
				linestr+= "  " + format(ablist[j], '.2f')
		linestr+= '\n'
		lines.append(linestr)

	line22 = stra + " 99"
	if(ablist[98] <= -10):
		line22+= " "+format(ablist[98], '.2f')
	else :
		line22+= "  " + format(ablist[98], '.2f')
	lines.append(line22)

	fo = open(filename, "w")
	# fo.write("Testcode \n")
	fo.writelines(lines)
	fo.close()
	return

def gen_inmod_inp (filename, ablist, teff, gravity, mbyh, molstat = True, num_iterations = 500):
	lines = ["" for i in range(15)]

	lines[0] = "read punch\n"
	lines[1] = "read molecules\n"
	lines[2] = "opacity ifop 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0\n"
	lines[3] = "iterations {}\n".format(num_iterations)
	lines[4] = "correction on\n"
	molstr = "on\n"
	if not molstat : molstr = "off\n"
	lines[5] = "molecules "+molstr
	lines[6] = "print 0\n"
	lines[7] = "punch 2\n"
	lines[8] = "pressure on\n"
	lines[9]  = "binsizes on\n"
	lines[10] = "frequencies 1221 1 1210 little\n"
	lines[11] = "scale b -7.600 0.100 2.10 {0:.0f} {1:.2f}\n".format(teff, gravity)
	line13p1 = "abundance scale   " + format(pow(10, mbyh), '.5f')
	line13p2 = " abundance change 1 "+ format(ablist[0], '.5f') + " 2 " + format(ablist[1], '.5f')+'\n'
	lines[12]  = line13p1 + line13p2

	stra = " abundance change"

	for i in range(2, 98, 6):
		linestr = stra
		for j in range(i, i+6):
			if(j < 9):
				linestr+= "  "+str(j+1)
			else :
				linestr+= " "+str(j+1)
			if(ablist[j] <= -10):
				linestr+= " "+format(ablist[j], '.2f')
			else :
				linestr+= "  " + format(ablist[j], '.2f')
		linestr+= '\n'
		lines.append(linestr)

	line30 = stra + " 99"
	if(ablist[98] <= -10):
		line30+= " {:.2f}\n".format(ablist[98])
	else :
		line30+= "  {:.2f}\n".format(ablist[98])
	line31 = "begin\n"
	line32 = "end\n"
	lines.extend([line30, line31, line32])

	fo = open(filename, "w")
	fo.writelines(lines)
	fo.close()
	return

def gen_input_inp (filename):
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
	fo = open(filename, "w")
	fo.writelines(lines)
	fo.close()
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
	lines[7] +='\n'
	lines[8] = "pressure on\n"
	lines[9] = "binsizes on\n"
	lines[10] = "odfnumber {}\n".format(num_velocities+1)
	lines[11] = "begin\n"
	lines[12] = "end\n"
	fo = open(filename, "w")
	fo.writelines(lines)
	fo.close()
	return

def gen_Tgrid_inp(filename, minT, maxT, numT, minP, maxP,  numP):
	lines = ["" for i in range(numT+ numP+2)]
	lines[0] = str(numT)+'\n'
	lines[1] = str(numP)+'\n'

	logstepT = (math.log10(maxT) - math.log10(minT))/(numT-1)
	# mulfact = 10**logstepT
	lognum = math.log10(minT)
	num = minT
	for i in range(2, numT+2):
		lines[i] = str(int(math.ceil(num)))+'\n'
		lognum = lognum+logstepT
		num = 10**lognum
	
	logstepP = (math.log10(maxP) - math.log10(minP))/(numP-1)
	# mult = 10**logstepP
	lognum = math.log10(minP)
	num = minP
	for i in range(numT+2, numT+numP+2):
		lines[i] = "\t{:.3e}\n".format(num)
		lognum = lognum+logstepP
		num = 10**lognum

	fo = open(filename, "w")
	fo.writelines(lines)
	fo.close()
	return

def check_ODF(filename, mbyh, comptype):
	path = "ODFlib/{}/{}".format(nameabun(comptype), filename)
	fileo = open(path, 'r')
	Lines = fileo.readlines()

	mindiff = 6
	minval = 0
	for line in Lines:
		line = line.strip()
		val = float(line)
		diff = abs(mbyh - val)
		if diff < mindiff: 
			minval = val
			mindiff =  diff
	fileo.close()
	stat = False
	if mindiff <= 0.05: stat = True
	return minval, stat

def check_model(filename, teff, mbyh, logg, comptype):
	path = "MODELlib/{}/{}".format(nameabun(comptype), filename)
	fileo = open(path, 'r')
	Lines = fileo.readlines()
	Tpre , Mhpre, Gpre = None, None, None
	difftemp = 10000
	diffmbyh = 6
	difflogg = 5
	stat = False
	for line in Lines:
		line = line.strip()
		vals = list(map(float, line.split()))
		tdiff = abs(teff-vals[0])
		mhdiff = abs(mbyh - vals[1])
		lgdiff = abs(logg - vals[2])
		
		if (tdiff <= 100 and mhdiff<= 0.05 and  lgdiff <= 0.3):
			if (not stat):
				Tpre, Mhpre, Gpre = vals
				stat = True
				difftemp, diffmbyh, difflogg = tdiff, mhdiff, lgdiff
			
			elif ((tdiff < difftemp) or (tdiff<= difftemp and mhdiff < diffmbyh) or (tdiff<= difftemp and mhdiff <=diffmbyh and lgdiff <difflogg)):
				Tpre, Mhpre, Gpre = vals
				stat = True
				difftemp, diffmbyh, difflogg = tdiff, mhdiff, lgdiff

		elif (not stat) and ((tdiff < difftemp) or (tdiff<= difftemp and mhdiff < diffmbyh) or (tdiff<= difftemp and mhdiff <=diffmbyh and lgdiff <difflogg)):
			Tpre, Mhpre, Gpre = vals
			difftemp, diffmbyh, difflogg = tdiff, mhdiff, lgdiff
	
	fileo.close()
	return Tpre, Mhpre, Gpre, stat

def get_start_model(filename, teff, mbyh, logg, comptype):
	path = "MODELlib/{}/{}".format(comptype, filename)
	fileo = open(path, 'r')
	Lines = fileo.readlines()
	Tpre , Mhpre, Gpre = None, None, None
	Tdiff , Mdiff, Gdiff = abs(teff), abs(mbyh), abs(logg)	

	for line in Lines:
		line = line.strip()
		vals = list(map(float, line.split()))
		tdiff = abs(teff-vals[0])
		mhdiff = abs(mbyh - vals[1])
		lgdiff = abs(logg - vals[2])
		if (tdiff<= Tdiff and mhdiff <= Mdiff and lgdiff <= diff):
			Tdiff , Mdiff, Gdiff = tdiff, mhdiff, lgdiff
			Tpre, Mhpre, Gpre = vals
	
	fileo.close()
	return Tpre, Mhpre, Gpre

def gen_control_inp(filename, caltype, tgridstd = True):
	flags = [0, 0, 0]
	flags[(caltype-1)%3] = 1
	lines = ["" for i in range(14)]
	lines[0] = "! CONTROL file for SSWOP\n"
	lines[1] = "{}	- flagODF - 1-on, 0-off\n".format(flags[0])
	lines[2] = "{}	- flagmodel - 1-on, 0-off\n".format(flags[1])
	lines[3] = "{}	- flagflux - 1-on, 0-off\n".format(flags[2])
	lines[4] = "!!  INPUT file names first: for ODFs, then for model, then for flux\n"
	lines[5] = "'./INPUT/atlas9.inODF'\n"
	lines[6] = "'./INPUT/atlas9.inmod'\n"
	lines[7] = "'./INPUT/atlas9.input'\n"
	lines[8] = "!!  modelfile names: first ODFs, then starting model, last either output or flux input!\n"
	if tgridstd : lines[9] = "'./bin/INPUT/atlas9.Tgrid'\n"
	else : lines[9] =  "'./INPUT/atlas9.Tgrid'\n"
	lines[10] = "'./INPUT/atlas9.start'\n"
	lines[11] = "'./INPUT/atlas9.modinp'\n"
	lines[12] = "!! location and name of ODF in .nc file\n"
	lines[13] = "'./INPUT/ODF.nc'\n" 
	fo = open(filename, "w")
	fo.writelines(lines)
	fo.close()
	return

# ablist = [0.911, 0.089, -10.88, -10.89, -9.44, -3.48, -3.99, -3.11, -7.48, -3.95, -5.71, -4.46, -5.57, -4.49, -6.59, -4.83, -6.54, -5.48, -6.82, -5.68, -8.94, -7.05, -8.04, -6.37, -6.65, -4.37, -7.12, -5.79, -7.83, -7.44, -9.16, -8.63, -9.67, -8.69, -9.41, -8.81, -9.44, -9.14, -9.8, -9.54, -10.62, -10.12, -20.0, -10.2, -10.92, -10.35, -11.1, -10.18, -10.58, -10.04, -11.04, -9.8, -10.53, -9.81, -10.92, -9.91, -10.82, -10.49, -11.33, -10.54, -20.0, -11.04, -11.53, -10.92, -11.94, -10.94, -11.78, -11.11, -12.04, -10.96, -11.28, -11.16, -11.91, -10.93, -11.77, -10.59, -10.69, -10.24, -11.03, -10.95, -11.14, -10.19, -11.33, -20.0, -20.0, -20.0, -20.0, -20.0, -20.0, -11.92, -20.0, -12.51, -20.0, -20.0, -20.0, -20.0, -20.0, -20.0, -20.0]
	
# gen_Tgrid_inp("INPUT/Tgrid.txt", 100, 10000, 20, 0.000001, 1000000,  12)
# gen_inODF_inp("inODF.txt", 4, [1.0, 2.2, 1.3, 2.8])
# gen_inmod_inp ("inmod.txt", ablist, 4000, 0.1, 0.1)
# gen_pun_inp("punchedimp.txt", ablist, 1, 2, True, 0.2, lbyh = 0.0, teff = 4000., gravity = 5.00000)
# gen_control_inp("control.txt", 1)
# gen_input_inp("atlas9input.txt")
# os.system("qsub runODF")
# os.system("cd ..\nls")
# os.system("ls")
# caltype - for defining type of calculation(ODF:cal1, model:cal2, flux:cal3)
# comstr - for composition type - Anders, Grevess or Asplund or User Defined
# mbyh - M/H value
# lbyH - L/H value
