$(document).ready(function() {
    $("a").each(function( i ) {
        if ( this.innerHTML == "" ) {
          this.closest('tr').remove();
        }
    });
})