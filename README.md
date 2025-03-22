# **CSARCH2 Cache Simulator**

Walkthrough Video: https://drive.google.com/file/d/1HipP0E3Icc1ru5rPXftYyo5O1583sHqi/view?usp=sharing

## **System Specifications**
- **Cache Memory: 8-way BSA + MRU**
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

## **System Output**
### **a.) Cache Memory Snapshot**  
- Option for **step-by-step animated tracing** or **final memory snapshot**  
- Provide a **text log** of the cache memory trace (whether step-by-step or final)  

### **b.) Performance Metrics**  
1. **Memory access count**  
2. **Cache hit count**  
3. **Cache miss count**  
4. **Cache hit rate**  
5. **Cache miss rate**  
6. **Average memory access time**  
7. **Total memory access time**  

---

## **c.) Detailed Analysis**  
- Include a detailed analysis of the three test cases  
- Submit as **"README"** in your GitHub repository  
- Be sure to specify the **full specifications** of your cache simulation system  


