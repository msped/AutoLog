$(document).ready(function() {
    $("a").each(function( i ) {
        if ( this.innerHTML == "None" ) {
          this.closest('tr').remove();
        }
    });
})