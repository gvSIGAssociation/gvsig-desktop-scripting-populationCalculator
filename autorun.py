# encoding: utf-8

import gvsig
from org.gvsig.andami import PluginsLocator

from org.gvsig.tools.swing.api import ToolsSwingLocator

from java.io import File
from org.gvsig.app import ApplicationLocator
import os

from areaCalculator.main import AreaCalculatorExtension

# Icon made by [author link] from www.flaticon.com 

def selfRegister():

  application = ApplicationLocator.getManager()
  
  icon_show = File(os.path.join(os.path.dirname(__file__),"areacalculator.png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting.area-calculator", "action", "tools-area-calculator1-show", None, icon_show)
  
  extension = AreaCalculatorExtension()

  actionManager = PluginsLocator.getActionInfoManager()
  action_show = actionManager.createAction(
    extension, 
    "tools-area-calculator-show", # Action name
    "AreaCalculator", # Text
    "show", # Action command
    "tools-area-calculator1-show", # Icon name
    None, # Accelerator
    1009000000, # Position 
    "AreaCalculator" # Tooltip
  )
  action_show = actionManager.registerAction(action_show)
  application.addTool(action_show, "AreaCalculator")
  
def main(*args):
    selfRegister()
