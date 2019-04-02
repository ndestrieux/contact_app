$( document ).ready(function() {

    $(".alert").click(function() {
        $(this).hide();
    });

    $("#selectAll").click(function (event) {
        event.preventDefault()
       $("#id_groups > option").attr("selected",true);
    });

    $("#deselectAll").click(function () {
       $("#id_groups > option").removeAttr('selected');
    });


});
