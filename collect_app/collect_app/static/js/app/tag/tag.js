$(document).ready(function() {

    $("#uic_create_button").button().click(function(){
        var tag_name = $("#uic_tag_input").val();
        $.post("/api/tag",{
            'name':tag_name
        }, function(data){
            parent.fnCreateOrSelectTagCallback(data.tag_id);
        }).error(function(){
            alert('Erro');
        });
    });

    $("a[rel=uic_tag_link]").live("click",function(){
        var tag_id = $(this).attr('href');
        parent.fnCreateOrSelectTagCallback(tag_id);
        return false;
    });

    $("#uic_tg_table").dataTable({
        "bSort":false,
        "bInfo":false,
        "bPaginate": false,
        "sScrollY": "150px",
        "bFilter":true,
        "oLanguage": default_oLanguage

    });
});