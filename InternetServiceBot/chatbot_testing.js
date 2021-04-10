const express = require("express");
const { WebhookClient } = require("dialogflow-fulfillment");
const { Payload } =require("dialogflow-fulfillment");
const app = express();

const MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
var randomstring = require("randomstring"); 
var user_name="";

app.post("/dialogflow", express.json(), (req, res) => {
    const agent = new WebhookClient({ 
		request: req, response: res 
		});

async function payload(agent)
{
  var payLoadData1=
  {
	"richContent": 
	[
	[
		{
		"type": "list",
		"title": "New User",
		"subtitle": "Press '1' for Registration",
		"event": {
			"name": "",
			"languageCode": "",
			"parameters": {}
		}
		},
		{
		"type": "divider"
		},
		{
		"type": "list",
		"title": "Already an User",
		"subtitle": "Press '2' login",
		"event": {
			"name": "",
			"languageCode": "",
			"parameters": {}
		}
		}
	]
	]
}
agent.add("Hi Enter Your Choice?")
agent.add(new Payload(agent.UNSPECIFIED,payLoadData1,{sendAsMessage:true, rawPayload:true }));
}
function isEmpty(val){
  return (val === undefined || val == null || val.length <= 0) ? true : false;
}

async function identify_user(agent)
{
  const choice =  agent.parameters.number;
  console.log(choice);
  if((choice>3) || (choice<0))
 {
 await agent.add("Enter correct choice");
}
else{
  console.log(choice);
	if(choice==2)
	{
	const client = new MongoClient(url);
	await client.connect();
	agent.add("Enter Username")
	const acct_num =  agent.parameters.phonenumber;
	if(isEmpty(acct_num))
	{
		await agent.add("Enter Username")
	}
	agent.add("Enter Password for ",acct_num);
	const password = await agent.parameters.password;
	if (isEmpty(password))
	{
	await agent.add("Enter password for",acct_num)
	}
	const snap = await client.db("AgentKiran").collection("UserInfo").findOne({acct_num: acct_num,password:password});
	console.log(snap);
	if(snap==null){
		await agent.add("Enter Your details correctly");
	}
	else
	{
	user_name=snap.username;
	await agent.add("Welcome  "+user_name+"!!  \n How can I help you");}
		}
  else
  {
	agent.add("Enter phonenumber");
	const acct_num = agent.parameters.phonenumber;
	console.log(acct_num);
	if (isEmpty(acct_num))
	{
		await agent.add("Enter phonenumber");
	}
	agent.add("Enter Password for ",acct_num);
	const password = agent.parameters.password;
	if(isEmpty(password))
	{
	agent.add("Enter Password for ",acct_num);
	}
	agent.add("Enter Username for ",acct_num);
	const name = agent.parameters.uname;
	console.log(acct_num,name,password,choice);
	const client = new MongoClient(url);
	await client.connect();
  if(!isEmpty(acct_num) || !isEmpty(password))
  {
	const insert = await client.db("AgentKiran").collection("UserInfo").insertOne({acct_num:acct_num,username:name,password:password});
	// console.log(insert);
  }
}
}
}
	
function report_issue(agent)
{
 
  var issue_vals={1:"Internet Down",2:"Slow Internet",3:"Buffering problem",4:"No connectivity"};
  
  const intent_val=agent.parameters.issue_num;
  
  var val=issue_vals[intent_val];
  
  var trouble_ticket=randomstring.generate(7);

  //Generating trouble ticket and storing it in Mongodb
  //Using random module
  MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("chatbot");
    
	var u_name = user_name;    
    var issue_val=  val; 
    var status="pending";

	let ts = Date.now();
    let date_ob = new Date(ts);
    let date = date_ob.getDate();
    let month = date_ob.getMonth() + 1;
    let year = date_ob.getFullYear();

    var time_date=year + "-" + month + "-" + date;

	var myobj = { username:u_name, issue:issue_val,status:status,time_date:time_date,trouble_ticket:trouble_ticket };

    dbo.collection("user_issues").insertOne(myobj, function(err, res) {
    if (err) throw err;
    db.close();    
  });
 });
 agent.add("The issue reported is: "+ val +"\nThe ticket number is: "+trouble_ticket);
}

//trying to load rich response
function custom_payload(agent)
{
	var payLoadData=
		{
  "richContent": [
    [
      {
        "type": "list",
        "title": "Internet Down",
        "subtitle": "Press '1' for Internet is down",
        "event": {
          "name": "",
          "languageCode": "",
          "parameters": {}
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "list",
        "title": "Slow Internet",
        "subtitle": "Press '2' Slow Internet",
        "event": {
          "name": "",
          "languageCode": "",
          "parameters": {}
        }
      },
	  {
        "type": "divider"
      },
	  {
        "type": "list",
        "title": "Buffering problem",
        "subtitle": "Press '3' for Buffering problem",
        "event": {
          "name": "",
          "languageCode": "",
          "parameters": {}
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "list",
        "title": "No connectivity",
        "subtitle": "Press '4' for No connectivity",
        "event": {
          "name": "",
          "languageCode": "",
          "parameters": {}
        }
      }
    ]
  ]
}
agent.add(new Payload(agent.UNSPECIFIED,payLoadData,{sendAsMessage:true, rawPayload:true }));
}




var intentMap = new Map();
intentMap.set("DefaultWelcomeIntent", payload);
intentMap.set("Service_intent", identify_user);
intentMap.set("Service_intent-custom-custom", report_issue);
intentMap.set("Service_intent-custom", custom_payload);

agent.handleRequest(intentMap);

});//Closing tag of app.post
console.log("listening on port number ",8080);
app.listen(process.env.PORT || 8080);

