$(document).ready(function () {

    $(".alert").click(function () {
        $(this).hide();
    });

    $("#selectAll").click(function (event) {
        event.preventDefault();
        $("#id_groups > option").attr("selected", true);
    });

    $("#deselectAll").click(function () {
        $("#id_groups > option").removeAttr('selected');
    });

    $('.remove_form').each(function () {
        const actualNbOfForms = parseInt($(this).closest('div').next('.form_set')
            .children('input:first').val());
        if (actualNbOfForms === 1) {
            $(this).addClass('disabled').attr('aria-disabled', true);
        }
    });

    $('form').on("click", ".add_form", function (event) {
        const formSetDiv = $(this).closest('div').next('.form_set');
        const totalForms = formSetDiv.children('input:first');
        const form_idx = totalForms.val();
        const emptyForm = formSetDiv.children('.empty_form');
        formSetDiv.append(emptyForm.html().replace(/__prefix__/g, form_idx));
        totalForms.val(parseInt(form_idx) + 1);
        if (parseInt(form_idx) + 1 > 1) {
            $(this).prev('a').removeClass('disabled').removeAttr('aria-disabled', true);
        }
    });

    $('form').on("click", ".remove_form", function (event) {
        const formSetDiv = $(this).closest('div').next('.form_set');
        const totalForms = formSetDiv.children('input:first');
        const form_idx = totalForms.val();
        formSetDiv.children('fieldset:last').remove();
        totalForms.val(parseInt(form_idx) - 1);
        if (parseInt(form_idx) - 1 === 1) {
            $(this).addClass('disabled').attr('aria-disabled', true);
        }
    });

});
