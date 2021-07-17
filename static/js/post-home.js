const toggleSwitch = document.querySelector('.tgl-group input[type="checkbox"]');
toggleSwitch.addEventListener('change', switchTheme, false);

const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
        toggleSwitch.checked = true;
    }
}
function openchat(id,friends){
    var form=document.createElement("form")
    form.action=`/chat/${id}/${friends}/`
    form.method="POST"
    document.body.appendChild(form)
    console.log(form)
    form.submit()

}

$(".add-person-formdiv").submit((ev)=>{
    ev.preventDefault();
    var name=$("#cf_name").val()
    var email=$("#cf_email").val()
    var data={
        name:name,
        email:email,
    }
    $.post('/add-contact-email/',data,(response)=>{
        var added=response['added'];
        console.log(added,response);
        if(added){
            $(".add-person-formdiv")[0].classList.toggle("closed")
            $(".add-person-formdiv>input")[0].classList.toggle("closed")
            $(".add-person-formdiv>input")[1].classList.toggle("closed")
        }else{
            $(".add-person-formdiv>input[type=email]").css({"border":"2px solid red",})
        }
    })

})
