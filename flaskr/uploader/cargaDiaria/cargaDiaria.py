class cargaDiaria:

    def __init__(self, centro, fecha, rDisp, rOc, cUTIdisp, cUTIoc, cCGdisp, cCGoc):
        self.centro = centro
        self.fecha = fecha
        self.rDisp = rDisp
        self.rOc = rOc
        self.cUTIdisp = cUTIdisp
        self.cUTioc = cUTIoc
        self.cGCdisp = cCGdisp
        self.cGCoc = cCGoc



    def cargarPacientes(self, pAlta, pCovidAlta, pFall, pCovidFall, pUTI):
        self.pAlta = pAlta
        self.pCovidAlta = pCovidAlta
        self.pFall = pFall
        self.pCovidFall = pCovidFall
        self.pUTI = pUTI