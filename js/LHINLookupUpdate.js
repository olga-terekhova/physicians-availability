function fetchRegion(postalCode) {
                                                                     

var xhttp = new XMLHttpRequest();
var postie = postalCode;

xhttp.onreadystatechange = function() {
                                                                            if (this.readyState == 4 && this.status == 200) {
                                                                                var regionResponse = this.responseText;
                                                                                
                                                                                const txt = regionResponse;
                                                                                const obj = JSON.parse(txt);
                                                                                var regionName = obj.name;
                                                                                
                                                                                console.log(regionName)
                                                                                

                                                                                //document.getElementById("myBranch").innerHTML = 'Your local branch is:<br/><a class="button postalcodetool" href="' + regionRel + '">' + regionName + '</a>';
                                                                            }
                                                                        }
                                                                        ;


xhttp.open("GET", "https://hccss-prod-func.azurewebsites.net/api/FindMyRegion?postalCode=" + postie, true);
xhttp.send();

}