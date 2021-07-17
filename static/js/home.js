
$.ajax({
    type:"POST",
    url:"get-inbox/",
    success:function (response){
        // if(friends){
        //     inner=`<h5 class="slide-heading">Messages</h5>`
        // }else{
        //     inner=`<h5 class="slide-heading">Requests</h5>`
        // }
        inb_inner=``
        req_inner=``
        response.forEach((res)=>{
            id=res[1]
            name=res[2]
            pp=res[3]
            friends=res[4]
            last_msg_det=res[5]
            my_uid=res[6]

            let temp_html=`
                <div class="row tile">
                    <div class="inb_pp col-2">
                        <img src="${pp}" class="">
                    </div>
                    <span class="col-10" id="${id}" onclick="openchat(${id},${friends})">
                        <div>${name}</div>
                        <div class="row">
                            <div class="col">${last_msg_det['message']}</div>`
                if(!last_msg_det['read'] && last_msg_det['sent_by']!=my_uid){
                    temp_html=temp_html.concat(`<div class="col-1 material-icons">circle</div>`)
                }

            temp_html.concat(`</div>
                    </span>
               </div>`)
            if(friends){
                inb_inner=inb_inner.concat(temp_html)
            }else{
                req_inner=req_inner.concat(temp_html)
            }


        });

        let inbox=document.getElementById("inbox")
        inbox.innerHTML=inb_inner;
        $(inbox).prepend(`<h5 class="slide-heading">Messages</h5>`)

        let requests=document.getElementById("requests")
        requests.innerHTML=req_inner
        $(requests).prepend(`<h5 class="slide-heading">Requests</h5>`)

    },
}).done(()=>{
    $.post("get-contacts/",(response)=>{
        i=0
        html=``

        for(var c in response){
            // console.log(response[c]);
            if(i%2 ==0){
                if(i!=0){
                    html+=`</div>`
                }
                html+=`<div class="row contact-row">`
            }
            html+=`
                <div class="col-5 tile contact-tile" onclick="openchat(${response[c]["id"]},${response[c]["friend"]})">
                    <img src="${response[c]["profile_pic"]}" class="row">
                        <div class="col-auto contact-col-name">
                            <div class="text-center">${response[c]["name"]}</div>
                        </div>
                </div>`
            i+=1
        }
        html+=`</div>`
        $("#all-contacts-div").html(html);
    }).done(()=>{
        $.post('get-settings/',(response)=>{
            console.log(response);
            var name=response['name'];
            var pp=response['profile_pic'];
            $(".pprofile")[0].src=pp;
            $(".profile-name")[0].textContent=name;
        });
    });
});
function changeProfilePic(){
    form=document.createElement("form")
    form.action="change-dp/"
    form.id="dp-form"
    form.method="POST"
    form.style="display:none"
    form.enctype="multipart/form-data"
    img_inp=document.createElement("input")
    img_inp.type="file"
    img_inp.id="image"
    img_inp.name="image"
    img_inp.accept="image/*"
    form.append(img_inp)
    document.body.appendChild(form)
    img_inp.click()
    $(img_inp).on("change",()=>{
        var data=new FormData(form)
        $.ajax({
            type:'POST',
            url: "change-dp/",
            data:data,
            cache:false,
            contentType: false,
            processData: false,
            success:function(response){
                console.log(response)
                var image_url=response["image_url"]
                $(".pprofile")[0].src=image_url;
            },
            error: function(data){
                console.log(data)
                console.log("error profile pic not uploaded!");
            }
        }).done(()=>{
            document.getElementById("dp-form").remove();
        });
    });
}

function toggle_active(element){
    if(!element.classList.contains("active")){
        $(".bottom-icon.active")[0].classList.remove("active");
        element.classList.add("active");

        // var $screen=$(".carousel-item")[element.dataset.slideTo];
        // $(".carousel-item.active")[0].classList.remove("active");
        // $screen.classList.add("active");

    }
}

function expandAddForm(){
        $(".add-person-formdiv")[0].classList.toggle("closed")
        $(".add-person-formdiv>input")[0].classList.toggle("closed")
        $(".add-person-formdiv>input")[1].classList.toggle("closed")

}


function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark'); //add this

    }
    else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light'); //add this
    }
}

