$(document).ready(function () {
    $('tbody').on('change', '#part-price', function () {
        var buildPrice = 0;
        $('#part-price').each(function () {
            buildPrice += parseFloat($(this).val()) || 0;
        });
         $('#build-total').html(buildPrice);
    })

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
        event.preventDefault();
        return false;
        }
    });

    $('#add-bodykit').on('click', function(){
        part_id = $('#bodykit-categories').find(":selected").val();
        title = $('#bodykit-categories').find(":selected").text();
        var template = '<tr>\
                        <td scope="row">'
                            + title +
                        '</td>\
                        <td>\
                            <input type="text" class="form-control input-sm" name="'+ part_id +'_product" required>\
                        </td>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ part_id +'_link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ part_id +'_price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#bodykit-table').append(template);
    })

    $('#add-engine').on('click', function(){
        part_id = $('#engine-categories').find(":selected").val();
        title = $('#engine-categories').find(":selected").text();
        var template = '<tr>\
                            <td scope="row">'+ title +'</td>\
                        <td>\
                            <input type="text" class="form-control input-sm" name="'+ part_id +'_product" required>\
                        </td>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ part_id +'_link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ part_id +'_price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#engine-table').append(template);
    })

    $('#add-running-gear').on('click', function(){
        part_id = $('#running-gear-categories').find(":selected").val();
        title = $('#running-gear-categories').find(":selected").text();
        var template = '<tr>\
                            <td scope="row">'+ title +'</td>\
                        <td>\
                            <input type="text" class="form-control input-sm" name="'+ part_id +'_product" required>\
                        </td>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ part_id +'_link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ part_id +'_price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#running-gear-table').append(template);
    })

    $('#add-interior').on('click', function(){
        part_id = $('#interior-categories').find(":selected").val();
        title = $('#interior-categories').find(":selected").text();
        var template = '<tr>\
                            <td scope="row">'+ title +'</td>\
                        <td>\
                            <input type="text" class="form-control input-sm" name="'+ part_id +'_product" required>\
                        </td>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ part_id +'_link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ part_id +'_price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#interior-table').append(template);
    })

    $('tbody').on('click', '#delete-row', function(){
        $(this).closest('tr').remove();
    })

    $("#part-price").each(function( i ) {
        if ( this.innerHTML == "None" ) {
          this.closest('tr').remove();
        }
    });
})