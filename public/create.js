const form_submit = document.getElementById("create-coop")
const form = document.getElementById("create_form")
const code_elmnt = document.getElementById("code")

form_submit.addEventListener("click", create_coop_lobby)

function create_coop_lobby() {
    
    //console.log(code)

    //reveal code
    //send code to backend db so join func works
    async function getData() {
        const response = await fetch("/create", {
            method: "POST",
        });
          
        let data = await response.json()        
        code_elmnt.innerHTML = data
        form_submit.innerHTML = "Join"
        form_submit.removeEventListener("click", create_coop_lobby)
        form_submit.href = `/join?id=${data}`
    }

    getData()
    //change create to join button
    //go to "waiting for player to join" view
    

}