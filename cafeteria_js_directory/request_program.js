function validation()
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function()
  {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("numeric").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET","http://127.0.0.1:5000/", true);
  xhttp.send();
}