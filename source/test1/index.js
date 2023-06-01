const { connect } = require("http2");
const net = require("net");
const readline = require("readline").createInterface({
	input: process.stdin,
	output: process.stdout,
});


const paths = {};

const name = process.argv[2];
const peers = process.argv[3].split("|")[0].split(",");
const distance_peers = process.argv[3].split("|")[1].split(",");
const showoutput = false;


var server = net.createServer((socket) => {
	const remoteDescription = socket.remoteAddress + ":" + socket.remotePort;
	const remoteTag = "[" + socket.remoteAddress + "] ";
	console.log();
	console.log("[SERVER] Incoming socket connection from " + remoteDescription);

socket.on("data", (data) => {
		const payload = data.toString().trim().split("|")[0];
		var distance = Number(data.toString().trim().split("|")[1]);

		if (payload.split(", ").length + 1 == peers.length + 2) {
			const array = payload.split(", ");
			const set = new Set(array);
			if (set.size === array.length && array[0] == name) {
				console.log("path: " + payload + ", " + name + " with distance " + distance);

		
				paths[payload + ", " + name] = distance;

				return;
			}
			return;
		} else {
			if (showoutput) {
				console.log(remoteTag + "Recieved payload: " + payload + ", " + name);
			}
		}

		if (payload.split(", ").includes(name)) {
			if (showoutput) {
				console.log(remoteTag + "Repeated routing, discarded!");
			}
			return;
		}

		const appended = payload + ", " + name;
		if (showoutput) {
			console.log(remoteTag + "Appended payload: " + appended);
		}

		
		peers.forEach((peer) => {
			const client = new net.Socket();
			client.connect(1337, peer, () => {
				console.log(remoteTag + "Connected to " + peer);
				client.write(appended + "|" + (distance + Number(distance_peers[peers.indexOf(peer)])));
				console.log(remoteTag + "Writing with " + appended);
				client._destroy(null, () => {
					console.log(remoteTag + "Disconnected from " + peer);
				});
			});
		});
	});
});

// Compute minimum path with distance
function getMinPath() {
	let minDistance = Infinity;
	let minPath = null;
	for (let path in paths) {
		if (paths[path] < minDistance) {
			minDistance = paths[path];
			minPath = path;
		}
	}
	if (minPath) {
		console.log(`Min path is: ${minPath} with distance ${minDistance}`);
	} else {
		console.log("No path found");
	}
}


const prompt = async () => {
	readline.question("> ", (command) => {
		if (command == "run") {
			peers.forEach((peer) => {
				if (peer == "") {
					prompt();
					return;
				}
				const client = new net.Socket();
				client.connect(1337, peer, () => {
					console.log("[CLIENT] Connected to " + peer);
					client.write(name + "|" + distance_peers[peers.indexOf(peer)]);
					console.log("[CLIENT] Writing with " + name);
					client._destroy(null, () => {
						console.log("[CLIENT] Disconnected from " + peer);
					});
				});
			});
			prompt();
		} else if (command == "minpath") {
			getMinPath();
		}
	});
};

prompt();
server.listen(1337, "0.0.0.0");
