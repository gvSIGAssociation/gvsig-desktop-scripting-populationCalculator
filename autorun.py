# encoding: utf-8
import gvsig

#import os
#open(os.path.normpath(os.path.join(__file__,"..","..", "__init__.py")), "a").close()

from gvsig import getResource
from org.gvsig.andami import PluginsLocator

from org.gvsig.tools.swing.api import ToolsSwingLocator

from java.io import File
from org.gvsig.app import ApplicationLocator
import os
from org.gvsig.tools import ToolsLocator
from addons.populationCalculator.main import PopulationCalculatorExtension

# Icon made by [author link] from www.flaticon.com

def i18nRegister():
    i18nManager = ToolsLocator.getI18nManager()
    i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))

def selfRegister():

  application = ApplicationLocator.getManager()

  icon_show = File(gvsig.getResource(__file__,"populationcalculator.png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting.population-calculator", "action", "tools-population-calculator-show", None, icon_show)
  extension = PopulationCalculatorExtension()
  actionManager = PluginsLocator.getActionInfoManager()
  action_show = actionManager.createAction(
    extension,
    "tools-population-calculator-show", # Action name
    "Population Calculator", # Text
    "show", # Action command
    "tools-population-calculator-show", # Icon name
    None, # Accelerator
    1009000000, # Position
    "Population Calculator" # Tooltip
  )
  action_show = actionManager.registerAction(action_show)
  application.addTool(action_show, "Population Calculator")

def main(*args):
    i18nRegister()
    selfRegister()
