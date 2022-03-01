from psyplot.plotter import Formatoption
import psyplot.project as psy

from psy_simple.base import TextBase

class StandardTitle(TextBase, Formatoption):
    
    default=True
    
    @property
    def enhanced_attrs(self):
        return self.get_fig_data_attrs()
    
    def validate(self, s):
        if s:
            get_enhanced_attrs = self.get_enhanced_attrs(self.data)
            zname = self.get_enhanced_attrs(self.data)['zname']
            zvalue = self.get_enhanced_attrs(self.data)['z']
            return {"time":'%A %e %b %Y\n %d.%m.%Y %H:%M:%S', 
                    "details":(f"%(long_name)s on "
                         f"{zname} {zvalue}")}
        else:
            return False
    
    def update(self, s):
        if type(s) is dict:
            self.standardtitle = [self.ax.set_title(
                self.replace(s['time'], self.plotter.data, self.enhanced_attrs), loc='right'), 
                          self.ax.set_title(
                self.replace(s['details'], self.plotter.data, self.enhanced_attrs), loc='left')]
            self.clear_other_texts()
        else:
            self.standardtitle = [self.ax.set_title('', loc='right'), self.ax.set_title('', loc='left')]
            
    def clear_other_texts(self, remove=False):
        fig = self.ax.get_figure()
        # don't do anything if our figtitle is the only Text instance
        if len(fig.texts) == 1:
            return
        for i, text in enumerate(fig.texts):
            if text == self._text:
                continue
            if text.get_position() == self._text.get_position():
                if not remove:
                    text.set_text('')
                else:
                    del fig[i]
                    
psy.plot.mapplot.plotter_cls.standardtitle = StandardTitle("standardtitle")