var htx = $(".textarea").height();
htx = htx - 22
$(".main").attr('style',
    "padding-bottom:"+htx+"px !important"
)

$(".main")[0].scrollTop = $(".main")[0].scrollHeight


firstKeyup=true

$(".textarea").on("keyup",()=>{

    if(firstKeyup) {
        firstKeyup=false;
        var htx = $(".textarea").height();
        htx = htx - 22
        console.log(htx)
        $(".main").attr("style",
            "padding-bottom:"+htx+"px !important"
        )
    }
});

$(".textarea").on("keydown",()=>{
    if(!firstKeyup) {
        firstKeyup=true;
        var htx = $(".textarea").height();
        htx = htx - 22
        $(".main").attr('style',
            "padding-bottom:"+htx+"px !important"
        )
    }
});


$(".footer-form").submit((ev)=>{

    ev.preventDefault();
    var message=$(".textarea")[0].innerText
    // html=`
    //     <div class="row mymsg-row">
    //         <div class="message">
    //             ${message}
    //         </div>
    //     </div>`
    // $(".main").append(html);
    $(".main").scrollTop($(".main").height()+$(".main").scrollTop()+150);
    $(".textarea")[0].textContent="";
    $(".textarea").keydown();
    var data={message:message};
    $.ajax({
        type:"POST",
        url:'send-message/',
        data:data,
        success:function (response){

        },
    });
});

function liveChatUpdate(){
    $.ajax({
        type:"POST",
        url:``,
        cache:false,
        data:{
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
        },
        success:function(s){
            var body = `<main>`;
            var bodyEnd = "</main>";
            var res = s.substring(s.indexOf(body)+body.length,s.indexOf(bodyEnd));
            $("main").html(res);
        },
    });
}
// scrolling problem
// setInterval(liveChatUpdate,1500);