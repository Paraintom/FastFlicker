//V 1.0

// Interface : 
// 1 - Create the chat object :
//  url = "ws://"+ip+":"+port+"/";
//	chat = new FastFLickerChat(url);
// 2- Listen to incoming message ---> onNewMessage should look like : function(e) {console.log(e.detail);}
//    Every message from the server raise an event from the chat, the msg itself is in the field detail of the event.
//	chat.subscribeForNewMessages(onNewMessage);
//	chat.listenTo(subjectString);
//  chat.doSend(msgToSend);

function FastFLickerChat(fastFlikerUrl){
	this.url = fastFlikerUrl;
}
  
FastFLickerChat.prototype.url = '';
FastFLickerChat.prototype.currentSubject = '';
FastFLickerChat.prototype.websocket;
FastFLickerChat.prototype.newMessageEventName = 'newMessageEvent';

FastFLickerChat.prototype.listenTo = function (subject) {
	if (typeof websocket != "undefined") {
		//closing the existing connection		
		websocket.onopen = null;
		websocket.onclose = null;
		websocket.onmessage = null;
		websocket.onerror = null;
		websocket.close();	
	}
	websocket = new WebSocket(this.url);
	instance = this;
	websocket.onopen = function(evt) { instance.onOpen(evt) };
    websocket.onclose = function(evt) { instance.onClose(evt) };
    websocket.onmessage = function(evt) { instance.onMessage(evt) };
    websocket.onerror = function(evt) { instance.onError(evt) };
	this.currentSubject = subject;
  }
  
FastFLickerChat.prototype.onOpen = function (evt)
  {
    FastFLickerChat.prototype.sendNewMsg("connected\n");
	this.doSend(this.currentSubject);
  }

  
FastFLickerChat.prototype.onClose = function (evt)
  {
    this.sendNewMsg("disconnected\n");
  }

FastFLickerChat.prototype.onMessage = function (evt)
  {
	if(evt.data != this.currentSubject)
		this.sendNewMsg("response: " + evt.data + '\n');
  }
  
FastFLickerChat.prototype.onError = function (evt)
  {
    this.sendNewMsg('error: ' + evt.data + '\n');
	websocket.close();
  }
  
  
FastFLickerChat.prototype.doSend = function (message)
  {
	if(message != this.currentSubject){
		this.sendNewMsg("sent: " + message + '\n'); 
	}
	websocket.send(message);
  }

FastFLickerChat.prototype.sendNewMsg = function(message)
  {
	event = new CustomEvent(this.newMessageEventName, { 'detail': message });
	// Dispatch/Trigger/Fire the event
	document.dispatchEvent(event);
  }
  
FastFLickerChat.prototype.subscribeForNewMessages = function (onNewMessage)
  {
	//onNewMessage should look like : function(e) {console.log(e.detail);}
	document.addEventListener(this.newMessageEventName, onNewMessage);
  }