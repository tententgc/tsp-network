// Import deps
const { connect } = require("http2");
const net = require("net");
const readline = require("readline").createInterface({
	input: process.stdin,
	output: process.stdout,
});

// Parse peer's IP address list
const name = process.argv[2];
const peers = process.argv[3].split(",");

// Create socket server (for retrieving broadcast)
var server = net.createServer((socket) => {
	// Log connection
	const remoteDescription = socket.remoteAddress + ":" + socket.remotePort;
	const remoteTag = "[" + socket.remoteAddress + "] ";
	console.log("[SERVER] Incoming socket connection from " + remoteDescription);

	// Add data event handler
	socket.on("data", (data) => {
		const payload = data.toString().trim();

		// Log payload information
		console.log(remoteTag + "Recieved payload: " + payload);

		// Check if payload already passed through current node
		if (payload.split(", ").includes(name)) {
			console.log(remoteTag + "Repeated routing, discarded!");
			return;
		}

		// Append payload with node name
		const appended = payload + ", " + name;
		console.log(remoteTag + "Appended payload: " + appended);

		// Broadcast payload to peer
		peers.forEach((peer) => {
			const client = new net.Socket();
			client.connect(1337, peer, () => {
				console.log(remoteTag + "Connected to " + peer);
				client.write(appended);
				console.log(remoteTag + "Writing with " + appended);
				client._destroy(null, () => {
					console.log(remoteTag + "Disconnected from " + peer);
				});
			});
		});
	});
});

const prompt = async () => {
	readline.question("> ", (peer) => {
		if (peer == "") {
			prompt();
			return;
		}
		const client = new net.Socket();
		client.connect(1337, peer, () => {
			console.log("[CLIENT] Connected to " + peer);
			client.write(name);
			console.log("[CLIENT] Writing with " + name);
			client._destroy(null, () => {
				console.log("[CLIENT] Disconnected from " + peer);
			});
		});
		prompt();
	});
};

prompt();
server.listen(1337, "0.0.0.0");
