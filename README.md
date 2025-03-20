# Uniform-Design-Schedule

本程式自方開泰先生所著的《均勻設計與均勻設計表》
並應應課堂作業需求以 Python 進行實作

# 均勻表生成與統計計算程式

此程式旨在生成均勻表 (Orthogonal Array)，並計算其統計特性。適用於需要進行實驗設計和測試數據生成的情境。程式包含了多種數學與資料處理技巧，用來處理和分析均勻表的各種指標。

## 功能

- **生成均勻表**：基於給定的因素數量與水平數量，生成對應的均勻表。
- **顯示表格**：可選擇將均勻表格式化並輸出到終端機中。
- **計算CD值**：計算並顯示均勻表的CD值。
- **浮點數精度控制**：根據需要可以控制計算結果的精度，避免數值誤差。

## 安裝需求

1. Python 3.x
2. 必要的 Python 套件（如：`numpy`，`pandas`，如果需要進行其他數據處理，請安裝相關套件）

## 使用方法

### 1. 計算均勻表的生成

可以使用 `produceTables()` 函數來生成指定因素和水平的均勻表。

```python
from your_module import produceTables

# 生成一個具有 3 個因素，每個因素 2 個水準的均勻表
table = produceTables(factors=3, levels=2)
print(table)
```

### 2. 顯示表格

`tableprint()` 和 `tableprint_sq()` 可以用來顯示生成的均勻表。前者顯示基本表格，後者顯示經過特殊處理後的版本。

```python
from your_module import tableprint

# 顯示表格
tableprint(table)
```

### 3. 計算 CD 值

`CDproTwo()` 函數可用於計算均勻表的 CD 值，這對於確定因素之間的關聯性和強度非常重要。

```python
from your_module import CDproTwo

# 假設已經生成均勻表
cd_value = CDproTwo(table)
print("CD值為：", cd_value)
```

### 4. 浮點數誤差處理

若需要更精確的計算，`deCDproTwo()` 可以處理浮點數誤差，並計算更精確的 CD 值。

```python
from your_module import deCDproTwo

# 計算精確的 CD 值
precise_cd_value = deCDproTwo(table)
print("精確的 CD 值為：", precise_cd_value)
```

## 函數介紹

### `produceTables(factors, levels)`

根據指定的因素數量 (`factors`) 和每個因素的水準數量 (`levels`)，生成對應的均勻表。

### `tableprint(table)`

將均勻表格式化並打印在終端機中。

### `tableprint_sq(table)`

顯示經過特殊處理後的均勻表，通常用於進行更多分析。

### `CDproTwo(table)`

計算並返回均勻表的 CD 值。

### `deCDproTwo(table)`

考慮浮點數誤差，計算並返回更精確的 CD 值。

## 註意事項

1. 此程式設計目的是進行實驗設計和測試數據生成，對於非常大規模的均勻表，可能需要進行效能優化。
2. 需要安裝相關 Python 套件來支援數據處理，請依需求安裝。

若您有任何問題或改進建議，請隨時提出 PR 或問題報告。

