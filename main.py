# encoding: utf-8

from org.gvsig.scripting.app.extension import ScriptingExtension
from javax.swing import SpinnerNumberModel
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.io import File
from gvsig import currentView, currentLayer, getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.fmap.geom.primitive import OrientableSurface
from org.gvsig.fmap.geom import Geometry

import os
open(os.path.normpath(os.path.join(__file__,"..","..", "__init__.py")), "a").close()

from java.text import NumberFormat
from java.util import Locale

    
class PopulationCalculatorExtension(ScriptingExtension):
    def __init__(self):
      pass

    def canQueryByAction(self):
      return True

    def isEnabled(self,action):
      return currentView()!=None

    def isVisible(self,action):
      return currentView()!=None

    def execute(self,actionCommand, *args):
        l = PopulationCalculator()
        l.showTool("Population Calculator")

class PopulationCalculator(FormPanel):
    def __init__(self):
        FormPanel.__init__(self,
                            os.path.join(os.path.dirname(__file__),
                                        "populationCalculator.xml")
                            )
        self.setPreferredSize(350,150)
        #i18n = ToolsLocator.getI18nManager()

        #i18n = ToolsSwingLocator.getToolsSwingManager()
        #i18n.translate(self.lblLayer)
        #i18n.translate(self.lblArea)
        #i18n.translate(self.lblIndividual)
        #i18n.translate(self.lblPopulation)
        i18n = ToolsLocator.getI18nManager()
        self.lblLayer.setText(i18n.getTranslation("_Layer"))
        self.lblArea.setText(i18n.getTranslation("_Area"))
        self.lblIndividual.setText(i18n.getTranslation("_Individuals"))
        self.lblPopulation.setText(i18n.getTranslation("_Population"))
        mmin = 0.0
        mvalue = 4.0
        mmax = 5000.0
        mstepSize = 0.2
        model = SpinnerNumberModel(mvalue, mmin, mmax, mstepSize)
        self.spnRatio.setModel(model)
        layers = currentView().getLayers()
        self.cmbLayer.removeAllItems()
        for layer in layers:
            lyr = isPolygon(layer)
            if lyr != None:
                self.cmbLayer.addItem(str(layer.getName()))#[str(layer.getName()),layer])
            
    def cmbLayer_change(self, *args):
        self.calculate()

    def spnRatio_change(self, *args):
        self.calculate()

    def calculate(self,*args):
        name = self.cmbLayer.getSelectedItem()
        layer = currentView().getLayer(name)
        if layer==None:
            return 0
        totalArea = calculateTotalArea(layer)
        self.txtArea.setText(str(setSeparatorFormat(int(totalArea))))
        ratio = self.spnRatio.getValue()
        ratio = float(ratio)
        calculate = totalArea * ratio
        try:
          strCalculate = str(setSeparatorFormat(int(calculate)))
        except:
          strCalculate = ""
        self.txtCalculate.setText(strCalculate)

    def btnCalcular_click(self, *args):
        self.calculate()

    def btnClose_click(self,*args):
        self.hide()

def isPolygon(layer):
    getTypeVectorLayer = getattr(layer,"getTypeVectorLayer",None)
    if getTypeVectorLayer == None:
        return
    getGeometryType = getattr(layer,"getGeometryType",None)
    if getGeometryType != None:
      geomType = getGeometryType()
      if geomType.isSubTypeOf(Geometry.TYPES.SURFACE) or \
        geomType.isSubTypeOf(Geometry.TYPES.MULTISURFACE) or \
        geomType.isTypeOf(Geometry.TYPES.SURFACE) or \
        geomType.isTypeOf(Geometry.TYPES.MULTISURFACE):
          return layer
    return None

def setSeparatorFormat(value):
    formatter = NumberFormat.getInstance(Locale.getDefault())
    symbols = formatter.getDecimalFormatSymbols()
    symbols.setGroupingSeparator('.')
    formatter.setDecimalFormatSymbols(symbols)
    return formatter.format(value)
    
def calculateTotalArea(layer):
    #Input: Polygon layer
    #Output: area
    if layer==None:
        return 0
    #Area
    if layer.getFeatureStore().getSelection().getCount() != 0:
        fset = layer.getFeatureStore().getSelection()
    else:
        fset = layer.getFeatureStore().getFeatureSet()
    totalArea = 0
    for f in fset:
        geomArea = f.getDefaultGeometry().area()
        totalArea += geomArea
    return int(totalArea)

def main(*args):
    layer = currentLayer()
    print "CAL: ", calculateTotalArea(layer)

    l = PopulationCalculator()
    l.showTool("Population Calculator")
