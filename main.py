# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import FormPanel
import os
from org.gvsig.scripting.app.extension import ScriptingExtension
from javax.swing import SpinnerNumberModel
from org.gvsig.tools import ToolsLocator


class AreaCalculatorExtension(ScriptingExtension):
    def __init__(self):
      pass
  
    def canQueryByAction(self):
      return True
  
    def isEnabled(self,action):
      return gvsig.currentView()!=None
  
    def isVisible(self,action):
      return gvsig.currentView()!=None
      
    def execute(self,actionCommand, *args):
        l = AreaCalculator()
        l.showTool("PopulationCalculator")
        
class AreaCalculator(FormPanel):
    def __init__(self):
        FormPanel.__init__(self,
                            os.path.join(os.path.dirname(__file__),
                                        "populationCalculator.xml")
                            )
        i18n = ToolsLocator.getI18nManager()
        self.lblLayer.setText(i18n.getTranslation("_Layer"))
        
        mmin = 0.0
        mvalue = 4.0
        mmax = 5000.0
        mstepSize = 0.2
        model = SpinnerNumberModel(mvalue, mmin, mmax, mstepSize)
        self.spnRatio.setModel(model)
        layers = gvsig.currentView().getLayers()
        self.cmbLayer.removeAllItems()
        for layer in layers:
            self.cmbLayer.addItem(str(layer.getName()))#[str(layer.getName()),layer])
            
    def cmbLayer_change(self, *args):
        self.calculate()
        
    def spnRatio_change(self, *args):
        self.calculate()
    
    def calculate(self,*args):
        name = self.cmbLayer.getSelectedItem()
        layer = gvsig.currentView().getLayer(name)
        if layer==None:
            return 0
        totalArea = calculateTotalArea(layer)
        self.txtArea.setText(str(totalArea))
        ratio = self.spnRatio.getValue()
        try:
            ratio = float(ratio)
        except:
            ratio = 1
        calculate = totalArea * ratio
        try:
          strCalculate = str(calculate)[0:-2]
        except:
          strCalculate = ""
        self.txtCalculate.setText(strCalculate)

    def btnCalcular_click(self, *args):
        self.calculate()

    def btnClose_click(self,*args):
        self.hide()

def calculateTotalArea(layer):
    #Input: Polygon layer
    #Output: area
    if layer==None:
        return 0
    layerType = layer.getGeometryType().getName()
    if layerType == "MultiPolygon2D" or layerType=="Polygon2D":
        pass
    else:
        return 0
    #Area
    fset = layer.getFeatureStore().getFeatureSet()
    totalArea = 0
    for f in fset:
        geomArea = f.getDefaultGeometry().area()
        totalArea += geomArea
    return int(totalArea)

def main(*args):
    #layer = gvsig.currentLayer()
    #value = calculateTotalArea(layer)
    #print "Area total: ", value
    #return
    l = AreaCalculator()
    l.showTool("Area Calculator")
    pass