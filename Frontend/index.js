const user_email=document.getElementById("email");
const user_password=document.getElementById("password");
const form=document.getElementById("userinput");
form.addEventListener("submit",async(e)=>{
    e.preventDefault();
    try{
        const response=await fetch("http://127.0.0.1:8000/userdata",
        {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({email:user_email.value,password:user_password.value})
        })
    const data=await response.json();
    if(response.ok){
        console.log(data)
    }
    else{
        console.log(data.detail)
    }
    }catch(err){
        console.log(err)
    }
})