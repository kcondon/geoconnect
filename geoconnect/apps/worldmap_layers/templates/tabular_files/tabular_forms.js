<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.10/css/jquery.dataTables.css">
<style>
/* Keep datatable header/body aligned */
#preview-tbl{ margin: 0;}

#table-wrapper {
  position:relative;
    border:1px solid #333;
}
#table-scroll {
  height:300px;
  overflow:auto;
  margin-top:20px;
}

.dataTables_wrapper.no-footer .dataTables_scrollBody {
    border: none;
}

</style>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.10/js/jquery.dataTables.js"></script>
<script>


    /* ------------------------------------------
        Submit the latitude/longitude form
    ------------------------------------------ */
    function submit_lat_lng_form(){
        logit('submit_lat_lng_form');

        // url for ajax  call
        check_lat_lng_url = '{% url 'view_process_lat_lng_form' %}';

        // Disable submit button + hide message box
        $('#id_frm_lat_lng_submit').addClass('disabled').html(getWorkingBtnMessage());
        $('#id_alert_container').empty().hide();

        // Submit form
        var jqxhr = $.post(check_lat_lng_url, $('#form_map_tabular_file').serialize(), function(json_resp) {
            // don't need a response for user
            logit(json_resp);
        })
        .done(function(json_resp) {
            if (json_resp.success){
                // Show map, update titles
                show_map_update_titles(json_resp);

            }else{
                logit(json_resp.message);
                // form error, display message
                //$('#msg_form_lat_lng').html(json_resp.message);
                $('#id_alert_container').show().empty().append(get_alert('danger', json_resp.message));

            }
          })
        .fail(function(json_resp) {
             //$('#simple_msg_div').empty().append(get_alert('danger', 'The classification failed.  Please try again.'));
        })
        .always(function() {
             // Enable submit button
             if ($('#id_frm_lat_lng_submit').length){
                 $('#id_frm_lat_lng_submit').removeClass('disabled').html('Submit Latitude & Longitude columns');
             }
        });
    }


    /**
        The user has selected a new "Geosptial Data Type"
        Via Ajax, retrieve a list of layers that match this type.
    */
    function update_target_layers_based_on_geotype(selected_geocode_type){

        logit('update_target_layers_based_on_geotype');
        if (selected_geocode_type.length == 0){
            return;
        }
        // form url to make request
        target_layers_by_type_url = '{% url 'ajax_get_all_join_targets' %}' + selected_geocode_type;

        // Temporarily disable layer dropdown box
        $('#id_chosen_layer').addClass('disabled');
        // Disable submit button
        $('#id_frm_single_column_submit').addClass('disabled').html('Working...');

        // Submit form
        var jqxhr = $.get(target_layers_by_type_url, function(json_resp) {
            // don't need a response for user
            logit(json_resp);
        })
        .done(function(json_resp) {
            if (json_resp.success && json_resp.data){
                logit('success!!' + json_resp.data);
                // {"message": "success", "data": [[9, "US Census Tract (2000) Boston Census Blocks"]], "success": true}
                // Update the dropdown box

                // Clear options from dropdown
                $('#id_chosen_layer')
                    .find('option').remove().end();

                // Add new options
                $.each(json_resp.data, function (index, item) {
                    $('#id_chosen_layer')
                        .append('<option value="' + item[0] + '">' + item[1] + '</option>');
                });

            }else{
                logit(json_resp.message);
                // form error, display message
                //$('#msg_form_lat_lng').html(json_resp.message);
                $('#id_alert_container').show().empty().append(get_alert('danger', json_resp.message));

            }
          })
        .fail(function(json_resp) {
        })
        .always(function() {
            // Enable dropdown
            $('#id_chosen_layer').removeClass('disabled');
            // Enable submit button
            $('#id_frm_single_column_submit').removeClass('disabled').html('Submit');

        });
        //alert(target_layers_by_type_url);
    }

    function submit_single_column_form(){
        logit('submit_single_column_form');

        // url for ajax  call
        map_tabular_file_url = '{% url 'view_map_tabular_file_form' %}';

        // Disable submit button + hide message box
        $('#id_frm_single_column_submit').addClass('disabled').html(getWorkingBtnMessage());
        $('#id_alert_container').empty().hide();

        // Submit form
        var jqxhr = $.post(map_tabular_file_url, $('#form_map_tabular_file').serialize(), function(json_resp) {
            // don't need a response for user
            logit(json_resp);
        })
        .done(function(json_resp) {
            if (json_resp.success){
                show_map_update_titles(json_resp);
                //$('#id_progress_bar').hide();
            }else{

                logit(json_resp.message);
                $('#id_alert_container').show().empty().append(get_alert('danger', json_resp.message));

            }
          })
        .fail(function(json_resp) {
             //$('#simple_msg_div').empty().append(get_alert('danger', 'The classification failed.  Please try again.'));
        })
        .always(function() {
             // Enable submit button
             if ($('#id_frm_single_column_submit').length){
                 $('#id_frm_single_column_submit').removeClass('disabled').html('Submit');
             }
        });
    }

    function bind_form_submit_buttons(){
        //logit('bind_submit_lat_lng_form');
        $("#id_frm_lat_lng_submit").on( "click", submit_lat_lng_form );
        $("#id_frm_single_column_submit").on( "click", submit_single_column_form );
    }

    function really_bind_hide_show_column_forms(){

        geocode_type_val = $( "#id_geocode_type" ).val()
        logit('type: '+ geocode_type_val);
        if (geocode_type_val == '{{ GEO_TYPE_LATITUDE_LONGITUDE }}'){
            // show latitude-longitude form
            $('.form_inactive_default').hide();
            $('.form_lat_lng_fields').show();
            $('.form_single_column_fields').hide();

        }else if (geocode_type_val == ''){
            // hide both forms

            $('.form_inactive_default').show();
            $('.form_lat_lng_fields').hide();
            $('.form_single_column_fields').hide();

        }else{
            // show single column form
            update_target_layers_based_on_geotype(geocode_type_val);
            $('.form_inactive_default').hide();
            $('.form_lat_lng_fields').hide();
            $('.form_single_column_fields').show();
            $("label[for='id_chosen_column']").html('Column for "' + $( "#id_geocode_type option:selected" ).html() + '"');

        }
    }

    function bind_hide_show_column_forms_on_ready(){
        really_bind_hide_show_column_forms();
    }

    function bind_hide_show_column_forms_on_change(){
        logit('bind geotype dropdown');
        $( "#id_geocode_type" ).change(function() {
            really_bind_hide_show_column_forms();
        });
    }


    /**
        Set the selected column option based on its value
    */
    function setNewSelectedCol(selectedText){
        var optToSelect = $('#id_chosen_column option[value="' +selectedText +'"]');
        if (typeof optToSelect === "undefined") {
            return;
        }
        logit("optToSelect: " + optToSelect.html());
        optToSelect.prop('selected', true);
    }

    /**
         click preview table to select tabular column
    */
    function bind_select_column_by_preview_table_click(){

        // Click on the header column
        $(".geo_col_select").on('click', function() {
            var selectedHeaderText = $(this).html();
            logit('clicked...:' + selectedHeaderText);
            setNewSelectedCol(selectedHeaderText);
        })

        // Click on the table body
        $("#preview-tbl tbody tr").on('click', 'td', function() {
              var colIdx = $(this).index();
              if (colIdx == 0) return;
              var colObj = $('#preview-tbl thead tr').find('th').eq(colIdx);
              var selectedHeaderText = colObj.find('div span').html();
              setNewSelectedCol(selectedHeaderText);
        });
    }

    $( document ).ready(function() {
        // bind events for form display
        bind_hide_show_column_forms_on_change();
        bind_hide_show_column_forms_on_ready();
        bind_form_submit_buttons();

        // click preview table to select tabular column
        bind_select_column_by_preview_table_click();

        var previewTable = $('#preview-tbl').DataTable( {
                "xscrollY": 200,
                "info":false, // remove 'Showing 1 to n of n entries'
                "scrollX": true,
                "paging" : false,
                "searching" : false
        } );

    // Example, iterate through header names
    /*
    logit('-- header names --');
    $('#preview-tbl thead tr th').each(function(){
        logit($(this).find('div span').html());
    })
    */

    // Example, iterate through option values names
    /*logit('-- option value names --');
    $('#id_chosen_column option').each(function(){
        logit($(this).html());
    })
    */
    });
</script>
