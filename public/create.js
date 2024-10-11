const form_submit = document.getElementById("create-coop")
const form = document.getElementById("create_form")

form_submit.addEventListener("click", create_coop_lobby)

function create_coop_lobby() {
    let code = Math.round(Math.random()*100000,0);
    console.log(code)
}