$(document).ready(function () {
    $('tbody').on('change', '#part-price', function () {
        var buildPrice = 0;
        $('#part-price').each(function () {
            buildPrice += parseInt($('#part-price').val()) || 0;
        });
         $('#build-total').val(buildPrice);
    })

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
        event.preventDefault();
        return false;
        }
    });

    $('#add-bodykit').on('click', function(){
        name = $('#bodykit-categories').find(":selected").val();
        title = $('#bodykit-categories').find(":selected").text();
        var template = '<tr>\
                        <th scope="row">' +
                           title 
                        + '</th>\
                        <th>\
                            <input type="text" class="form-control input-sm" name="'+ name +'-product" required>\
                        </th>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ name +'-link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ name +'-price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#bodykit-table').append(template);
    })

    $('#add-engine').on('click', function(){
        name = $('#engine-categories').find(":selected").val();
        title = $('#engine-categories').find(":selected").text();
        var template = '<tr>\
                        <th scope="row">' +
                           title 
                        + '</th>\
                        <th>\
                            <input type="text" class="form-control input-sm" name="'+ name +'-product" required>\
                        </th>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ name +'-link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ name +'-price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#engine-table').append(template);
    })

    $('#add-running-gear').on('click', function(){
        name = $('#running-gear-categories').find(":selected").val();
        title = $('#running-gear-categories').find(":selected").text();
        var template = '<tr>\
                        <th scope="row">' +
                           title 
                        + '</th>\
                        <th>\
                            <input type="text" class="form-control input-sm" name="'+ name +'-product" required>\
                        </th>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ name +'-link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ name +'-price" step="any" id="part-price" required>\
                        </td>\
                        <td>\
                            <i class="far fa-times-circle" id="delete-row"></i>\
                        </td>\
                    </tr>'
        $('#running-gear-table').append(template);
    })

    $('#add-interior').on('click', function(){
        name = $('#interior-categories').find(":selected").val();
        title = $('#interior-categories').find(":selected").text();
        var template = '<tr>\
                        <th scope="row">' +
                           title 
                        + '</th>\
                        <th>\
                            <input type="text" class="form-control input-sm" name="'+ name +'-product" required>\
                        </th>\
                        <td>\
                            <input type="url" class="form-control input-sm" name="'+ name +'-link" required>\
                        </td>\
                        <td>\
                            <input type="number" class="form-control input-sm" name="'+ name +'-price" step="any" id="part-price" required>\
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
})