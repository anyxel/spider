function callWithDelay(func, delay) {
  let timeout;
  return function (...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), delay);
  };
}

let wsPty = null;

function startApp() {
  const delay = 50;
  const host = 'localhost:8282';
  const pathname = '/';
  const scrollBackLimit = 5000; // current limit is 5000, change it in future if required
  const fitAddon = new FitAddon.FitAddon();
  const terminal = new Terminal({
    rows: 30,
    screenKeys: true,
    cursorBlink: true,
    macOptionIsMeta: true,
    scrollback: true,
  });
  const terminalDivId = "terminal";
  const webSocketProtocol = window.location.protocol.indexOf("https")
    ? "ws"
    : "wss";
  wsPty = new WebSocket(`${webSocketProtocol}://${host}${pathname}pty`);

  terminal.loadAddon(fitAddon);

  function fitToScreen() {
    fitAddon.fit();
    console.log(terminal.cols, terminal.rows);
    wsPty.send(
      JSON.stringify({
        action: "resize",
        data: {cols: terminal.cols, rows: terminal.rows},
      })
    );
  }

  window.onresize = callWithDelay(fitToScreen, delay);

  wsPty.onopen = function () {
    terminal.open(document.getElementById(terminalDivId));
    terminal.options.scrollback = scrollBackLimit;
    fitToScreen();
  };

  wsPty.onmessage = function (event) {
    terminal.write(event.data);
  };

  terminal.onKey((event) => {
    wsPty.send(JSON.stringify({action: "input", data: {key: event.key}}));
  });

  terminal.attachCustomKeyEventHandler((event) => {
    if (
      (event.ctrlKey || event.metaKey) &&
      event.code === "KeyV" &&
      event.type === "keydown"
    ) {
      navigator.clipboard.readText().then((clipText) => {
        wsPty.send(JSON.stringify({action: "input", data: {key: clipText}}));
      });
      event.preventDefault();
    }
  });

  function sendPing() {
    wsPty.send(JSON.stringify({action: "ping"}));
  }

  if (KEEP_ALIVE) {
    setInterval(sendPing, KEEP_ALIVE * 1000);
  }
}

window.onload = startApp;
