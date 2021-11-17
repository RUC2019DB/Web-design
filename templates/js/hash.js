function hash(str)
{
    var b = 378551;  
    var a = 63689;  
    var hash = 0;
    var modKey = 999999999755591
    for(var i = 0; i<str.length; i++)  
    {  
        hash = (hash * a + str.charAt(i).charCodeAt()) % modKey;
        a  = (a * b) % modKey
    }  
    return hash;
}