$(document).ready(function() {
    var you = "Me";
    botSays("Hi how may i help you today ?")
});

function answer(x) {
    var you = "Me";    
    var Hello = ["HI", "HEY", "HOWDY", "HEYA", "HOLA", "HELLO", "SUP", "KONNICHIWA", "ALOHA"]
    var Goodbye = ["BYE", "SEE YA", "CYA", "LATER", "ADIOS", "SAYONARA", "SEEYA"]
    var Greeting = ["WHAT'S UP", "HOW'S IT GOING", "HOW ARE YOU", "NICE DAY", "GOOD MORNING", "GOOD NIGHT"]
    var Name = ["WHAT IS YOUR NAME", "WHAT'S YOUR NAME", "WHO ARE YOU", "WHAT DO THEY CALL YOU", "COMO TE LLAMAS"]
    var Actions = ["HELP", "DRINK", "CHALLENGE"]
    var Questions = ["QUESTION", "QUIZ", "CODE", "ANSWER", "HTML", "CSS", "JAVASCRIPT"];
    var Else = true;
    var reactions = [BotHello, BotGoodbye, BotGreeting];
    var BotHello = ["HI", "HEY", "HOWDY", "HEYA", "HOLA", "HELLO", "SUP", "KONNICHIWA", "ALOHA"]
    var BotGoodbye = ["BYE", "SEE YA", "CYA", "LATER", "ADIOS", "SAYONARA", "SEEYA"]
    var BotGreeting = ["WHAT'S UP", "HOW'S IT GOING", "HOW ARE YOU", "NICE TO SEE YOU", "GOOD MORNING", "WELCOME"]
    var BotPleasant = ["Thanks.", "Good job.", "Cool.", "I see.", "Anyway.", "right-o."]
    var botOut = botChat.value;
    var ans;
    document.getElementsByTagName("textarea")[0] = botChat
    document.getElementsByTagName("input")[0].value = ""

    question = x.toUpperCase()
    if (question === "" || null) {
        setTimeout(function() {
            botSays("\nBot : What? You shy?");
            botChat.scrollTop = botChat.scrollHeight;
        }, 600);
        return;
    } else if (Hello.includes(question)) {
        printUserMsg(x);
        callAws("Hi");
        botChat.scrollTop = botChat.scrollHeight;
        return;
    } else if (Goodbye.includes(question)) {
        printUserMsg(x);
        callAws("BYE");
        botChat.scrollTop = botChat.scrollHeight;
        return;
    } else if (Greeting.includes(question)) {
        printUserMsg(x);
        callAws("NICE DAY");
        botChat.scrollTop = botChat.scrollHeight;
        return;
    } else if (Name.includes(question)) {
        printUserMsg(x);
        callAws("WHO ARE YOU");
        botChat.scrollTop = botChat.scrollHeight;
        return;
    } else {
        printUserMsg(x);
        callAws(x);
        botChat.scrollTop = botChat.scrollHeight;
        return;
    }
}

function botSays(x) {
    document.getElementsByTagName("textarea")[0].innerHTML += ('\nBot : ' + x);
}

function printUserMsg(x) {
    document.getElementsByTagName("textarea")[0].innerHTML += ('\nMe : ' + x);
}

function youSay(x) {
    botSays("\n" + you + " \ : " + x)
}

function youDo(x) {
    botSays("\n" + you + " " + x)
}

function callAws(x) {
    var apigClient = apigClientFactory.newClient({
        apiKey: 'MAEHlqiTlQ1UgtBgzGv6k4cu1yLZZQy821ZwmEqT'
    });
    var params = {
    };
    var body = {
        "key1": x,
        "userId": "123"
    }


    var url = window.location.href;
	url_Split = url.split("/");
	token_split = url_Split[url_Split.length - 1].split("&");
	id_token = token_split[0].split("=");
	var token_id_final = id_token[1];
	console.log(id_token[1])


	var additionalParams = {
	  headers: {
	    'Authorization':token_id_final
	  }
	 
	};


    apigClient.chatbotPost(params, body, additionalParams)
        .then(function(result) {
            // Add success callback code here.
            x = result.data;
            botSays(x + "\n")
            console.log(result)
        }).catch(function(result) {
            // Add error callback code here.
            console.log(result)
        });
}

function enterButton(e, x) {
    if (e.keyCode == 13) {
        answer(x);
    }
}

function setCharAt(str, index, chr) {
    if (index > str.length - 1) return str;
    return str.substr(0, index) + chr + str.substr(index + 1);
}