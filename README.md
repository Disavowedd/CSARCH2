# **CSARCH2 Cache Simulator**

Walkthrough Video: https://drive.google.com/file/d/1HipP0E3Icc1ru5rPXftYyo5O1583sHqi/view?usp=sharing

#### Submitted by:
##### CSARCH2 S12 Group 8
- Kyle Adrian Bibon
- Gian Raphael Blasco
- Kenneth Louis Mangulabnan
- Antonio Enrique Monserrat
- Carlo San Buenaventura


## **System Specifications**
- **Cache Memory: 8-way Block Set Associative + Most Recently Used**
- **Cache line size:** 16 words  
- **Number of cache blocks:** 32 blocks  
- **Read policy:** Non load-through  
- **Number of memory blocks:** User input (minimum of 1024 blocks)  

---

## **Test Cases**
### **a.) Sequential Sequence**  
- Sequence up to **2n** cache blocks  
- Repeat the sequence **four times**  
- **Example** (if n = 32):  
  `0, 1, 2, 3, ..., 63` {repeated 4x}  

---
### **b.) Random Sequence**  
- Sequence containing **4n** main memory blocks  
- Randomly ordered  

---
### **c.) Mid-Repeat Blocks**  
- Start at **block 0**  
- Repeat the sequence in the middle **two times** up to **n - 1** blocks  
- Continue up to **2n**  
- Repeat the sequence **four times**  
- **Example** (if n = 8):  
  `0, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15` {repeated 4x}  

---
---
## Test Case Detail Analyses:
###### 8-way BSA Cache Table Format
|  Set  | Block 0 | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 | Block 6 | Block 7 |
| :---: | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|   0   |         |         |         |         |         |         |         |         |
|  Age  |         |         |         |         |         |         |         |         |
|   1   |         |         |         |         |         |         |         |         |
|  Age  |         |         |         |         |         |         |         |         |
|   2   |         |         |         |         |         |         |         |         |
|  Age  |         |         |         |         |         |         |         |         |
|   3   |         |         |         |         |         |         |         |         |
|  Age  |         |         |         |         |         |         |         |         |

##### a.) Sequential Sequence
##### b.) Random Sequence
##### c.) Mid-Repeat Blocks: 
