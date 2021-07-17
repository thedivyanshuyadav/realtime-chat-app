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
        type:"GET",
        url:``,
        cache:false,
        data:{
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
        },
        success:function(s){
            var body = `<main>`;
            var bodyEnd = "</main>";
            var res = s.substring(s.indexOf(body)+body.length,s.indexOf(bodyEnd));
            var scrollT=$(".main").scrollTop()
            var maxScrollT=$(".main").height() - 25
            console.log(maxScrollT,scrollT);
            prevHtml=$("main").html()
            $("main").html(res);
            newHtml=$("main").html();

            if(maxScrollT-scrollT<35.5 && prevHtml!==newHtml)
                $(".main").scrollTop($(".main").height() + $(".main")[0].offsetHeight);
            else
                $(".main").scrollTop(scrollT);
        },
    });
}
// scrolling problem
setInterval(liveChatUpdate,1500);