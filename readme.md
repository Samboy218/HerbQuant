# HerbQuant

This project aims to automate the measurement of quantifying herbivory.
Currently the code is able to extract leaves from a scanned image of many leaflets and provide precise
measurements of each individual leaflet, further work will attempt to improve on this by attempting to
automatically quantify the herbivory, that is the amount of area missing due to herbivorous activity, 
of each leaf. This solution would be able to replace other methods which are slower, less precise, and may
cost orders of magnitude more money to implement.


## Usage
place scanned images containing multiple leaflets into the `samples/` directory. The script will scan that
directory and process any png images there. Extracted leaflets will be placed into the `images/` directory
(make sure this directory exists before execution of the script). Finally, the leaves will be measured and
this measurement data will be dumped into a file `data.csv`


This image:
![scan of many leaflets](./samples/Leaf_1_1.png)

Becomes all of these images:  
![leaf1](./images/Leaf_1_1-001.png)
![leaf2](./images/Leaf_1_1-002.png)
![leaf3](./images/Leaf_1_1-003.png)
![leaf4](./images/Leaf_1_1-004.png)
![leaf5](./images/Leaf_1_1-005.png)
![leaf6](./images/Leaf_1_1-006.png)
![leaf7](./images/Leaf_1_1-007.png)
![leaf8](./images/Leaf_1_1-008.png)
![leaf9](./images/Leaf_1_1-009.png)
![leaf10](./images/Leaf_1_1-010.png)
![leaf11](./images/Leaf_1_1-011.png)
![leaf12](./images/Leaf_1_1-012.png)
![leaf13](./images/Leaf_1_1-013.png)
