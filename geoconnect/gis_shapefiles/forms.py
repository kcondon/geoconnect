from django import forms
from gis_shapefiles.models import ShapefileSet


class ShapefileSetForm(forms.ModelForm):
    class Meta:
        model = ShapefileSet
        fields = ['name', 'dv_file',]
"""

class ShapefileGroupForm(forms.Form):
    name = forms.CharField(initial='BARI test')
    gis_file = forms.FileField(label='GIS file')
    #sender = forms.EmailField()
    #cc_myself = forms.BooleanField(required=False)
    
"""