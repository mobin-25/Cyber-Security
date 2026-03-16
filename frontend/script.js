async function analyze() {

let message = document.getElementById("message").value;

let response = await fetch("http://127.0.0.1:5000/analyze",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({text:message})
});

let data = await response.json();

let color = "green"

if(data.risk === "HIGH"){
color = "red"
}
else if(data.risk === "SUSPICIOUS"){
color = "orange"
}

document.getElementById("result").innerHTML =
"<b style='color:"+color+"'>Risk Level: "+data.risk+"</b>" +
"<br>Detected Words: " + data.detected.join(", ");

}