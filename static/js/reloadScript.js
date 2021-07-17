

function liveMainPageUpdate(){
    $.ajax({
        type:"POST",
        url:"/inbox",
        cache:false,
        data:{
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
        },
        success:function(htmlResponse){
            var pageElement=document.createElement("html");
            $(pageElement).html(htmlResponse);
            var liveupdate=$($(pageElement.getElementsByClassName("carousel-item active")).children().filter("div.container-fluid.recent-chats")[0]).children().filter("div.liveupdate").html();
            $($(".carousel-item.active .recent-chats .liveupdate")[0]).html(liveupdate);
        },
    });
}