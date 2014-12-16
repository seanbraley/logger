## Server Side Code for App Logger-Android

### Requirements
* Python 2.7
* scipy
* scikit-learn
* reportlab

### Main app
* Requires access to port 12000

#### `main.py`
* Handles UDP packets from the Logger android application

#### `listen.py`
* Test script that prints UDP packets received to stdout, useful for debugging 

#### `run.py`
* Client side testing script

#### `analyse.py`
* Requires a text file in the same folder as the script, will use this to create a PDF with the results as a graph
* Graph will be the cluster the data belongs to over time
* Use {data, sample, testoutput, real_data}.txt are sample data files

#### `graphs.py`
* Contains the code for the line plot graphs


### Other included scripts
* Useful utilities

#### `fix_data.py`
* Fixes data that was recorded without proper line breaks

#### `kmeans1.py`
* Test file used during development, left in for reference

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
- [ ] Add threaded TCP Socket class that will attempt to send notification to the device

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