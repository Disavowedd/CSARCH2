# **CSARCH2 Cache Simulator**

Walkthrough Video: https://drive.google.com/file/d/1UB8l4Ye78i3JIy7V5gtWQ2NEWmql1cG7/view?usp=sharing

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
## Test Case Detail Analyses:
###### 8-way BSA Cache Table Format
|  Set  | Block 0 | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 | Block 6 | Block 7 |
| :---: | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|   0   |         |         |         |         |         |         |         |         |
|   1   |         |         |         |         |         |         |         |         |
|   2   |         |         |         |         |         |         |         |         |
|   3   |         |         |         |         |         |         |         |         |

##### a.) Sequential Sequence:
**Initial Cache State and Memory Access Pattern:**

At the start, the cache is empty, so the first memory accesses result in cache misses. The set index is determined by:
Set Index = (Block Number)mod(Number of Sets). Once sets are full, the MRU policy evicts the most recently used block, causing frequent replacements when new blocks are introduced. After the cache is populated, repeated access to the same blocks results in cache hits. 

Number of memory blocks: 1024
**FINAL CACHE MEMORY SNAPSHOT:**
|  Set  |  Block 0  |  Block 1  |  Block 2  |  Block 3  |  Block 4  |  Block 5  |  Block 6  |  Block 7  |
| :---: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| **0** |     0     |     4     |     8     |     12    |     48    |     52    |     56    |     60    |
| **1** |     1     |     5     |     9     |     13    |     49    |     53    |     57    |     61    |
| **2** |     2     |     6     |     10    |     14    |     50    |     54    |     58    |     62    |
| **3** |     3     |     7     |     11    |     15    |     51    |     55    |     59    |     63    |

**Cache Outputs and Performance:**
The simulation records **256 memory accesses with 96 hits and 160 misses**, giving a **37.50% hit rate** and **62.50% miss rate.**

The average memory access time is: (96×16)+(160×177)/256 = **116.62ns**
where:
- Cache hit time = 16 ns
- Cache miss time = 177 ns

The total memory access time is: 96×16+160×177 = **29856ns**

The cache initially experiences high miss rates due to filling and MRU-based replacements. However, once the working set stabilizes, hit rates improve, enhancing overall performance.

##### b.) Random Sequence:

##### c.) Mid-Repeat Blocks: 
