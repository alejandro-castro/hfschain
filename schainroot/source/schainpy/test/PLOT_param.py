import os, sys
import time
import datetime

path = os.path.split(os.getcwd())[0]
sys.path.append(path)
from controller import *
desc = "Este programa graficara los parametros adquiridos a traves de los momentos espectrales."
filename = "hf_test.xml"
controllerObj = Project()
controllerObj.setup(id = '191', name='paramplot', description=desc)

#----------------------------------------------NEW----------------------------------------------------#
'''
example:
python PLOT_HF.py  -path '/media/igp-114/PROCDATA' -f 2.72 -C 0 -ii 6 -online 0 -code 0 -date "2018/01/25" -startTime "00:00:00" -endTime "23:59:59" -lo 31
'''
print "REVISAR LA LINEA DE EJEMPLO EN EL ARCHIVO EN CASO PROBLEMAS DE EJECUCION"
import argparse
parser = argparse.ArgumentParser()
########################## PATH- DATA  ###################################################################################################
parser.add_argument('-path',action='store',dest='path_lectura',help='Directorio de Datos \
    .Por defecto, se esta ingresando entre comillas /media/igp-114/PROCDATA/',default='/media/ci-81/062717d4-e7c7-4462-9365-08418e5483b2/')
########################## FRECUENCIA ####################################################################################################
parser.add_argument('-f',action='store',dest='f_freq',type=float,help='Frecuencia en Mhz 2.72 y 3.64. Por defecto, se esta ingresando 2.72 ',default=2.72)
########################## CAMPAIGN ### 600 o 100 perfiles ###############################################################################
parser.add_argument('-C',action='store',dest='c_campaign',type=int,help='Campaign 1 (600 perfiles) y 0(100 perfiles). Por defecto, se esta ingresando 1',default=1)
########################## INCOHERENT INTEGRATION ### Entre 0 y 6  #######################################################################
parser.add_argument('-ii',action='store',dest='i_integration',type=int,help='Data spectra tiene integraciones incoherentes entre \
    0 y 6. Por defecto, se esta ingresando 0',default=0)
########################## ONLINE OR OFFLINE   ###########################################################################################
parser.add_argument('-online',action='store',dest='online',type=int,help='Operacion 0 Off-line 1 On-Line\
       .Por defecto, se esta ingresando 0(off Line) ',default=0)
########################## CODIGO - INPUT ################################################################################################
parser.add_argument('-code',action='store',dest='code_seleccionado',type=int,help='Code de Tx para generar en estacion \
    de Rx Spectro 0,1,2. Por defecto, se esta ingresando 0(Ancon)',default=0)
########################## DAY- SELECCION ################################################################################################
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
daybefore= yesterday.strftime("%Y/%m/%d")
today = datetime.datetime.now().strftime("%Y/%m/%d")
parser.add_argument('-date',action='store',dest='date_seleccionado',help='Seleccionar fecha si es OFFLINE se ingresa \
    la fecha con el dia deseado. Por defecto, considera el dia anterior',default=daybefore)
######################### TIME- SELECCION ################################################################################################
parser.add_argument('-startTime',action='store',dest='time_start',help='Ingresar tiempo de inicio, formato 15:00:00 entre comillas',default="00:00:00")
parser.add_argument('-endTime',action='store',dest='time_end',help='Ingresar tiempo de fin, formato 23:59:59 entre comillas',default="23:59:59")

########################## LOCATION AND ORIENTATION ####################################################################################################
parser.add_argument('-lo',action='store',dest='lo_seleccionado',type=int,help='Parametro para establecer la ubicacion de la estacion de Rx y su orientacion.\
    Example: XA   ----- X: Es el primer valor determina la ubicacion de la estacion. A: Es \
      el segundo valor determina la orientacion N45O o N45E.  \
    11: JRO-N450, 12: JRO-N45E \
            21: HYO-N45O, 22: HYO-N45E',default=11)
###########################################################################################################################################
results    = parser.parse_args()
path       = str(results.path_lectura)
freq       = results.f_freq
campaign   = results.c_campaign
inc_int    = results.i_integration
online       = (results.online)
code       = int(results.code_seleccionado)
date       = results.date_seleccionado
time_start = results.time_start
time_end   = results.time_end
lo         = results.lo_seleccionado

nProfiles = 100
nFFT      = 100
set       = 0

if campaign == 1:
    nProfiles=600
    nFFT     =600
    inc_int= 0
if online == 1:
    date      = today
    time_start= "00:00:00"
    time_end  = "23:59:59"
    set = None

ngraph= 1
if freq <3:
    ngraph= 0

setupF   = freq
setradarF= freq*10**6
numberF  = int(freq*10**3)
number   = str(numberF)
lo_n=lo/10
lo_0=lo_n*10+1
lo_1=lo_0+1

