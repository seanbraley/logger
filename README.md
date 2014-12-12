## Server Side Code for App

### Running app
`python main.py`

### Debugging
`python listen.py`
* Will print everything the main script would see.
* Requires access to port 12000

### `run.py`
* Client side testing script

### `main.py`
* Currently handles UDP requests turning them into upper case

---
## Server Side Actions

### Main actions
```
set counter=0
loop
	wait for UDP packet
	on packet received:
		counter += 1
		data = normalize(data)
		if counter < 100:
			add_data_to_cluster(data)
		elif counter == 100:
			fit(iterations=n)
		elif counter%10==0:
			fit_predict(data)
		else:
			fit(data)
```

### General Todo
- [x] Create the repo
- [x] Get Ports working
- [ ] Write out pseudocode for server actions
- [ ] ???
- [ ] Add threaded TCP Socket class that will attempt to send notification to the device
- [ ] ???

### Extended Todo
- [ ] Install Cassandra
- [ ] Connect python to Cassandra
- [ ] Store incoming data packets
- [ ] Design retrieval scripts
- [ ] Investigate MiniBatchClustering	

### Current Limitations
* Server will forget dataset when server shuts down
	* We will need to keep a base set to start from
* KMeans object does not keep record of data passed into it