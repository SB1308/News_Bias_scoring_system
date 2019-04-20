from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from ga import *
# from PIL import Image, ImageOps
import datetime
import os.path
import clips
import ast
import time
import constants
from json import loads, dumps
from django.views.decorators.csrf import csrf_exempt

# ------------------------------------------------------------------------------
# Create your views here.


def index(request):
    return render(request, 'd.html')

def b(request):
    return render(request, 'e.html')

def amm(request):
    return render(request, 'amm.html')


# Passes the waypoints back and run GA
@csrf_exempt
def newRoute(request):
    print('newRoute! \n')
    data = request.POST.copy()
    wp = data.get('wayPts')
    result = runGA(wp)

    return redirect('/b?foo='+str(result))

# Passes the waypoints back and run GA
@csrf_exempt
def petrol(request):
    print('petrol! \n')
    creditCard = request.POST['cc']
    try:
        response = clipsChoosePetrolBrand(creditCard)
    except:
        response = ''
    print('brand = '+response)
    constants.petrolBrand = response
    return HttpResponse(response)

# Run Clips to choose the petrol station brand depending on which card it has.
def clipsChoosePetrolBrand(data):
    # Preference
    #data = 'DBS-Esso'
    ccInput = '(form-input ' +\
                 '(Bankcard '+data+'))'
    # CLIPS
    clips.Clear()
    clips.Load(settings.CLIPS_DIR + "/init.clp")
    clips.Load(settings.CLIPS_DIR + "/card_clips.clp")
    clips.Reset()
    clips.Assert(ccInput)
    clips.Run()
    return clips.StdoutStream.Read()

