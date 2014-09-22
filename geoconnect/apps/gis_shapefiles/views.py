import logging

from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from apps.gis_shapefiles.forms import ShapefileInfoForm
from apps.gis_shapefiles.models import ShapefileInfo, WORLDMAP_MANDATORY_IMPORT_EXTENSIONS

from apps.gis_shapefiles.shapefile_zip_check import ShapefileZipCheck
from apps.gis_shapefiles.shp_services import get_successful_worldmap_attempt_from_shapefile

from apps.worldmap_import.models import WorldMapImportAttempt
from apps.classification.forms import ClassifyLayerForm, ATTRIBUTE_VALUE_DELIMITER

from geo_utils.geoconnect_step_names import GEOCONNECT_STEP_KEY, STEP1_EXAMINE, STEP2_VISUALIZE, STEP3_STYLE

from geo_utils.view_util import get_common_lookup

logger = logging.getLogger(__name__)


@login_required
def view_delete_files(request):
    if not settings.DEBUG:
        return HttpResponse('only for testing!')
    ShapefileInfo.objects.all().delete()
    return HttpResponseRedirect(reverse('view_examine_dataset', args=()))

    
@login_required
def view_delete_worldmap_visualization_attempts(request):
    if not settings.DEBUG:
        return HttpResponse('only for testing!')
    WorldMapImportAttempt.objects.all().delete()
    return HttpResponseRedirect(reverse('view_examine_dataset', args=()))


@login_required
def view_examine_dataset(request):
    """
    Display a list of :model:`gis_shapefiles.ShapefileInfo` objects, each linked to a detail page.
    For testing, allow the upload of a new shapefile object.

    **Context** 
    
    ``RequestContext``

    :ShapefileInfoForm: Check for a ShapefileInfoForm object in the request.POST
    
    **Template:**

    :template:`gis_shapefiles/view_01_examine_zip.html`
    """
    #return HttpResponse('view_google_map')
    d = { 'page_title' : 'Shapefiles: Test Upload Page'\
        , 'existing_shapefiles' : ShapefileInfo.objects.all()
        }
    
    if request.method=='POST':        
        shp_form = ShapefileInfoForm(request.POST, request.FILES)
        if shp_form.is_valid():
            shapefile_info = shp_form.save()
            return HttpResponseRedirect(reverse('view_shapefile'\
                                        , kwargs={ 'shp_md5' : shapefile_info.md5 })\
                                    )
            return HttpResponse('saved')            
        else:
            d['Form_Err_Found'] = True
            print shp_form.errors
            #return HttpResponse('blah - not valid')
    else:
        shp_form = ShapefileInfoForm

    d['shp_form'] = shp_form 

    return render_to_response('gis_shapefiles/view_01_examine_zip.html', d\
                            , context_instance=RequestContext(request))

#@login_required
def view_shapefile_first_time(request, shp_md5):
    return view_shapefile(request, shp_md5, first_time_notify=True)

def view_shapefile_visualize_attempt(request, shp_md5):
    return view_shapefile(request, shp_md5, just_made_visualize_attempt=True)


