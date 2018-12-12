var exp = /Infinity.*war.*poster.*released/i; //a pattern to find whether posters are released
msg.search_result = msg.payload.search(exp);  //searches for pattern in msg.payload
//and produces : -1, for no match and 0 or more, for a match
var poster_print;
if(msg.search_result < 0)
    {
        poster_print = "Don't print the poster!";	//if pattern is not matched
    }
else
    {
        poster_print = "Print the poster!";			//if pattern is matched
    }
msg.payload = "Tweet/Input : \""+msg.payload+"\", Result : "+msg.search_result+".\n"+poster_print;
return msg;