
"""
Form for:
    - Select geospatial data
    - Select column 1
    - Select column 2 (if lat/lng)
    - clean
        - column 2 optional
        - column 1 cannot be same as column 2
"""
from django import forms
#from apps.worldmap_connect.jointarget_formatter import JoinTargetFormatter

'''
class DeleteMapForm(forms.Form):

    gis_data_file_md5 = forms.CharField(widget=forms.HiddenInput())
    worldmap_layer_info_md5 = forms.CharField(widget=forms.HiddenInput())
    confirmation = forms.BooleanField(label="I understand all versions of this map will be deleted from WorldMap.", initial=False)
'''

GEO_TYPE_LATITUDE_LONGITUDE = 'latitude-longitude'


class ChooseSingleColumnForm(forms.Form):
    """
    Basic form for capturing chosen column name
    """
    tabular_file_info_id = forms.IntegerField(widget=forms.HiddenInput())
    chosen_layer = forms.ChoiceField(label="Choose layer", choices=())
    chosen_column = forms.ChoiceField(label="Choose column", choices=())

    def __init__(self, tabular_file_info_id, layer_choices, column_names, *args, **kwargs):
        super(ChooseSingleColumnForm, self).__init__(*args, **kwargs)
        assert column_names is not None, "You must initiate this form with column names"

        colname_choices = [(c, c) for c in column_names if c]
        #print 'colname_choices', colname_choices
        self.fields['tabular_file_info_id'].initial = tabular_file_info_id

        self.fields['chosen_layer'].choices = layer_choices
        self.fields['chosen_layer'].widget.attrs.update({'class' : 'form-control'})

        self.fields['chosen_column'].choices = colname_choices
        self.fields['chosen_column'].widget.attrs.update({'class' : 'form-control'})


    def clean_chosen_layer(self):

        chosen_layer_id = self.cleaned_data.get('chosen_layer', None)
        if chosen_layer_id is None:
            ValidationError(_('You must choose a layer'))

        try:
            return int(chosen_layer_id)
        except ValueError:
            ValidationError(_('The layer does not have a valid id. (talk to the admin)'))


class LatLngColumnsForm(forms.Form):
    """
    Simple form for capturing latitude and longitude column names
    """
    err_msg_for_web = None

    tabular_file_info_id = forms.IntegerField(widget=forms.HiddenInput())
    latitude = forms.ChoiceField(label='Latitude Column', choices=())
    longitude = forms.ChoiceField(label='Longitude Column', choices=())

    def __init__(self, tabular_file_info_id, column_names, *args, **kwargs):
        super(LatLngColumnsForm, self).__init__(*args, **kwargs)
        assert column_names is not None, "You must initiate this form with column names"
        colname_choices = [(c, c) for c in column_names if c]
        print 'colname_choices', colname_choices
        self.fields['tabular_file_info_id'].initial = tabular_file_info_id
        self.fields['latitude'].choices = colname_choices
        self.fields['longitude'].choices = colname_choices

        self.fields['latitude'].widget.attrs.update({'class' : 'form-control'})
        self.fields['longitude'].widget.attrs.update({'class' : 'form-control'})

    def get_latitude_colname(self):
        assert self.cleaned_data is not None, "Do not call this unless .is_valid() is True"

        return self.cleaned_data.get('latitude')

    def get_longitude_colname(self):
        assert self.cleaned_data is not None, "Do not call this unless .is_valid() is True"

        return self.cleaned_data.get('longitude')

    def clean(self):
        """
        Check to make sure the lat and lng columns aren't the same
        """
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')

        if latitude == longitude:
            err_msg = 'The Longitude column cannot be the same as the Latitude column.'
            self.err_msg_for_web = err_msg
            # django 1.6
            self._errors["longitude"] = self.error_class([err_msg])
            del self.cleaned_data["longitude"]

            #self.add_error('longitude', err_msg)   # django 1.8
            raise forms.ValidationError(err_msg)

        return self.cleaned_data
"""
from apps.gis_tabular.forms import LatLngColumnsForm
f = LatLngColumnsForm()
"""