#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
|----------------------------------------------------------|
|             ,--|--.                                      |
|          ,-'       `-.                                   |
|        ,'      |      `.                                 |
|      ,'                 `.                               |
|     /          |          \                              |
|    /                       \                           / |
|- - - - - - - - + - - - - - -\- - - - - - - - - - - - -/- |
|                              \                       /   |
|                |              \                     /    |
|                                `.                 ,'     |
|                |                 `.             ,'       |
|                                    `-.       ,-'         |
|                |                      `--,--'            |
|----------------------------------------------------------|
"""


from matplotlib.figure import Figure
try:
    from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
except ImportError:
    try:
        from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
    except ImportError:
        raise Exception('Unable to start application as none of the matplotlib backends could be '
                        'imported')

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from multiprocessing import Pipe


class Plot(Gtk.Box):

    graph_properties = {
        'linestyle': '-',
        'marker': '',
    }

    def __init__(self, size=(800, 400)):
        self.size = size
        Gtk.Box.__init__(self)

        fig = Figure()

        self.ax = fig.add_subplot(111, fc='black')

        self.ax.grid(True, 'both', 'both')

        canvas = FigureCanvas(fig)
        canvas.set_size_request(*size)
        self.add(canvas)

        parent_conn, self.child_conn = Pipe(duplex=False)  # Pipe to pump the label data through

        def update_self(source, condition):
            """
            watches pipe and when data changes, changes the label
            """
            assert parent_conn.poll()
            i = parent_conn.recv()
            print('recived', i)
            self.ax.clear()
            self.ax.grid(True, 'both', 'both')
            print(self.ax.plot(i, **self.graph_properties))
            self.queue_draw()
            return True

        GObject.io_add_watch(parent_conn.fileno(), GObject.IO_IN, update_self)

    # TODO z plotu odebrat popisky (asi)

    def update(self, values):
        # type: (tuple) -> None
        """
        renews plotted values
        when all values are
        """
        self.child_conn.send(values)


if __name__ == '__main__':
    from TestUtil import test_util

    p = Plot()

    def t1(*_, **__):
        print('t1')
        x = [0.0, 0.012271538285719925, 0.024541228522912288, 0.03680722294135883, 0.049067674327418015, 0.06132073630220858, 0.07356456359966743, 0.0857973123444399, 0.0980171403295606, 0.11022220729388306, 0.1224106751992162, 0.13458070850712617, 0.14673047445536175, 0.15885814333386145, 0.17096188876030122, 0.18303988795514095, 0.19509032201612825, 0.20711137619221856, 0.2191012401568698, 0.2310581082806711, 0.24298017990326387, 0.25486565960451457, 0.26671275747489837, 0.27851968938505306, 0.29028467725446233, 0.3020059493192281, 0.3136817403988915, 0.3253102921622629, 0.33688985339222005, 0.34841868024943456, 0.3598950365349881, 0.37131719395183754, 0.3826834323650898, 0.3939920400610481, 0.40524131400498986, 0.41642956009763715, 0.4275550934302821, 0.43861623853852766, 0.44961132965460654, 0.46053871095824, 0.47139673682599764, 0.4821837720791227, 0.49289819222978404, 0.5035383837257176, 0.5141027441932217, 0.524589682678469, 0.5349976198870972, 0.5453249884220465, 0.5555702330196022, 0.5657318107836131, 0.5758081914178453, 0.5857978574564389, 0.5956993044924334, 0.6055110414043255, 0.6152315905806268, 0.6248594881423863, 0.6343932841636455, 0.6438315428897914, 0.6531728429537768, 0.6624157775901718, 0.6715589548470183, 0.680600997795453, 0.6895405447370668, 0.6983762494089729, 0.7071067811865475, 0.7157308252838186, 0.7242470829514669, 0.7326542716724128, 0.7409511253549591, 0.7491363945234593, 0.7572088465064845, 0.765167265622459, 0.773010453362737, 0.7807372285720944, 0.7883464276266062, 0.7958369046088835, 0.8032075314806448, 0.8104571982525948, 0.8175848131515837, 0.8245893027850253, 0.8314696123025452, 0.838224705554838, 0.844853565249707, 0.8513551931052652, 0.8577286100002721, 0.8639728561215867, 0.8700869911087113, 0.8760700941954066, 0.8819212643483549, 0.8876396204028539, 0.8932243011955153, 0.8986744656939538, 0.9039892931234433, 0.9091679830905223, 0.9142097557035307, 0.9191138516900578, 0.9238795325112867, 0.9285060804732155, 0.9329927988347388, 0.937339011912575, 0.9415440651830208, 0.9456073253805213, 0.9495281805930367, 0.9533060403541938, 0.9569403357322089, 0.9604305194155658, 0.9637760657954398, 0.9669764710448521, 0.970031253194544, 0.9729399522055601, 0.9757021300385286, 0.9783173707196277, 0.9807852804032304, 0.9831054874312163, 0.9852776423889412, 0.9873014181578584, 0.989176509964781, 0.99090263542778, 0.99247953459871, 0.9939069700023561, 0.9951847266721968, 0.996312612182778, 0.9972904566786902, 0.9981181129001492, 0.9987954562051724, 0.9993223845883495, 0.9996988186962042, 0.9999247018391445, 1.0, 0.9999247018391445, 0.9996988186962042, 0.9993223845883495, 0.9987954562051724, 0.9981181129001492, 0.9972904566786902, 0.996312612182778, 0.9951847266721969, 0.9939069700023561, 0.99247953459871, 0.99090263542778, 0.989176509964781, 0.9873014181578584, 0.9852776423889412, 0.9831054874312163, 0.9807852804032304, 0.9783173707196277, 0.9757021300385286, 0.9729399522055602, 0.970031253194544, 0.9669764710448521, 0.9637760657954398, 0.9604305194155659, 0.9569403357322089, 0.9533060403541939, 0.9495281805930367, 0.9456073253805214, 0.9415440651830208, 0.937339011912575, 0.9329927988347388, 0.9285060804732156, 0.9238795325112867, 0.9191138516900578, 0.9142097557035307, 0.9091679830905225, 0.9039892931234434, 0.8986744656939539, 0.8932243011955152, 0.8876396204028539, 0.881921264348355, 0.8760700941954066, 0.8700869911087115, 0.8639728561215868, 0.8577286100002721, 0.8513551931052652, 0.8448535652497072, 0.8382247055548382, 0.8314696123025455, 0.8245893027850252, 0.8175848131515837, 0.8104571982525948, 0.8032075314806449, 0.7958369046088836, 0.7883464276266063, 0.7807372285720946, 0.7730104533627371, 0.7651672656224591, 0.7572088465064847, 0.7491363945234593, 0.740951125354959, 0.7326542716724128, 0.7242470829514669, 0.7157308252838187, 0.7071067811865476, 0.6983762494089729, 0.689540544737067, 0.6806009977954532, 0.6715589548470186, 0.662415777590172, 0.6531728429537766, 0.6438315428897914, 0.6343932841636455, 0.6248594881423863, 0.6152315905806269, 0.6055110414043257, 0.5956993044924335, 0.585797857456439, 0.5758081914178454, 0.5657318107836135, 0.5555702330196022, 0.5453249884220464, 0.5349976198870972, 0.524589682678469, 0.5141027441932218, 0.5035383837257177, 0.49289819222978415, 0.4821837720791229, 0.47139673682599786, 0.4605387109582402, 0.4496113296546069, 0.43861623853852755, 0.42755509343028203, 0.41642956009763715, 0.4052413140049899, 0.39399204006104815, 0.3826834323650899, 0.3713171939518377, 0.35989503653498833, 0.3484186802494348, 0.33688985339222033, 0.32531029216226326, 0.3136817403988914, 0.30200594931922803, 0.2902846772544624, 0.27851968938505317, 0.2667127574748985, 0.2548656596045147, 0.24298017990326407, 0.23105810828067133, 0.21910124015687005, 0.20711137619221884, 0.1950903220161286, 0.1830398879551409, 0.17096188876030122, 0.15885814333386147, 0.1467304744553618, 0.13458070850712628, 0.12241067519921635, 0.11022220729388324, 0.09801714032956083, 0.08579731234444016, 0.07356456359966773, 0.06132073630220849, 0.049067674327417966, 0.03680722294135883, 0.024541228522912326, 0.012271538285720007, 1.2246467991473532e-16, -0.012271538285719762, -0.02454122852291208, -0.03680722294135858, -0.049067674327417724, -0.061320736302208245, -0.0735645635996675, -0.08579731234443992, -0.09801714032956059, -0.110222207293883, -0.1224106751992161, -0.13458070850712606, -0.14673047445536158, -0.15885814333386122, -0.17096188876030097, -0.18303988795514065, -0.19509032201612836, -0.2071113761922186, -0.2191012401568698, -0.23105810828067108, -0.24298017990326382, -0.25486565960451446, -0.26671275747489825, -0.2785196893850529, -0.2902846772544621, -0.3020059493192278, -0.3136817403988912, -0.325310292162263, -0.3368898533922201, -0.34841868024943456, -0.3598950365349881, -0.37131719395183743, -0.38268343236508967, -0.39399204006104793, -0.4052413140049897, -0.41642956009763693, -0.4275550934302818, -0.4386162385385273, -0.44961132965460665, -0.46053871095824006, -0.47139673682599764, -0.48218377207912266, -0.4928981922297839, -0.5035383837257175, -0.5141027441932216, -0.5245896826784687, -0.5349976198870969, -0.5453249884220461, -0.555570233019602, -0.5657318107836132, -0.5758081914178453, -0.5857978574564389, -0.5956993044924332, -0.6055110414043254, -0.6152315905806267, -0.6248594881423862, -0.6343932841636453, -0.6438315428897913, -0.6531728429537765, -0.6624157775901718, -0.6715589548470184, -0.680600997795453, -0.6895405447370668, -0.6983762494089728, -0.7071067811865475, -0.7157308252838185, -0.7242470829514668, -0.7326542716724126, -0.7409511253549589, -0.749136394523459, -0.7572088465064842, -0.765167265622459, -0.7730104533627367, -0.7807372285720944, -0.7883464276266059, -0.7958369046088835, -0.803207531480645, -0.8104571982525947, -0.8175848131515838, -0.8245893027850251, -0.8314696123025452, -0.8382247055548379, -0.844853565249707, -0.8513551931052649, -0.857728610000272, -0.8639728561215865, -0.8700869911087113, -0.8760700941954067, -0.8819212643483549, -0.887639620402854, -0.8932243011955152, -0.8986744656939538, -0.9039892931234431, -0.9091679830905224, -0.9142097557035305, -0.9191138516900577, -0.9238795325112865, -0.9285060804732155, -0.932992798834739, -0.9373390119125748, -0.9415440651830208, -0.9456073253805212, -0.9495281805930367, -0.9533060403541938, -0.9569403357322088, -0.9604305194155657, -0.9637760657954398, -0.9669764710448522, -0.970031253194544, -0.9729399522055602, -0.9757021300385285, -0.9783173707196277, -0.9807852804032303, -0.9831054874312163, -0.9852776423889411, -0.9873014181578583, -0.9891765099647809, -0.99090263542778, -0.9924795345987101, -0.9939069700023561, -0.9951847266721969, -0.996312612182778, -0.9972904566786902, -0.9981181129001492, -0.9987954562051724, -0.9993223845883494, -0.9996988186962042, -0.9999247018391445, -1.0, -0.9999247018391445, -0.9996988186962042, -0.9993223845883495, -0.9987954562051724, -0.9981181129001492, -0.9972904566786902, -0.996312612182778, -0.9951847266721969, -0.9939069700023561, -0.9924795345987101, -0.99090263542778, -0.9891765099647809, -0.9873014181578584, -0.9852776423889412, -0.9831054874312164, -0.9807852804032304, -0.9783173707196278, -0.9757021300385286, -0.9729399522055603, -0.970031253194544, -0.9669764710448523, -0.96377606579544, -0.9604305194155658, -0.9569403357322089, -0.9533060403541939, -0.9495281805930368, -0.9456073253805213, -0.9415440651830209, -0.937339011912575, -0.9329927988347391, -0.9285060804732156, -0.9238795325112866, -0.9191138516900579, -0.9142097557035306, -0.9091679830905225, -0.9039892931234433, -0.898674465693954, -0.8932243011955153, -0.8876396204028542, -0.881921264348355, -0.8760700941954069, -0.8700869911087115, -0.8639728561215866, -0.8577286100002722, -0.8513551931052651, -0.8448535652497072, -0.838224705554838, -0.8314696123025455, -0.8245893027850253, -0.817584813151584, -0.8104571982525949, -0.8032075314806453, -0.7958369046088837, -0.7883464276266061, -0.7807372285720946, -0.7730104533627369, -0.7651672656224592, -0.7572088465064846, -0.7491363945234596, -0.7409511253549591, -0.7326542716724131, -0.724247082951467, -0.715730825283819, -0.7071067811865477, -0.6983762494089727, -0.6895405447370672, -0.680600997795453, -0.6715589548470187, -0.6624157775901718, -0.6531728429537771, -0.6438315428897915, -0.6343932841636459, -0.6248594881423865, -0.6152315905806274, -0.6055110414043257, -0.5956993044924332, -0.5857978574564391, -0.5758081914178452, -0.5657318107836136, -0.5555702330196022, -0.5453249884220468, -0.5349976198870973, -0.5245896826784694, -0.5141027441932219, -0.5035383837257181, -0.49289819222978426, -0.4821837720791226, -0.4713967368259979, -0.46053871095823995, -0.449611329654607, -0.43861623853852766, -0.42755509343028253, -0.41642956009763726, -0.4052413140049904, -0.39399204006104827, -0.3826834323650904, -0.3713171939518378, -0.359895036534988, -0.3484186802494349, -0.33688985339222, -0.32531029216226337, -0.3136817403988915, -0.3020059493192286, -0.2902846772544625, -0.27851968938505367, -0.2667127574748986, -0.2548656596045144, -0.24298017990326418, -0.231058108280671, -0.21910124015687016, -0.20711137619221853, -0.19509032201612872, -0.183039887955141, -0.17096188876030177, -0.15885814333386158, -0.1467304744553624, -0.13458070850712642, -0.12241067519921603, -0.11022220729388336, -0.0980171403295605, -0.08579731234444028, -0.07356456359966741, -0.06132073630220906, -0.04906767432741809, -0.036807222941359394, -0.024541228522912448, -0.012271538285720572, -2.4492935982947064e-16, 0.012271538285720083, 0.02454122852291196, 0.03680722294135891, 0.0490676743274176, 0.061320736302208564, 0.07356456359966693, 0.0857973123444398, 0.09801714032956002, 0.11022220729388288, 0.12241067519921554, 0.13458070850712592, 0.1467304744553619, 0.15885814333386108, 0.17096188876030127, 0.18303988795514053, 0.19509032201612825, 0.20711137619221803, 0.2191012401568697, 0.23105810828067053, 0.2429801799032637, 0.2548656596045139, 0.2667127574748981, 0.2785196893850532, 0.290284677254462, 0.3020059493192281, 0.3136817403988911, 0.32531029216226287, 0.33688985339221955, 0.34841868024943445, 0.35989503653498756, 0.3713171939518373, 0.38268343236508995, 0.3939920400610478, 0.40524131400498997, 0.4164295600976368, 0.4275550934302821, 0.4386162385385272, 0.44961132965460654, 0.4605387109582395, 0.47139673682599753, 0.48218377207912216, 0.4928981922297838, 0.5035383837257177, 0.5141027441932214, 0.524589682678469, 0.5349976198870968, 0.5453249884220465, 0.5555702330196018, 0.5657318107836131, 0.5758081914178448, 0.5857978574564388, 0.5956993044924328, 0.6055110414043253, 0.6152315905806269, 0.6248594881423861, 0.6343932841636456, 0.6438315428897912, 0.6531728429537768, 0.6624157775901713, 0.6715589548470183, 0.6806009977954526, 0.6895405447370668, 0.6983762494089724, 0.7071067811865474, 0.7157308252838187, 0.7242470829514667, 0.7326542716724128, 0.7409511253549588, 0.7491363945234593, 0.7572088465064842, 0.7651672656224588, 0.7730104533627365, 0.7807372285720944, 0.7883464276266058, 0.7958369046088833, 0.8032075314806449, 0.8104571982525945, 0.8175848131515837, 0.824589302785025, 0.8314696123025452, 0.8382247055548377, 0.844853565249707, 0.8513551931052649, 0.857728610000272, 0.8639728561215864, 0.8700869911087112, 0.8760700941954066, 0.8819212643483548, 0.8876396204028539, 0.8932243011955151, 0.8986744656939538, 0.9039892931234431, 0.9091679830905223, 0.9142097557035304, 0.9191138516900577, 0.9238795325112865, 0.9285060804732155, 0.932992798834739, 0.9373390119125747, 0.9415440651830208, 0.9456073253805212, 0.9495281805930367, 0.9533060403541936, 0.9569403357322088, 0.9604305194155657, 0.9637760657954398, 0.9669764710448522, 0.9700312531945439, 0.9729399522055602, 0.9757021300385285, 0.9783173707196277, 0.9807852804032303, 0.9831054874312163, 0.9852776423889411, 0.9873014181578583, 0.9891765099647809, 0.99090263542778, 0.99247953459871, 0.993906970002356, 0.9951847266721969, 0.996312612182778, 0.9972904566786902, 0.9981181129001492, 0.9987954562051724, 0.9993223845883494, 0.9996988186962042, 0.9999247018391445, 1.0, 0.9999247018391445, 0.9996988186962042, 0.9993223845883495, 0.9987954562051724, 0.9981181129001492, 0.9972904566786902, 0.996312612182778, 0.9951847266721969, 0.9939069700023561, 0.9924795345987101, 0.9909026354277801, 0.9891765099647811, 0.9873014181578583, 0.9852776423889412, 0.9831054874312164, 0.9807852804032307, 0.9783173707196275, 0.9757021300385286, 0.9729399522055603, 0.9700312531945443, 0.9669764710448521, 0.96377606579544, 0.960430519415566, 0.9569403357322087, 0.9533060403541939, 0.9495281805930368, 0.9456073253805216, 0.9415440651830207, 0.937339011912575, 0.9329927988347392, 0.928506080473216, 0.9238795325112867, 0.9191138516900579, 0.914209755703531, 0.9091679830905222, 0.9039892931234433, 0.898674465693954, 0.8932243011955158, 0.8876396204028538, 0.8819212643483552, 0.8760700941954069, 0.870086991108712, 0.8639728561215867, 0.8577286100002722, 0.8513551931052656, 0.8448535652497069, 0.8382247055548381, 0.8314696123025456, 0.8245893027850258, 0.8175848131515836, 0.8104571982525949, 0.8032075314806454, 0.7958369046088842, 0.7883464276266062, 0.7807372285720947, 0.7730104533627375, 0.7651672656224586, 0.7572088465064846, 0.7491363945234597, 0.7409511253549598, 0.7326542716724127, 0.7242470829514671, 0.7157308252838191, 0.7071067811865483, 0.6983762494089728, 0.6895405447370673, 0.6806009977954537, 0.6715589548470181, 0.6624157775901718, 0.6531728429537772, 0.6438315428897923, 0.6343932841636454, 0.6248594881423866, 0.6152315905806275, 0.6055110414043251, 0.5956993044924334, 0.5857978574564392, 0.575808191417846, 0.5657318107836129, 0.5555702330196023, 0.5453249884220469, 0.5349976198870982, 0.5245896826784687, 0.514102744193222, 0.5035383837257182, 0.4928981922297836, 0.4821837720791227, 0.47139673682599803, 0.46053871095824084, 0.4496113296546063, 0.43861623853852777, 0.42755509343028264, 0.4164295600976382, 0.4052413140049897, 0.3939920400610484, 0.3826834323650905, 0.3713171939518371, 0.35989503653498817, 0.348418680249435, 0.33688985339222094, 0.32531029216226265, 0.31368174039889163, 0.3020059493192287, 0.29028467725446344, 0.27851968938505295, 0.2667127574748987, 0.25486565960451535, 0.24298017990326343, 0.23105810828067114, 0.21910124015687027, 0.2071113761922195, 0.19509032201612797, 0.18303988795514115, 0.17096188876030188, 0.15885814333386258, 0.1467304744553616, 0.13458070850712653, 0.12241067519921703, 0.1102222072938826, 0.09801714032956063, 0.08579731234444041, 0.07356456359966843, 0.061320736302208294, 0.049067674327418216, 0.03680722294135952, 0.024541228522913457, 0.012271538285719807, 3.6739403974420594e-16, -0.012271538285719072, -0.024541228522912725, -0.03680722294135878, -0.04906767432741748, -0.06132073630220756, -0.07356456359966769, -0.08579731234443967, -0.0980171403295599, -0.11022220729388188, -0.12241067519921629, -0.1345807085071258, -0.1467304744553609, -0.15885814333386186, -0.17096188876030116, -0.18303988795514042, -0.19509032201612725, -0.20711137619221878, -0.21910124015686958, -0.23105810828067042, -0.2429801799032627, -0.2548656596045146, -0.266712757474898, -0.2785196893850522, -0.2902846772544628, -0.302005949319228, -0.3136817403988909, -0.3253102921622619, -0.3368898533922203, -0.34841868024943434, -0.35989503653498744, -0.3713171939518364, -0.38268343236508984, -0.3939920400610477, -0.40524131400498903, -0.41642956009763754, -0.427555093430282, -0.4386162385385271, -0.44961132965460565, -0.4605387109582402, -0.4713967368259974, -0.4821837720791221, -0.4928981922297829, -0.5035383837257176, -0.5141027441932213, -0.5245896826784681, -0.5349976198870975, -0.5453249884220464, -0.5555702330196017, -0.5657318107836123, -0.5758081914178454, -0.5857978574564386, -0.5956993044924327, -0.6055110414043245, -0.6152315905806268, -0.624859488142386, -0.6343932841636447, -0.6438315428897917, -0.6531728429537766, -0.6624157775901713, -0.6715589548470176, -0.6806009977954531, -0.6895405447370667, -0.6983762494089722, -0.7071067811865479, -0.7157308252838187, -0.7242470829514666, -0.7326542716724121, -0.7409511253549593, -0.7491363945234593, -0.7572088465064841, -0.7651672656224582, -0.7730104533627371, -0.7807372285720943, -0.7883464276266058, -0.7958369046088838, -0.8032075314806449, -0.8104571982525945, -0.8175848131515832, -0.8245893027850254, -0.8314696123025451, -0.8382247055548376, -0.8448535652497065, -0.8513551931052652, -0.8577286100002719, -0.8639728561215864, -0.8700869911087117, -0.8760700941954066, -0.8819212643483548, -0.8876396204028535, -0.8932243011955154, -0.8986744656939537, -0.903989293123443, -0.9091679830905219, -0.9142097557035307, -0.9191138516900575, -0.9238795325112864, -0.9285060804732157, -0.9329927988347388, -0.9373390119125747, -0.9415440651830205, -0.9456073253805214, -0.9495281805930366, -0.9533060403541936, -0.9569403357322085, -0.9604305194155658, -0.9637760657954397, -0.9669764710448518, -0.9700312531945441, -0.9729399522055602, -0.9757021300385285, -0.9783173707196274, -0.9807852804032305, -0.9831054874312163, -0.9852776423889411, -0.9873014181578582, -0.989176509964781, -0.99090263542778, -0.9924795345987099, -0.9939069700023561, -0.9951847266721969, -0.996312612182778, -0.9972904566786901, -0.9981181129001492, -0.9987954562051724, -0.9993223845883494, -0.9996988186962041, -0.9999247018391445, -1.0, -0.9999247018391445, -0.9996988186962042, -0.9993223845883495, -0.9987954562051724, -0.9981181129001493, -0.9972904566786902, -0.996312612182778, -0.9951847266721969, -0.9939069700023562, -0.99247953459871, -0.9909026354277801, -0.9891765099647811, -0.9873014181578583, -0.9852776423889412, -0.9831054874312164, -0.9807852804032307, -0.9783173707196275, -0.9757021300385286, -0.9729399522055603, -0.9700312531945443, -0.9669764710448521, -0.96377606579544, -0.9604305194155661, -0.9569403357322087, -0.9533060403541939, -0.9495281805930369, -0.9456073253805217, -0.9415440651830207, -0.9373390119125751, -0.9329927988347392, -0.928506080473216, -0.9238795325112867, -0.9191138516900579, -0.914209755703531, -0.9091679830905223, -0.9039892931234434, -0.8986744656939541, -0.8932243011955159, -0.8876396204028538, -0.8819212643483552, -0.876070094195407, -0.870086991108712, -0.8639728561215867, -0.8577286100002723, -0.8513551931052656, -0.8448535652497069, -0.8382247055548382, -0.8314696123025456, -0.824589302785026, -0.8175848131515836, -0.810457198252595, -0.8032075314806454, -0.7958369046088843, -0.7883464276266063, -0.7807372285720948, -0.7730104533627375, -0.7651672656224587, -0.7572088465064847, -0.7491363945234598, -0.7409511253549599, -0.7326542716724127, -0.7242470829514672, -0.7157308252838193, -0.7071067811865485, -0.6983762494089729, -0.6895405447370673, -0.6806009977954538, -0.6715589548470182, -0.6624157775901719, -0.6531728429537773, -0.6438315428897924, -0.6343932841636454, -0.6248594881423867, -0.6152315905806275, -0.6055110414043252, -0.5956993044924334, -0.5857978574564393, -0.5758081914178461, -0.565731810783613, -0.5555702330196024, -0.545324988422047, -0.5349976198870983, -0.5245896826784688, -0.5141027441932221, -0.5035383837257184, -0.4928981922297837, -0.48218377207912283, -0.47139673682599814, -0.46053871095824095, -0.44961132965460643, -0.4386162385385279, -0.42755509343028275, -0.4164295600976383, -0.4052413140049898, -0.3939920400610485, -0.3826834323650906, -0.3713171939518372, -0.3598950365349883, -0.3484186802494351, -0.33688985339222105, -0.32531029216226276, -0.31368174039889174, -0.3020059493192288, -0.29028467725446355, -0.27851968938505306, -0.2667127574748988, -0.25486565960451546, -0.24298017990326354, -0.23105810828067125, -0.2191012401568704, -0.20711137619221964, -0.19509032201612808, -0.18303988795514126, -0.170961888760302, -0.1588581433338627, -0.14673047445536175, -0.13458070850712664, -0.12241067519921715, -0.11022220729388273, -0.09801714032956076, -0.08579731234444053, -0.07356456359966855, -0.06132073630220841, -0.049067674327418334, -0.03680722294135964, -0.024541228522913582, -0.01227153828571993]
        p.update(x)

    def t2(*_, **__):
        print('t2')
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        p.update((x, y))

    test_util(p, t1, t2)