#@login_required
def view_shapefile(request, shp_md5, **kwargs):
    ## This logic shouldn't be here, factor it out similar to SendShapefileService
    """
    Retrieve and view a :model:`gis_shapefiles.ShapefileInfo` object

    :shp_md5: unique md5 hash for a :model:`gis_shapefiles.ShapefileInfo`
    :template:`gis_shapefiles/view_02_single_shapefile.html`
    """
    logger.debug('view_shapefile')

    first_time_notify = kwargs.get('first_time_notify', False)
    just_made_visualize_attempt = kwargs.get('just_made_visualize_attempt', False)

    d = get_common_lookup(request)
    d['page_title'] = 'Examine Shapefile'
    d['WORLDMAP_SERVER_URL'] = settings.WORLDMAP_SERVER_URL
    d[GEOCONNECT_STEP_KEY] = STEP1_EXAMINE 
    
    if first_time_notify:
        d['first_time_notify'] = True
    
    try:
        shapefile_info = ShapefileInfo.objects.get(md5=shp_md5)
        d['shapefile_info'] = shapefile_info
        
    except ShapefileInfo.DoesNotExist:
        logger.error('Shapefile not found for hash: %s' % shp_md5)
        raise Http404('Shapefile not found.')
    
    logger.debug('shapefile_info: %s' % shapefile_info)
    

    """
    Early pass: Move this logic out of view
    """
    if not shapefile_info.zipfile_checked:
        logger.debug('zipfile_checked NOT checked')

        logger.debug('fname: %s' % shapefile_info.get_dv_file_fullpath())
        #zip_checker = ShapefileZipCheck(shapefile_info.dv_file, **{'is_django_file_field': True})
        #zip_checker = ShapefileZipCheck(os.path.join(settings.MEDIA_ROOT, shapefile_info.dv_file.name))

        zip_checker = ShapefileZipCheck(shapefile_info.get_dv_file_fullpath())
        zip_checker.validate()

        list_of_shapefile_set_names = zip_checker.get_shapefile_setnames()

        # Error: No shapefiles found
        #
        if zip_checker.err_detected:
            # Update shapefile_info object
            shapefile_info.has_shapefile = False
            shapefile_info.zipfile_checked = True

            # Update for user template
            d['Err_Found'] = True

            if zip_checker.err_no_file_to_check:
                logger.debug('Error: No file to check')

                # Update shapefile_info object
                shapefile_info.name = '(no file to check)'
                shapefile_info.save()

                # Update for user template
                d['Err_No_File_Found'] = True
                #d['zip_name_list'] = zip_checker.get_zipfile_names()
                #d['WORLDMAP_MANDATORY_IMPORT_EXTENSIONS'] = WORLDMAP_MANDATORY_IMPORT_EXTENSIONS
                zip_checker.close_zip()

            elif zip_checker.err_no_shapefiles:
                logger.debug('Error: No shapefiles found')

                # Update shapefile_info object
                shapefile_info.name = '(not a shapefile)'
                shapefile_info.save()

                # Update for user template
                d['Err_No_Shapefiles_Found'] = True
                d['zip_name_list'] = zip_checker.get_zipfile_names()
                d['WORLDMAP_MANDATORY_IMPORT_EXTENSIONS'] = WORLDMAP_MANDATORY_IMPORT_EXTENSIONS
                zip_checker.close_zip()

            elif zip_checker.err_multiple_shapefiles:
                # Error: More than one shapefile in the .zip
                #
                shapefile_info.name = '(multiple shapefiles found)'
                shapefile_info.save()

                # Update for user template
                d['Err_Multiple_Shapefiles_Found'] = True
                d['list_of_shapefile_set_names'] = list_of_shapefile_set_names
                d['zip_name_list'] = zip_checker.get_zipfile_names()
                zip_checker.close_zip()

            # Send error to user
            return render_to_response('gis_shapefiles/view_02_single_shapefile.html', d\
                                    , context_instance=RequestContext(request))

        # Load the single shapefile
        #
        elif len(list_of_shapefile_set_names) == 1:
            logger.debug('Load the single shapefile')
            
            shapefile_info.has_shapefile = True
            shapefile_info.zipfile_checked = True
            shapefile_info.save()
            #shapefile_info.name = os.path.basename(list_of_shapefile_set_names[0])
            (success, err_msg_or_none) = zip_checker.load_shapefile_from_open_zip(list_of_shapefile_set_names[0], shapefile_info)
            if not success:
                #print 'here - err'
                d['Err_Found'] = True
                print ('Err msg: %s' % err_msg_or_none)
                if zip_checker.err_could_not_process_shapefile:
                    d['Err_Shapefile_Could_Not_Be_Opened'] = True
                    d['zip_name_list'] = zip_checker.get_zipfile_names()
                else:
                    d['Err_Msg'] = err_msg_or_none
                shapefile_info.has_shapefile = False
                shapefile_info.save()
                logger.error('Shapefile not loaded. (%s)' % shp_md5)
                return render_to_response('gis_shapefiles/view_02_single_shapefile.html', d\
                                        , context_instance=RequestContext(request))

            zip_checker.close_zip()    
                
            return render_to_response('gis_shapefiles/view_02_single_shapefile.html', d\
                                    , context_instance=RequestContext(request))
            
        
    # The examination failed
    # No shapefile was found in this .zip
    #
    if not shapefile_info.has_shapefile:
        logger.debug('No shapefile found in .zip')
        
        d['Err_Found'] = True
        d['Err_No_Shapefiles_Found'] = True
        #d['zip_name_list'] = zip_checker.get_zipfile_names()
        d['WORLDMAP_MANDATORY_IMPORT_EXTENSIONS'] = WORLDMAP_MANDATORY_IMPORT_EXTENSIONS
        return render_to_response('gis_shapefiles/view_02_single_shapefile.html', d\
                                , context_instance=RequestContext(request))
    
    
                            
    
    logger.debug('Has an import been attempted?')
    latest_import_attempt = WorldMapImportAttempt.get_latest_attempt(shapefile_info)
    #get_successful_worldmap_attempt_from_shapefile(shapefile_info)
    if latest_import_attempt:
        logger.debug('latest_import_attempt: %s' % latest_import_attempt )
        import_success_object = latest_import_attempt.get_success_info()
        if import_success_object:
            if just_made_visualize_attempt:
                d['page_title'] = 'Visualize Shapefile'
                d[GEOCONNECT_STEP_KEY] = STEP2_VISUALIZE
            else:
                d['page_title'] = 'Style Shapefile'
                d[GEOCONNECT_STEP_KEY] = STEP3_STYLE 
            
            classify_form = ClassifyLayerForm(**dict(import_success_object=import_success_object))
            #d['form_inline'] = True
            d['classify_form'] = classify_form
            d['ATTRIBUTE_VALUE_DELIMITER'] = ATTRIBUTE_VALUE_DELIMITER
            
                
                    
        d['import_success_object'] = import_success_object
        print(d)
        logger.debug('import_success_object: %s' % d['import_success_object'] ) #WorldMapImportSuccess.objects.filter(import_attempt__gis_data_file=shapefile_info)
        d['import_fail_list'] =latest_import_attempt.get_fail_info() 
        
        logger.debug('import_fail_list: %s' % d['import_fail_list'] ) 
        #WorldMapImportFail.objects.filter(import_attempt__gis_data_file=shapefile_info)
    

    
    return render_to_response('gis_shapefiles/view_02_single_shapefile.html', d\
                            , context_instance=RequestContext(request))
                            
   