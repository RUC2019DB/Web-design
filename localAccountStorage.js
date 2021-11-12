function setAccount(value)
{
    var date = new Date()
    var setTime = date.getTime()
    localStorage.setItem("username",value)
    localStorage.setItem("setTime",setTime)
}

function getAccount()
{
    return localStorage.getItem("username")
}

function deleteAccount()
{
    localStorage.removeItem("username")
    localStorage.removeItem("setTime")
}

function checkExpire()
{
    var date = new Date()
    var nowTime = date.getTime()
    var setTime = localStorage.getItem("setTime")
    if (setTime==null) return
    if ((nowTime-setTime)/1000/60/60>1) deleteAccount()
    return
}