print "Path",path
print "Frecuencia en Mhz",freq
print "Freq_setup",freq
print "Freq_setradar",setradarF
print "Freq_number", numberF
print "Mode Campaign" ,campaign
print "nProfiles",nProfiles
print "nFFT",nFFT
print "Incoherent integration",inc_int
print "Online",online
print "Code",code
print "Date",date
print "Time_start", time_start
print "Time_end"  , time_end
print "ngraph",ngraph
print "set",set
print "Location&orientation",lo
print "REVISAR LA LINEA DE EJEMPLO EN EL ARCHIVO EN CASO PROBLEMAS DE EJECUCION"

time.sleep(1)
#-----------------------------------------------------------------------------------------------------#
#python PLOT_HF_test.py -online 0 -C 0 -ii 6 -f 2.64990234375 -code 0 -date "2018/01/08" -startTime "00:20:00" -endTime "23:59:59" -lo 11

#-------------------------PATH-PDATA-------------------------------------
#path='/media/igp-114/PROCDATA/'
#-----------------------------PATH-graficos-----------------------------------#

figpath=    '/home/jm/Pictures/graphics_schain/sp'+str(code)+'1_f'+str(ngraph)+'/'
parampath = '/home/jm/Pictures/graphics_schain/sp'+str(code)+'1_f'+str(ngraph)+'/param/'
print "figpath",figpath
print "paramPath", parampath
#---------------------------------------------------------------------------#
'''
readUnitConfObj = controllerObj.addReadUnit(datatype = 'HFReader',
                                            path     = path,
                                            startDate= date,   #'2017/12/31',# 2017/11/14 date
                                            endDate  = date,   #'2017/12/31',#date 2017/11/14
                                            code     = code,
                                            frequency= setupF,
                                            campaign = campaign,
                                            inc_int  = inc_int,
                                            startTime= time_start,
                                            endTime  = time_end,
                                            online   = online,
                                            set      = 0,
                                            delay    = 0,
                                            walk     = 1,
                                            timezone = -5*3600
                                            )
'''
#controllerObj es una clase Project que inicializa algunas variables simples
# y un Diccionario llamado self.procUnitConfObjDict = {}
# En este diccionario al parecer iran ingresando una serie de procesos formando una cola.
# Quien Agrega procesos a procUnitConfObjDict ?
# addReadUnit agregara una unidad de lectura y configurara esa unida en ReadUnitConf()
# tambien hara el setup donde se configuran el id, starttime endtime day y se llama a
# addRunOperation(**kwargs)
# Preguta : que es addRunOperation()?
# R: addRunOperation llama a addOperation y ha addParameter.
# Pregunta que es addOperation?
# R: addOperation agrega un id y una prioridad a la Operacion
# llama a OperationConf()
# {Que es OperationConf?}
# {R: Es una clase base que ne su setup declara la lista parmConfObjList }
# llama a Operation.setup
# y agrega la configuracion a la lista de configuraciones.

# Pregunta que es addParameter?
# R: addParameter tiene 2 significados dependiendo de la clase donde se encuentre
# lo tiene OperationConf() y procUnitConf(), manda todos los kwargs a opConfObjList[0],
# Pregunta xq a la primera posicion? es acaso una lista? o un diccionario?


# Pregunta es : que es ReadUnitConf()?
# R: ReadUnitConf() es una clase que hereda de procUnitConf

# Pregunta que es procUnitConf?
# R: procUnitConf es una unidad de procesamiento, que inicializa ciertos valores como
# un diccionario opObjDict y una lista opConfObjList.
# Gracias a que hereda de procUnitConf se le puede asignar los metodos "addOperation", "addParameter"
# y el .run()!




readUnitConfObj = controllerObj.addReadUnit(datatype='HFParamReader',
                                            path     = parampath,
                                            startDate= date,   #'2017/12/31',# 2017/11/14 date
                                            endDate  = date,   #'2017/12/31',#date 2017/11/14
                                            code     = code,
                                            frequency= setupF,
                                            campaign = campaign,
                                            inc_int  = inc_int,
                                            startTime= time_start,
                                            endTime  = time_end,
                                            online   = online,
                                            set      = 0,
                                            delay    = 0,
                                            walk     = 1,
                                            timezone = -5*3600
                                            )

# procUnitConfObj0 = controllerObj.addProcUnit(datatype='HDF5Reader', inputId=readUnitConfObj.getId())
#
# opObj1 = procUnitConfObj0.addOperation(name='HDF5Reader')
# opObj1.addParameter(name='path', value=figpath+'/param')
# opObj1.addParameter(name='blocksPerFile', value='10', format='int')
# opObj1.addParameter(name='metadataList',value='type,inputUnit,heightList,frequency',format='list')#,RxInfo,TxInfo /*RxInfo = lat,long,alt,type double or simple, etc...
# opObj1.addParameter(name='dataList',value='data_param,data_SNR,data_RGB,CrossData,utctime',format='list')#AvgCohModuledata_DC,data_Coherence
# opObj1.addParameter(name='mode',value='0',format='int')#call channels


print "Escribiendo el archivo XML"
controllerObj.writeXml(filename)
print "Leyendo el archivo XML"
controllerObj.readXml(filename)

controllerObj.createObjects()
controllerObj.connectObjects()

#timeit.timeit('controllerObj.run()', number=2)

controllerObj.run()
