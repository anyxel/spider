const webSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`);

webSocket.onopen = function (event) {
  // console.log('WebSocket connection opened:', event);
};

webSocket.onclose = function (event) {
  console.log('WebSocket connection closed:', event);
};
