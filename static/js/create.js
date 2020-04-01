$(document).ready(function () {
    $('tbody').on('change', '.part-price', function () {
        var buildPrice = 0;
        $('.part-price').each(function () {
            buildPrice += parseFloat($(this).val()) || 0;
        });
        $('#build-total').html(buildPrice);
        $('input[name="total"]').val(buildPrice);
    });

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
        event.preventDefault();
        return false;
        }
    });

    $('#add-exterior').on('click', function(){
        part_id = $('#exterior-categories').find(":selected").val();
        title = $('#exterior-categories').find(":selected").text();
        if (part_id != 'Choose an option'){
            var template = '<tr>' +
                        '<td scope="row">' + title + '</td>' +
                        '<td>' +
                            '<input type="text" class="form-control input-sm" name="exterior_'+ part_id +'_product" required>' +
                        '</td>' +
                        '<td>' +
                            '<input type="url" class="form-control input-sm" name="exterior_'+ part_id +'_link" required>' +
                        '</td>' +
                        '<td>' +
                            '<input type="number" class="form-control input-sm part-price" name="exterior_'+ part_id +'_price" step="any" required>' +
                        '</td>' +
                        '<td>' +
                            '<div class="text-center">' +
                                '<input type="checkbox" name="exterior_'+ part_id +'_purchased">' +
                            '</div>'+
                        '</td>' +
                        '<td>' +
                            '<i class="far fa-times-circle" id="delete-row"></i>' +
                        '</td>' +
                    '</tr>';
            $('#exterior-table').append(template);
        }
        
    });

    $('#add-engine').on('click', function(){
        part_id = $('#engine-categories').find(":selected").val();
        title = $('#engine-categories').find(":selected").text();
        if (part_id != 'Choose an option') {
           var template = '<tr>' +
                            '<td scope="row">' + title + '</td>' +
                            '<td>' +
                                '<input type="text" class="form-control input-sm" name="engine_'+ part_id +'_product" required>' +
                            '</td>' +
                            '<td>' +
                                '<input type="url" class="form-control input-sm" name="engine_'+ part_id +'_link" required>' +
                            '</td>' +
                            '<td>' +
                                '<input type="number" class="form-control input-sm part-price" name="engine_'+ part_id +'_price" step="any" required>' +
                            '</td>' +
                            '<td>' +
                            '<div class="text-center">' +
                                '<input type="checkbox" name="engine_'+ part_id +'_purchased">' +
                            '</div>'+
                            '</td>' +
                            '<td>' +
                                '<i class="far fa-times-circle" id="delete-row"></i>' +
                            '</td>' +
                        '</tr>';
            $('#engine-table').append(template); 
        }
        
    });

    $('#add-running-gear').on('click', function(){
        part_id = $('#running-gear-categories').find(":selected").val();
        title = $('#running-gear-categories').find(":selected").text();
        if (part_id != 'Choose an option') {
           var template = '<tr>' +
                            '<td scope="row">' + title + '</td>' +
                            '<td>' +
                                '<input type="text" class="form-control input-sm" name="running_'+ part_id +'_product" required>' +
                            '</td>' +
                            '<td>' +
                                '<input type="url" class="form-control input-sm" name="running_'+ part_id +'_link" required>' +
                            '</td>' +
                            '<td>' +
                                '<input type="number" class="form-control input-sm part-price" name="running_'+ part_id +'_price" step="any" required>' +
                            '</td>' +
                            '<td>' +
                            '<div class="text-center">' +
                                '<input type="checkbox" name="running_'+ part_id +'_purchased">' +
                            '</div>'+
                            '</td>' +
                            '<td>' +
                                '<i class="far fa-times-circle" id="delete-row"></i>' +
                            '</td>' +
                        '</tr>';
            $('#running-gear-table').append(template); 
        }
        
    });

    $('#add-interior').on('click', function(){
        part_id = $('#interior-categories').find(":selected").val();
        title = $('#interior-categories').find(":selected").text();
        if (part_id != 'Choose an option') {
           var template = '<tr>' +
                            '<td scope="row">' + title + '</td>' +
                            '<td>' +
                                '<input type="text" class="form-control input-sm" name="interior_'+ part_id +'_product" required>' +
                            '</td>' +
                            '<td>' +
                                '<input type="url" class="form-control input-sm" name="interior_'+ part_id +'_link" required>' +
                            '</td>' +
                            '<td>' +
                                '<input type="number" class="form-control input-sm part-price" name="interior_'+ part_id +'_price" step="any" required>' +
                            '</td>' +
                            '<td>' +
                            '<div class="text-center">' +
                                '<input type="checkbox" name="interior_'+ part_id +'_purchased">' +
                            '</div>'+
                            '</td>' +
                            '<td>' +
                                '<i class="far fa-times-circle" id="delete-row"></i>' +
                            '</td>' +
                        '</tr>';
            $('#interior-table').append(template); 
        }
        
    });

    $('tbody').on('click', '#delete-row', function(){
        $(this).closest('tr').remove();
    });
});
