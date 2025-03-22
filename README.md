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

---

### a.) **Sequential Sequence:**  
**Initial Cache State and Memory Access Pattern:**  
- At the start, the cache is empty, so the first memory accesses result in cache misses. The set index is determined by:  
**Set Index = (Block Number) mod (Number of Sets)**  

Once sets are full, the MRU policy evicts the most recently used block, causing frequent replacements when new blocks are introduced. After the cache is populated, repeated access to the same blocks results in cache hits. 

**Number of memory blocks:** 1024  

**FINAL CACHE MEMORY SNAPSHOT:**  
|  Set  |  Block 0  |  Block 1  |  Block 2  |  Block 3  |  Block 4  |  Block 5  |  Block 6  |  Block 7  |
| :---: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| **0** |     0     |     4     |     8     |     12    |     48    |     52    |     56    |     60    |
| **1** |     1     |     5     |     9     |     13    |     49    |     53    |     57    |     61    |
| **2** |     2     |     6     |     10    |     14    |     50    |     54    |     58    |     62    |
| **3** |     3     |     7     |     11    |     15    |     51    |     55    |     59    |     63    |

**Cache Outputs and Performance:**  
- The simulation records **256 memory accesses** with **96 hits** and **160 misses**, giving a **37.50% hit rate** and **62.50% miss rate**.  
- The average memory access time is:  (96×16)+(160×177)/256 = **116.62ns**
  
  where:  
  - Cache hit time = **16 ns**  
  - Cache miss time = **177 ns**
    
- The total memory access time is: 96×16+160×177 = **29,856ns**

The cache initially experiences high miss rates due to filling and MRU-based replacements. However, once the working set stabilizes, hit rates improve, enhancing overall performance.  

---

### b.) **Random Sequence:**  
**Initial Cache State and Memory Access Pattern:**  
- In the random sequence test case, the memory access pattern follows a random order, meaning that the accessed memory blocks are distributed without any predictable pattern. This type of access pattern is challenging for a cache to optimize because it lacks locality of reference, which makes it difficult for the cache to anticipate future accesses.  

At the start, the cache is initially empty. Since the accesses are random, there is no repetition or predictable order, causing frequent cache misses. The memory access count is **128**, which reflects the number of memory requests processed by the cache during the simulation.  

**Number of memory blocks:** 1024  

**FINAL CACHE MEMORY SNAPSHOT:**  
|  Set  |  Block 0  |  Block 1  |  Block 2  |  Block 3  |  Block 4  |  Block 5  |  Block 6  |  Block 7  |
| :---: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| **0** |    952    |    344    |    780    |    936    |     4     |    392    |    412    |    496    |
| **1** |    81     |    357    |    297    |    25     |    121    |    237    |    853    |    425    |
| **2** |    934    |    206    |    110    |    970    |    278    |    1014   |    150    |    918    |
| **3** |    875    |    371    |    883    |    923    |    611    |    311    |    991    |    783    |

**Cache Outputs and Performance:**  
- The simulation records **128 memory accesses** with **5 hits** and **123 misses**, giving a **3.91% hit rate** and **96.09% miss rate**.  
- The average memory access time is:  (5×16)+(123×177)/128 = **170.71ns**

   where:  
  - Cache hit time = **16 ns**  
  - Cache miss time = **177 ns**
    
- The total memory access time is: (5×16)+(123×177) = **21,851ns**
  
The low hit rate reflects the challenges posed by the random access pattern, which prevents the cache from taking advantage of temporal or spatial locality. The high miss rate results in frequent data fetching from the main memory, increasing the overall memory access time. 

---

### c.) **Mid-Repeat Blocks:**  
**Initial Cache State and Memory Access Pattern:**  
- In the mid-repeat blocks test case, the memory access pattern shows moderate levels of repetition, meaning that certain memory blocks are accessed multiple times after some interval. This creates an opportunity for the cache to benefit from **temporal locality** (recently accessed blocks being accessed again) and **spatial locality** (nearby blocks being accessed together). The cache starts in an empty state, leading to initial misses as it fills up. However, once the working set stabilizes and repeated blocks begin to be accessed, the hit rate improves.  

**Number of memory blocks:** 1024  

**FINAL CACHE MEMORY SNAPSHOT:**  
|  Set  |  Block 0  |  Block 1  |  Block 2  |  Block 3  |  Block 4  |  Block 5  |  Block 6  |  Block 7  |
| :---: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| **0** |     0     |     8     |     16    |     24    |     48    |     52    |     56    |     60    |
| **1** |     1     |     9     |     17    |     25    |     49    |     53    |     57    |     61    |
| **2** |     2     |     10    |     18    |     26    |     50    |     54    |     58    |     62    |
| **3** |     3     |     11    |     19    |     27    |     51    |     55    |     59    |     63    |

**Cache Outputs and Performance:**  
- The simulation records **380 memory accesses** with **196 hits** and **184 misses**, giving a **51.58% hit rate** and **48.42% miss rate**.  
- The average memory access time is: (196×16)+(184×177)/380 = **93.96ns**

   where:  
  - Cache hit time = **16 ns**  
  - Cache miss time = **177 ns**
  
- The total memory access time is:  (196×16)+(184×177) = **35,704ns**

The higher hit rate (compared to random access) reflects the benefit of repeating memory blocks, which allows the cache to take advantage of temporal locality. However, the hit rate is not perfect due to the moderate level of repetition and the working set exceeding the cache size at times, leading to evictions and subsequent misses.