def runGA(wp):
    print('brand = '+constants.petrolBrand)
    brand = constants.petrolBrand
    constants.Loccor = []
    constants.Startloc = []
    constants.Endloc = []
    constants.Petrolcor = []

    constants.start_time = None
    constants.prev_iter_time = None
    constants.prev_gen_time = None

    constants.locList = []
    constants.petrolList = []

    constants.startx = []
    constants.starty = []
    constants.endx = []
    constants.endy = []
    constants.Shortest_Distance = 0

    # Linkloc is a temporary point to connnect the start and end with 0 distance
    constants.Linkloc = []

    constants.final_list = []
    constants.curlist = []

    config = loads(wp)
    input = config[0]
    val = input['latLng'].split(',')
    constants.Startloc.append(float(val[0]))
    constants.Startloc.append(float(val[1]))
    print('Startloc = ' + input['latLng'])

    print('len(config) '+str(len(config)))

    for i in range(1, len(config)-1):
        input = config[i]
        val = input['latLng'].split(',')
        val2 = [float(val[0]),float(val[1])]
        constants.Loccor.append(val2)
        print('i = ' + str(i))

    input = config[len(config)-1]
    val = input['latLng'].split(',')
    constants.Endloc.append(float(val[0]))
    constants.Endloc.append(float(val[1]))
    print('Endloc = ' + input['latLng'])


    #constants.Loccor = [[1.37581623430087, 103.830624122889], [1.42115590658249, 103.848117628541],[1.26430476455787, 103.822308649915]]

    # Startloc is the coordinates of the start point
    #constants.Startloc = [1.33945271661449, 103.70668501289]

    # Endloc is the coordinates of the end point
    #constants.Endloc = [1.31489619639367, 103.764423054189]

    # Petrolcor is the coordinates of the petrol stations - SPC
    constants.Petrolcor1 = [[1.328276, 103.813597], [1.44244103727, 103.776200994], [1.365289, 103.839673], [1.36449, 103.84592],
                          [1.378994, 103.836168], [1.3266884782029, 103.84788192046], [1.3278458229585, 103.93984413714],
                          [1.28408372439, 103.818506849], [1.318023, 103.831998], [1.383397, 103.772767], [1.3185147308667, 103.90876173461],  
						  [1.305726, 103.795075], [1.323107, 103.819387], [1.2884418507336, 103.83815013614], [1.368597016813, 103.88433792135],
                          [1.3146267758284, 103.7146202756], [1.371972, 103.828816], [1.3423035906473, 103.73729182853], [1.297636, 103.838181],
                          [1.3318422790676, 103.88041106101], [1.3020768186352, 103.88435589325], [1.2769678624928, 103.79068634598],
                          [1.3708755393005, 103.96031413222], [1.400355, 103.909162], [1.2913261708666, 103.80089438566], [1.293097, 103.825994], 
						  [1.43999072142, 103.825246311], [1.391207, 103.898967], [1.41003, 103.90099], [1.348636, 103.938567],
                          [1.308243296161, 103.89477060979], [1.27175076934, 103.807202523], [1.3247173754161, 103.84163668491], 
						  [1.3357392758618, 103.85558287997], [1.313866, 103.930981], [1.3583617491309, 103.88286422548], [1.348829, 103.837778],
                          [1.357567, 103.87521], [1.4174586657123, 103.83783562788]]
    # Caltex
    constants.Petrolcor2 = [[1.290536, 103.806638], [1.32677, 103.84507], [1.30373, 103.86583],
                            [1.33525, 103.7868], [1.3163, 103.90013], [1.31471, 103.769], [1.31885, 103.83335], [1.30907, 103.9108],
                           [1.31548, 103.91907], [1.31774, 103.78545], [1.32328, 103.69191], [1.28447, 103.81505], [1.30466, 103.742], 
                           [1.33874, 103.69273], [1.3578, 103.86785], [1.33268, 103.88363], [1.3255, 103.89083], [1.34741, 103.87163], 
                           [1.34941, 103.92845], [1.30749, 103.89565], [1.35569, 103.88072], [1.37094, 103.82823], [1.32498, 103.82693], 
                           [1.40349, 103.81848], [1.42984, 103.829]]
    # Esso
    constants.Petrolcor3 = [[1.31333702966203, 103.688291788335], [1.32513419600353, 103.724455695065], [1.30969711617262, 103.754834106309],
                           [1.35103948153137, 103.723669186664], [1.34522197636818, 103.732766747768], [1.30812643020781, 103.761111327647], 
                           [1.36669080664894, 103.750547929865], [1.37816692983858, 103.737936504206], [1.37759071544749, 103.75021031988], 
                           [1.39529413805329, 103.747316846257], [1.33993485715375, 103.774745224001], [1.33624062033011, 103.784052362459], 
                           [1.3451770241423, 103.773389778832], [1.29125205568181, 103.801092969151], [1.28014695291125, 103.78552999506], 
                           [1.33002302155172, 103.799054384985], [1.3310638096288, 103.798712381925], [1.30695019942495, 103.802462265599], 
                           [1.37695815673441, 103.762572545694], [1.29479330109375, 103.81638766634], [1.28259804485137, 103.821441444977], 
                           [1.31250881313516, 103.796171570295], [1.29264112902212, 103.825616886066], [1.31093436675036, 103.842758072049], 
                           [1.43097003446446, 103.78451978162], [1.33627721077057, 103.84652087842], [1.43425427963372, 103.761927080423], 
                           [1.31626142386249, 103.836939567923], [1.35796716105207, 103.828390025712], [1.3730552650489, 103.828947502264], 
                           [1.31337269054335, 103.861173086447], [1.32873401100801, 103.872220370971], [1.4401988340604, 103.824549249224], 
                           [1.43163469684038, 103.839867501622], [1.44043314468618, 103.825090080646], [1.33233225144634, 103.879000196883], 
                           [1.32433597332174, 103.880715967756], [1.30256134234211, 103.884276248332], [1.31108036207879, 103.883636844169], 
                           [1.3704859187379, 103.828172843262], [1.31422873560528, 103.889105425095], [1.36257285737842, 103.852539960282], 
                           [1.31128678062408, 103.894436406046], [1.35879969213689, 103.884058439841], [1.30837730734643, 103.908009188333], 
                           [1.36248001410832, 103.868157296049], [1.36100845388432, 103.87391992528], [1.31102483053203, 103.920378020705], 
                           [1.37081546766153, 103.864050606108], [1.37080808189673, 103.864064571602], [1.32050255282747, 103.916073376036], 
                           [1.31452985974162, 103.934305854401], [1.32229200544007, 103.932480579897], [1.36320780681881, 103.887975679942], 
                           [1.38515804733144, 103.900520468615], [1.3605756543141, 103.947725887411], [1.37490843711826, 103.940566200869], 
                           [1.35755709161332, 103.959006565688]]
    # Shell
    constants.Petrolcor4 = [[1.33096374121429, 103.79911013825], [1.32336813859506, 103.817337523914], [1.31889313369982, 103.84974693471],
                           [1.311064267582, 103.842228758288], [1.3113429474723, 103.843097934166], [1.31448131375713, 103.857185168034], 
                           [1.32419151051026, 103.842166350087], [1.3677573528469, 103.844724571954], [1.3445835294881, 103.864557902417], 
                           [1.34802835446495, 103.838337837848], [1.369919302961, 103.827910661751], [1.3835621334922, 103.877066495307], 
                           [1.44053034160932, 103.824420690435], [1.36326260646867, 103.867309861394], [1.35124988188239, 103.835408663847], 
                           [1.34108964634274, 103.848900569646], [1.39991025627215, 103.817849976558], [1.44431165485791, 103.790067364842], 
                           [1.41117052943868, 103.756454408364], [1.36078678141973, 103.873990176496], [1.43080205677891, 103.833011168832], 
                           [1.29066996157808, 103.806855076045], [1.37227099840537, 103.76342332201], [1.29752024517664, 103.80333216638], 
                           [1.2898004536272, 103.832437278375], [1.28677750729998, 103.83452296254], [1.28934111083007, 103.803024131521], 
                           [1.28837425312142, 103.81951732881], [1.33863200262167, 103.776811690093], [1.31881147030039, 103.912968727184], 
                           [1.30979958951717, 103.90099804453], [1.30821485693545, 103.909909697653], [1.31198237882228, 103.875582544247], 
                           [1.31056412656593, 103.883811232417], [1.34925376748037, 103.89014412224], [1.33118255886658, 103.877758601196], 
                           [1.36575629784199, 103.967238515642], [1.33178786290627, 103.888830798484], [1.32170762851012, 103.891660315436], 
                           [1.4045657500855, 103.906643154864], [1.39153102596969, 103.892660441487], [1.31256586519379, 103.926550406504], 
                           [1.33086144381, 103.947588153704], [1.3492287633002, 103.947704385806], [1.31093807363241, 103.894475257291], 
                           [1.34395983553428, 103.707788246958], [1.34762672421064, 103.764888536147], [1.35022742637168, 103.738433107817], 
                           [1.38560552565511, 103.746481830809], [1.32353941367612, 103.721771262524], [1.35008666551121, 103.701213561875], 
                           [1.438325338316, 103.775415745085], [1.27747832544973, 103.789682515263], [1.28926117294813, 103.777844345902]]
	
    # All
    constants.Petrolcor5 = [[1.328276, 103.813597], [1.44244103727, 103.776200994], [1.365289, 103.839673], [1.36449, 103.84592],
                           [1.378994, 103.836168], [1.3266884782029, 103.84788192046], [1.3278458229585, 103.93984413714],
                           [1.28408372439, 103.818506849], [1.318023, 103.831998], [1.383397, 103.772767], [1.3185147308667, 103.90876173461],  
						   [1.305726, 103.795075], [1.323107, 103.819387], [1.2884418507336, 103.83815013614], [1.368597016813, 103.88433792135],
                           [1.3146267758284, 103.7146202756], [1.371972, 103.828816], [1.3423035906473, 103.73729182853], [1.297636, 103.838181],
                           [1.3318422790676, 103.88041106101], [1.3020768186352, 103.88435589325], [1.2769678624928, 103.79068634598],
                           [1.3708755393005, 103.96031413222], [1.400355, 103.909162], [1.2913261708666, 103.80089438566], [1.293097, 103.825994], 
						   [1.43999072142, 103.825246311], [1.391207, 103.898967], [1.41003, 103.90099], [1.348636, 103.938567],
                           [1.308243296161, 103.89477060979], [1.27175076934, 103.807202523], [1.3247173754161, 103.84163668491], 
						   [1.3357392758618, 103.85558287997], [1.313866, 103.930981], [1.3583617491309, 103.88286422548], [1.348829, 103.837778],
                           [1.357567, 103.87521], [1.4174586657123, 103.83783562788],
                           [1.290536, 103.806638], [1.32677, 103.84507], [1.30373, 103.86583], 
                           [1.33525, 103.7868], [1.3163, 103.90013], [1.31471, 103.769], [1.31885, 103.83335], [1.30907, 103.9108], 
                           [1.31548, 103.91907], [1.31774, 103.78545], [1.32328, 103.69191], [1.28447, 103.81505], [1.30466, 103.742], 
                           [1.33874, 103.69273], [1.3578, 103.86785], [1.33268, 103.88363], [1.3255, 103.89083], [1.34741, 103.87163], 
                           [1.34941, 103.92845], [1.30749, 103.89565], [1.35569, 103.88072], [1.37094, 103.82823], [1.32498, 103.82693], 
                           [1.40349, 103.81848], [1.42984, 103.829],
	                       [1.31333702966203, 103.688291788335], [1.32513419600353, 103.724455695065], [1.30969711617262, 103.754834106309], 
                           [1.35103948153137, 103.723669186664], [1.34522197636818, 103.732766747768], [1.30812643020781, 103.761111327647], 
                           [1.36669080664894, 103.750547929865], [1.37816692983858, 103.737936504206], [1.37759071544749, 103.75021031988], 
                           [1.39529413805329, 103.747316846257], [1.33993485715375, 103.774745224001], [1.33624062033011, 103.784052362459], 
                           [1.3451770241423, 103.773389778832], [1.29125205568181, 103.801092969151], [1.28014695291125, 103.78552999506], 
                           [1.33002302155172, 103.799054384985], [1.3310638096288, 103.798712381925], [1.30695019942495, 103.802462265599], 
                           [1.37695815673441, 103.762572545694], [1.29479330109375, 103.81638766634], [1.28259804485137, 103.821441444977], 
                           [1.31250881313516, 103.796171570295], [1.29264112902212, 103.825616886066], [1.31093436675036, 103.842758072049], 
                           [1.43097003446446, 103.78451978162], [1.33627721077057, 103.84652087842], [1.43425427963372, 103.761927080423], 
                           [1.31626142386249, 103.836939567923], [1.35796716105207, 103.828390025712], [1.3730552650489, 103.828947502264], 
                           [1.31337269054335, 103.861173086447], [1.32873401100801, 103.872220370971], [1.4401988340604, 103.824549249224], 
                           [1.43163469684038, 103.839867501622], [1.44043314468618, 103.825090080646], [1.33233225144634, 103.879000196883], 
                           [1.32433597332174, 103.880715967756], [1.30256134234211, 103.884276248332], [1.31108036207879, 103.883636844169], 
                           [1.3704859187379, 103.828172843262], [1.31422873560528, 103.889105425095], [1.36257285737842, 103.852539960282], 
                           [1.31128678062408, 103.894436406046], [1.35879969213689, 103.884058439841], [1.30837730734643, 103.908009188333], 
                           [1.36248001410832, 103.868157296049], [1.36100845388432, 103.87391992528], [1.31102483053203, 103.920378020705], 
                           [1.37081546766153, 103.864050606108], [1.37080808189673, 103.864064571602], [1.32050255282747, 103.916073376036], 
                           [1.31452985974162, 103.934305854401], [1.32229200544007, 103.932480579897], [1.36320780681881, 103.887975679942], 
                           [1.38515804733144, 103.900520468615], [1.3605756543141, 103.947725887411], [1.37490843711826, 103.940566200869], 
                           [1.35755709161332, 103.959006565688],			   
	                       [1.33096374121429, 103.79911013825], [1.32336813859506, 103.817337523914], [1.31889313369982, 103.84974693471], 
                           [1.311064267582, 103.842228758288], [1.3113429474723, 103.843097934166], [1.31448131375713, 103.857185168034], 
                           [1.32419151051026, 103.842166350087], [1.3677573528469, 103.844724571954], [1.3445835294881, 103.864557902417], 
                           [1.34802835446495, 103.838337837848], [1.369919302961, 103.827910661751], [1.3835621334922, 103.877066495307], 
                           [1.44053034160932, 103.824420690435], [1.36326260646867, 103.867309861394], [1.35124988188239, 103.835408663847], 
                           [1.34108964634274, 103.848900569646], [1.39991025627215, 103.817849976558], [1.44431165485791, 103.790067364842], 
                           [1.41117052943868, 103.756454408364], [1.36078678141973, 103.873990176496], [1.43080205677891, 103.833011168832], 
                           [1.29066996157808, 103.806855076045], [1.37227099840537, 103.76342332201], [1.29752024517664, 103.80333216638], 
                           [1.2898004536272, 103.832437278375], [1.28677750729998, 103.83452296254], [1.28934111083007, 103.803024131521], 
                           [1.28837425312142, 103.81951732881], [1.33863200262167, 103.776811690093], [1.31881147030039, 103.912968727184], 
                           [1.30979958951717, 103.90099804453], [1.30821485693545, 103.909909697653], [1.31198237882228, 103.875582544247], 
                           [1.31056412656593, 103.883811232417], [1.34925376748037, 103.89014412224], [1.33118255886658, 103.877758601196], 
                           [1.36575629784199, 103.967238515642], [1.33178786290627, 103.888830798484], [1.32170762851012, 103.891660315436], 
                           [1.4045657500855, 103.906643154864], [1.39153102596969, 103.892660441487], [1.31256586519379, 103.926550406504], 
                           [1.33086144381, 103.947588153704], [1.3492287633002, 103.947704385806], [1.31093807363241, 103.894475257291], 
                           [1.34395983553428, 103.707788246958], [1.34762672421064, 103.764888536147], [1.35022742637168, 103.738433107817], 
                           [1.38560552565511, 103.746481830809], [1.32353941367612, 103.721771262524], [1.35008666551121, 103.701213561875], 
                           [1.438325338316, 103.775415745085], [1.27747832544973, 103.789682515263], [1.28926117294813, 103.777844345902]]
	
    constants.startx = constants.Startloc[0]
    constants.starty = constants.Startloc[1]
    constants.endx = constants.Endloc[0]
    constants.endy = constants.Endloc[1]

    constants.Linkloc = [10000, 10000]

    constants.start_time = time.time()

    #constants.Petrolcor = constants.Petrolcor1

    if brand == 'SPC':
        constants.Petrolcor = constants.Petrolcor1
    elif brand == 'Caltex':
        constants.Petrolcor = constants.Petrolcor2
    elif brand == 'Esso':
        constants.Petrolcor = constants.Petrolcor3
    elif brand == 'Shell':
        constants.Petrolcor = constants.Petrolcor4
    else :
        constants.Petrolcor = constants.Petrolcor5

    for i in range(0, len(constants.Loccor)):
        constants.locList.append(Loc(x=constants.Loccor[i][0], y=constants.Loccor[i][1]))
    constants.locList.append(Loc(x=constants.Startloc[0], y=constants.Startloc[1]))
    constants.locList.append(Loc(x=constants.Endloc[0], y=constants.Endloc[1]))
    constants.locList.append(Loc(x=constants.Linkloc[0], y=constants.Linkloc[1]))

    constants.assign_time = time.time()
    constants.prev_iter_time = constants.assign_time
    constants.prev_gen_time = constants.assign_time

    for i in range(0, len(constants.Petrolcor)):

        curlist = constants.locList[:]
        curlist.append(Loc(x=constants.Petrolcor[i][0], y=constants.Petrolcor[i][1]))
        popSize = 40
        eliteSize = 10
        mutationRate = 0.01
        generations = 10
        population = curlist
        pop = initialPopulation(popSize, population)

        for j in range(0, generations):
            #        print ("petrol station " + str (i) + " Generation " + str(j) + " processing")
            pop = nextGeneration(pop, eliteSize, mutationRate)
            gen_time = time.time()
            #        print ("time required to process generation " + str(j) +  " is  " + str(gen_time-prev_gen_time))
            prev_gen_time = gen_time
        curlist = []
        Shortest_distance1 = 1 / rankRoutes(pop)[0][1]
        bestRouteIndex1 = rankRoutes(pop)[0][0]
        bestRoute1 = pop[bestRouteIndex1]
        #Shortest_distance2 = 1 / rankRoutes(pop)[1][1]
        #bestRouteIndex2 = rankRoutes(pop)[1][0]
        #bestRoute2 = pop[bestRouteIndex2]
        #Shortest_distance3 = 1 / rankRoutes(pop)[2][1]
        #bestRouteIndex3 = rankRoutes(pop)[2][0]
        #bestRoute3 = pop[bestRouteIndex3]
        rank_time = time.time()
        #    print ("ranking time for the top 3 routes is " + str (rank_time-prev_gen_time))
        constants.final_list.append((Shortest_distance1, bestRoute1))
        #constants.final_list.append((Shortest_distance2, bestRoute2))
        #constants.final_list.append((Shortest_distance3, bestRoute3))
        iter_time = time.time()
        #    print ("petrol station " + str (i) + "done")
        #    print ("time required to process petrol station " + str(i) +  " is  " + str(iter_time-prev_iter_time))
        prev_iter_time = iter_time

    # In[499]:

    # sorted_list is the final sorted list of the top 3 routes for each petrol pump. So if there are 10 petrol pumps
    # sorted_list would have 10 x 3 lists. sorted_list [k][1] is the k-th ranked list
    process_time = time.time()
    sorted_list = sorted(constants.final_list, key=lambda x: x[0], reverse=False)

    # In[500]:

    #list = [0, 3, 6]
    list = [0]
    num = 1
    for i in list:
        print (" The length of rank " + str(num) + " is " + str(sorted_list[i][0]))
        print (" The route of rank : " + str(num) + " is ")
        srt = []
        srt = clean_list(sorted_list[i][1])
        result = ""
        for j in range(0, len(srt)):
            print ("xcor  is " + str(srt[j].x) + " and ycor is " + str(srt[j].y))
            result += "{\"x\":\""+str(srt[j].x)+"\",\"y\":\""+str(srt[j].y)+"\"},"
        num = num + 1

    result = "["+result[0:len(result)-1]+"]"

    sort_time = time.time()

    # In[501]:

    print("run time is " + str(sort_time - constants.start_time))
    return result


